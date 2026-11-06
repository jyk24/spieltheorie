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


# ---------------------------------------------------------------------------
# Nim – kombinatorische Spieltheorie
# ---------------------------------------------------------------------------

from app.game_engine import (
    NIM_INITIAL_PILES,
    nim_ai_move,
    nim_final_result,
    nim_play_round,
    nim_sum,
    nim_valid_move,
)


class TestNim:
    def test_nim_sum_xor(self):
        assert nim_sum([3, 4, 5]) == 2
        assert nim_sum([0, 0, 0]) == 0
        assert nim_sum([1, 1]) == 0
        assert nim_sum([7]) == 7

    def test_valid_move_rejects_out_of_range(self):
        assert not nim_valid_move([3, 4, 5], 5, 1)
        assert not nim_valid_move([3, 4, 5], 0, 0)
        assert not nim_valid_move([3, 4, 5], 0, 4)
        assert nim_valid_move([3, 4, 5], 0, 3)
        assert nim_valid_move([3, 4, 5], 2, 1)

    def test_optimal_ai_closes_nim_sum_to_zero(self):
        # XOR 3,4,5 = 2 – optimale KI muss auf 0 reduzieren
        pile, take = nim_ai_move("optimal", [3, 4, 5])
        piles = [3, 4, 5]
        piles[pile] -= take
        assert nim_sum(piles) == 0

    def test_optimal_ai_never_takes_zero(self):
        for _ in range(20):
            pile, take = nim_ai_move("optimal", [2, 4, 6])
            assert take >= 1

    def test_greedy_takes_whole_largest_pile(self):
        pile, take = nim_ai_move("greedy", [2, 7, 3])
        assert pile == 1 and take == 7

    def test_cautious_takes_one(self):
        pile, take = nim_ai_move("cautious", [2, 7, 3])
        assert take == 1

    def test_play_round_removes_stones(self):
        result = nim_play_round([3, 4, 5], 0, 2, "random")
        assert result["piles_after_player"] == [1, 4, 5]
        # KI muss auch etwas genommen haben
        assert sum(result["piles_after_ai"]) < sum(result["piles_after_player"])

    def test_player_wins_when_takes_last_stone(self):
        result = nim_play_round([0, 0, 3], 2, 3, "optimal")
        assert result["player_won"] is True
        assert result["game_over"] is True
        assert result["ai_take"] == 0

    def test_ai_wins_when_takes_last_stone(self):
        # Spieler laesst 1 Stein uebrig – KI nimmt ihn
        result = nim_play_round([0, 0, 2], 2, 1, "optimal")
        assert result["player_won"] is False
        assert result["ai_won"] is True
        assert result["game_over"] is True

    def test_invalid_move_returns_error(self):
        result = nim_play_round([3, 4, 5], 0, 99, "optimal")
        assert "error" in result

    def test_optimal_ai_beats_suboptimal_player(self):
        """Startposition [3,4,5] XOR=2. Wenn Spieler suboptimal startet (z.B. nimmt 1 aus
        Haufen 0 → [2,4,5] XOR=3), muss optimale KI daraus Sieg machen."""
        import random as _r
        _r.seed(42)
        piles = [3, 4, 5]
        history = []
        # Spieler macht ersten Zug: nimmt 1 aus Haufen 0 (suboptimal)
        turn = nim_play_round(piles, 0, 1, "optimal")
        piles = turn["piles_after_ai"]
        history.append(turn)
        # Optimale KI reduziert Nim-Summe auf 0
        assert nim_sum(piles) == 0
        # Weiter spielen – unabhaengig vom Spielerzug bleibt KI in Gewinnposition
        while not turn.get("game_over"):
            # Spieler nimmt 1 aus erstem nicht-leeren Haufen
            idx = next(i for i, p in enumerate(piles) if p > 0)
            turn = nim_play_round(piles, idx, 1, "optimal")
            piles = turn["piles_after_ai"]
            history.append(turn)
        assert turn["ai_won"] is True

    def test_final_result_counts_perfect_moves(self):
        history = [
            {"nim_before": 2, "nim_after_player": 0},
            {"nim_before": 3, "nim_after_player": 0},
            {"nim_before": 1, "nim_after_player": 1},  # Suboptimal
        ]
        final = nim_final_result(history, player_won=True)
        assert final["perfect_moves"] == 2
        assert final["costly_moves"] == 1
        assert final["total_turns"] == 3
        assert final["result"] == "win"

    def test_initial_piles_constant(self):
        assert NIM_INITIAL_PILES == [3, 4, 5]
