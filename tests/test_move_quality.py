"""Independent move labels, including conservative special-label evidence."""

import unittest

import chess

from core.move_quality import classify_move


def row_for(fen=chess.STARTING_FEN, san="e4", **changes):
    board = chess.Board(fen)
    move = board.parse_san(san)
    row = {
        "fen_before": fen,
        "played_move": san,
        "played_uci": move.uci(),
        "best_move": san,
        "best_uci": move.uci(),
        "expected_before": 0.65,
        "expected_after": 0.65,
        "second_best_expected": None,
        "legal_move_count": board.legal_moves.count(),
        "reply_pv": [],
        "mate_before": None,
        "mate_after": None,
    }
    board.push(move)
    row["fen_after"] = board.fen()
    row.update(changes)
    return row


class MoveQualityTests(unittest.TestCase):
    def test_an_alternative_checkmate_does_not_claim_that_mate_was_lost(self):
        quality = classify_move(row_for(
            "7k/5K2/8/5Q2/8/8/8/8 w - - 0 42", "Qh5#",
            best_move="Qh3#", best_uci="f5h3", expected_before=1.0, expected_after=1.0,
            mate_before=1, mate_after=0, eval_after_cp=100000,
        ))
        self.assertEqual(quality["key"], "excellent")
        self.assertNotIn("no longer preserves", quality["reason"])

    def test_cutoffs_include_upper_boundary_and_next_value_changes_class(self):
        for loss, key in (
            (0, "excellent"), (0.02, "excellent"),
            (0.020001, "good"), (0.05, "good"),
            (0.050001, "inaccuracy"), (0.10, "inaccuracy"),
            (0.100001, "mistake"), (0.20, "mistake"),
            (0.200001, "blunder"), (0.8, "blunder"),
        ):
            with self.subTest(loss=loss):
                quality = classify_move(row_for(
                    best_move="d4", best_uci="d2d4",
                    expected_before=0.8, expected_after=0.8 - loss,
                ))
                self.assertEqual(quality["key"], key)
                self.assertAlmostEqual(quality["loss"], loss)

    def test_best_move_gets_zero_loss_despite_independent_search_noise(self):
        quality = classify_move(row_for(expected_before=0.7, expected_after=0.4))
        self.assertEqual(quality["key"], "best")
        self.assertEqual(quality["loss"], 0)
        self.assertIn("search", quality["reason"].lower())

    def test_negative_loss_is_clamped_without_awarding_a_special_move(self):
        quality = classify_move(row_for(
            best_move="d4", best_uci="d2d4", expected_after=0.75,
        ))
        self.assertEqual((quality["key"], quality["loss"]), ("excellent", 0))

    def test_only_legal_move_is_forced_even_with_a_losing_evaluation(self):
        quality = classify_move(row_for(
            "7r/8/8/8/8/5k2/8/7K w - - 0 1", "Kg1",
            expected_before=0.01, expected_after=0.01,
        ))
        self.assertEqual(quality["key"], "forced")

    def test_incorrect_legal_count_does_not_turn_an_ordinary_move_into_forced(self):
        quality = classify_move(row_for(legal_move_count=1))
        self.assertEqual(quality["key"], "best")

    def test_unique_good_best_move_is_explicitly_only_a_great_candidate(self):
        quality = classify_move(row_for(second_best_expected=0.54))
        self.assertEqual((quality["key"], quality["label"]), ("great", "Great candidate"))
        self.assertIn("second", quality["reason"].lower())

    def test_great_candidate_requires_gap_and_a_non_losing_non_overwhelming_position(self):
        cases = (
            {"second_best_expected": 0.56},
            {"second_best_expected": None},
            {"second_best_expected": 0.10, "expected_before": 0.3, "expected_after": 0.3},
            {"second_best_expected": 0.7, "expected_before": 0.98, "expected_after": 0.98},
            {"second_best_expected": 0.4, "expected_after": 0.3},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                self.assertEqual(classify_move(row_for(**changes))["key"], "best")

    def test_legal_piece_offer_with_persistent_material_loss_is_a_brilliant_candidate(self):
        quality = classify_move(row_for(
            "r1bq1rk1/ppp1bppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 0 8",
            "Bxh7+", expected_after=0.64,
            reply_pv=["Kxh7", "Ng5+", "Kg8"],
        ))
        self.assertEqual((quality["key"], quality["label"]), ("brilliant", "Brilliant candidate"))
        self.assertIn("2", quality["reason"])

    def test_exchange_is_not_a_brilliant_sacrifice(self):
        quality = classify_move(row_for(
            "3rk3/8/8/8/8/8/8/3RK3 w - - 0 1", "Rxd8+",
            reply_pv=["Kxd8", "Ke2", "Ke7"],
        ))
        self.assertEqual(quality["key"], "best")

    def test_immediate_material_recovery_is_not_a_brilliant_sacrifice(self):
        quality = classify_move(row_for(
            "5nk1/R6r/8/8/8/8/8/K6Q w - - 0 1", "Qxh7+",
            reply_pv=["Nxh7", "Rxh7", "Kf8"],
        ))
        self.assertEqual(quality["key"], "best")

    def test_pinned_capture_is_not_evidence_of_a_sacrifice(self):
        quality = classify_move(row_for(
            "4k3/8/4p3/8/4B3/8/8/K3R3 w - - 0 1", "Bf5",
            reply_pv=["exf5", "Rb1", "Kf7"],
        ))
        self.assertEqual(quality["key"], "best")

    def test_en_passant_capture_does_not_invent_a_piece_sacrifice(self):
        quality = classify_move(row_for(
            "4k3/8/8/8/3Pp3/8/8/4K3 b - d3 0 1", "exd3",
            reply_pv=["Kd2", "Kd7", "Kxd3"],
        ))
        self.assertEqual(quality["key"], "best")

    def test_short_or_illegal_sacrifice_line_keeps_best(self):
        fen = "r1bq1rk1/ppp1bppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 0 8"
        for pv in ([], ["Kxh7"], ["Kxh7", "Ng5+"], ["Kxh7", "Ke8", "Kg8"]):
            with self.subTest(pv=pv):
                self.assertEqual(classify_move(row_for(fen, "Bxh7+", reply_pv=pv))["key"], "best")

    def test_null_move_in_a_reply_line_is_not_sacrifice_evidence(self):
        quality = classify_move(row_for(
            "r1bq1rk1/ppp1bppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 0 8",
            "Bxh7+", reply_pv=["Kxh7", "--", "Kg8"],
        ))
        self.assertEqual(quality["key"], "best")

    def test_brilliant_candidate_requires_a_sound_not_already_overwhelming_position(self):
        fen = "r1bq1rk1/ppp1bppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 0 8"
        for before, after in ((0.65, 0.49), (0.65, 0.62), (0.98, 0.98)):
            with self.subTest(before=before, after=after):
                quality = classify_move(row_for(
                    fen, "Bxh7+", reply_pv=["Kxh7", "Ng5+", "Kg8"],
                    expected_before=before, expected_after=after,
                ))
                self.assertEqual(quality["key"], "best")

    def test_candidate_evidence_rejects_a_mismatched_after_position_turn(self):
        row = row_for(
            "r1bq1rk1/ppp1bppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R1BQ1RK1 w - - 0 8",
            "Bxh7+", reply_pv=["Kxh7", "Ng5+", "Kg8"],
        )
        row["fen_after"] = row["fen_after"].replace(" b ", " w ")
        self.assertEqual(classify_move(row)["key"], "best")

    def test_missing_a_known_mate_adds_reason_without_inventing_a_miss_label(self):
        quality = classify_move(row_for(
            best_move="d4", best_uci="d2d4", mate_before=3,
            expected_before=1, expected_after=0.5,
        ))
        self.assertEqual(quality["key"], "blunder")
        self.assertIn("mate", quality["reason"].lower())

    def test_expected_scores_must_be_finite_fractions(self):
        for value in (None, float("nan"), float("inf"), -0.01, 1.01, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                classify_move(row_for(expected_before=value))


if __name__ == "__main__":
    unittest.main()
