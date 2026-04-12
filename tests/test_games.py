"""Tests für die Spiellogik (game_engine.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.game_engine import (
    SCENARIOS,
    gd_ai_move,
    gd_final_result,
    gd_play_round,
    trust_ai_return,
    trust_final_result,
    ultimatum_ai_response,
    ultimatum_score,
    verhandlung_ai_offer,
    verhandlung_score,
)


# ---------------------------------------------------------------------------
# Gefangenendilemma
# ---------------------------------------------------------------------------

class TestGefangenendilemma:
    def test_tit_for_tat_first_move_cooperates(self):
        assert gd_ai_move("tit_for_tat", []) == "C"

    def test_tit_for_tat_mirrors_last_move(self):
        history = [{"player": "D", "ai": "C", "player_score": 5, "ai_score": 0, "round": 1,
                    "player_label": "V", "ai_label": "K"}]
        assert gd_ai_move("tit_for_tat", history) == "D"

    def test_always_cooperate(self):
        assert gd_ai_move("always_cooperate", [{"player": "D"}]) == "C"

    def test_always_defect(self):
        assert gd_ai_move("always_defect", []) == "D"

    def test_grim_trigger_triggers_on_defect(self):
        history = [{"player": "D"}]
        assert gd_ai_move("grim_trigger", history) == "D"

    def test_grim_trigger_cooperates_without_defect(self):
        history = [{"player": "C"}]
        assert gd_ai_move("grim_trigger", history) == "C"

    def test_play_round_payoff_cc(self):
        result = gd_play_round("C", "always_cooperate", [])
        assert result["player_score"] == 3
        assert result["ai_score"] == 3

    def test_play_round_payoff_cd(self):
        result = gd_play_round("C", "always_defect", [])
        assert result["player_score"] == 0
        assert result["ai_score"] == 5

    def test_play_round_payoff_dc(self):
        result = gd_play_round("D", "always_cooperate", [])
        assert result["player_score"] == 5
        assert result["ai_score"] == 0

    def test_play_round_payoff_dd(self):
        result = gd_play_round("D", "always_defect", [])
        assert result["player_score"] == 1
        assert result["ai_score"] == 1

    def test_final_result_win(self):
        history = [{"player_score": 5, "ai_score": 0, "player": "D"} for _ in range(10)]
        result = gd_final_result(history)
        assert result["result"] == "win"
        assert result["player_total"] == 50
        assert result["cooperation_rate"] == 0

    def test_final_result_draw(self):
        history = [{"player_score": 3, "ai_score": 3, "player": "C"} for _ in range(10)]
        result = gd_final_result(history)
        assert result["result"] == "draw"
        assert result["cooperation_rate"] == 100


# ---------------------------------------------------------------------------
# Ultimatumspiel
# ---------------------------------------------------------------------------

class TestUltimatumspiel:
    def test_fair_ai_accepts_above_40(self):
        result = ultimatum_ai_response(45, "fair", 0)
        assert result["accepts"] is True

    def test_fair_ai_rejects_below_40(self):
        result = ultimatum_ai_response(35, "fair", 0)
        assert result["accepts"] is False

    def test_strict_ai_rejects_below_50(self):
        result = ultimatum_ai_response(45, "strict", 0)
        assert result["accepts"] is False

    def test_strict_ai_accepts_50(self):
        result = ultimatum_ai_response(50, "strict", 0)
        assert result["accepts"] is True

    def test_score_proposer_accepted(self):
        p, ai = ultimatum_score(40, True, is_proposer=True)
        assert p == 60
        assert ai == 40

    def test_score_rejected(self):
        p, ai = ultimatum_score(40, False, is_proposer=True)
        assert p == 0
        assert ai == 0

    def test_ai_response_has_reason(self):
        result = ultimatum_ai_response(50, "fair", 0)
        assert isinstance(result["reason"], str)
        assert len(result["reason"]) > 0


# ---------------------------------------------------------------------------
# Vertrauensspiel
# ---------------------------------------------------------------------------

class TestVertrauensspiel:
    def test_reciprocal_returns_positive(self):
        result = trust_ai_return(5, "reciprocal")
        assert result["returned"] > 0
        assert result["pot"] == 15

    def test_selfish_returns_little(self):
        result = trust_ai_return(10, "selfish")
        # Egoistisch: gibt max 20% zurück
        assert result["returned"] <= result["pot"] * 0.25

    def test_cooperative_returns_over_half(self):
        result = trust_ai_return(10, "cooperative")
        assert result["returned"] >= result["pot"] * 0.5

    def test_zero_investment(self):
        result = trust_ai_return(0, "reciprocal")
        assert result["pot"] == 0
        assert result["returned"] == 0

    def test_final_result_structure(self):
        history = [trust_ai_return(5, "reciprocal") for _ in range(8)]
        final = trust_final_result(history)
        assert "trust_rate" in final
        assert "result" in final
        assert final["trust_rate"] >= 0


# ---------------------------------------------------------------------------
# Verhandlungssimulation
# ---------------------------------------------------------------------------

class TestVerhandlungssimulation:
    def test_scenarios_exist(self):
        assert "gehalt" in SCENARIOS
        assert "auto" in SCENARIOS
        assert "projekt" in SCENARIOS

    def test_ai_offer_within_range(self):
        sc = SCENARIOS["gehalt"]
        result = verhandlung_ai_offer(sc, 0, None)
        assert sc["min_value"] <= result["offer"] <= sc["max_value"]

    def test_score_above_batna(self):
        sc = SCENARIOS["gehalt"]
        final_price = sc["player_batna"] + 5000
        result = verhandlung_score(sc, final_price, 1)
        assert result["score"] > 0
        assert result["grade"] in ("A", "B", "C", "D")

    def test_score_at_batna_is_zero(self):
        sc = SCENARIOS["gehalt"]
        result = verhandlung_score(sc, sc["player_batna"], 1)
        assert result["score"] == 0

    def test_deal_detection_on_close_offers(self):
        sc = SCENARIOS["gehalt"]
        # Wenn der Spieler sehr nah am KI-Angebot ist, soll Deal ausgelöst werden
        result = verhandlung_ai_offer(sc, 2, sc["player_batna"] + 2000)
        # Kein Crash, Ergebnis hat korrekte Struktur
        assert "offer" in result
        assert "deal" in result
