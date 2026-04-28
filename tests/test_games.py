"""Tests für die Spiellogik (game_engine.py)."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.game_engine import (
    NIM_DEFAULT_HEAPS,
    SCENARIOS,
    gd_ai_move,
    gd_final_result,
    gd_play_round,
    nim_apply_move,
    nim_ai_move,
    nim_final_result,
    nim_is_terminal,
    nim_optimal_move,
    nim_play_turn,
    nim_xor_sum,
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
# Nim (Bouton 1901)
# ---------------------------------------------------------------------------

class TestNim:
    def test_xor_sum_basic(self):
        assert nim_xor_sum([3, 4, 5]) == 2  # 011 ^ 100 ^ 101 = 010
        assert nim_xor_sum([1, 1]) == 0
        assert nim_xor_sum([0, 0, 0]) == 0
        assert nim_xor_sum([7]) == 7

    def test_terminal_detection(self):
        assert nim_is_terminal([0, 0, 0]) is True
        assert nim_is_terminal([0, 1, 0]) is False

    def test_optimal_move_lowers_xor_to_zero(self):
        # Alle hier sind N-Positionen (XOR != 0)
        for heaps in [[3, 4, 5], [5, 7, 9], [1, 4, 7], [2, 4, 7]]:
            move = nim_optimal_move(heaps)
            assert move is not None, f"missed N-position {heaps}"
            i, take = move
            new = list(heaps)
            new[i] -= take
            assert nim_xor_sum(new) == 0
            assert 1 <= take <= heaps[i]

    def test_optimal_move_returns_none_for_p_position(self):
        # XOR=0 -> P-position
        assert nim_optimal_move([1, 1]) is None
        assert nim_optimal_move([3, 5, 6]) is None  # 011 ^ 101 ^ 110 = 000
        assert nim_optimal_move([0, 0, 0]) is None

    def test_apply_move_validation(self):
        with pytest.raises(ValueError):
            nim_apply_move([3, 4, 5], 0, 0)
        with pytest.raises(ValueError):
            nim_apply_move([3, 4, 5], 0, 4)
        with pytest.raises(ValueError):
            nim_apply_move([3, 4, 5], 5, 1)

    def test_apply_move_correct(self):
        assert nim_apply_move([3, 4, 5], 1, 2) == [3, 2, 5]

    def test_play_turn_normal_round(self):
        history: list = []
        rec = nim_play_turn([3, 4, 5], 0, 1, "random", history)
        assert rec["player_take"] == 1
        assert rec["after_player"] == [2, 4, 5]
        assert rec["ai_heap"] is not None
        assert sum(rec["after_ai"]) < sum([3, 4, 5])
        assert rec["is_final"] is False
        assert rec["winner"] is None

    def test_play_turn_player_wins(self):
        # Spieler nimmt den letzten Stein
        rec = nim_play_turn([0, 0, 1], 2, 1, "optimal", [])
        assert rec["is_final"] is True
        assert rec["winner"] == "player"
        assert rec["after_player"] == [0, 0, 0]
        assert rec["ai_heap"] is None  # KI nicht mehr am Zug

    def test_play_turn_ai_can_finish(self):
        # Nach Spielerzug bleibt 1 Stein -> KI nimmt ihn
        rec = nim_play_turn([0, 0, 2], 2, 1, "random", [])
        assert rec["after_player"] == [0, 0, 1]
        assert rec["after_ai"] == [0, 0, 0]
        assert rec["is_final"] is True
        assert rec["winner"] == "ai"

    def test_optimal_ai_always_wins_from_p_position(self):
        # Wenn der Spieler in einer P-Position startet, gewinnt die optimale KI immer.
        # Test: Spieler spielt zufällig, KI optimal, Startposition [1, 1] (P-Position)
        random.seed(42)
        player_wins = 0
        for _ in range(50):
            heaps = [1, 1]
            history: list = []
            while not nim_is_terminal(heaps):
                # zufälliger Spielerzug
                from app.game_engine import nim_random_move
                hi, tk = nim_random_move(heaps)
                rec = nim_play_turn(heaps, hi, tk, "optimal", history)
                history.append(rec)
                heaps = rec["after_ai"]
                if rec["is_final"]:
                    if rec["winner"] == "player":
                        player_wins += 1
                    break
        assert player_wins == 0, "Optimal AI must never lose from a P-position"

    def test_final_result_structure(self):
        history = [{
            "round": 1, "before": [3, 4, 5], "player_heap": 0, "player_take": 2,
            "after_player": [1, 4, 5], "ai_heap": 1, "ai_take": 4,
            "after_ai": [1, 0, 5], "xor_after_player": 0, "is_final": False, "winner": None,
        }, {
            "round": 2, "before": [1, 0, 5], "player_heap": 2, "player_take": 5,
            "after_player": [1, 0, 0], "ai_heap": 0, "ai_take": 1,
            "after_ai": [0, 0, 0], "xor_after_player": 1, "is_final": True, "winner": "ai",
        }]
        final = nim_final_result(history, "optimal")
        assert final["result"] == "loss"
        assert final["rounds"] == 2
        assert final["optimal_player_moves"] == 1
        assert final["optimal_rate"] == 50
