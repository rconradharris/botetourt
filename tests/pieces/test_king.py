from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class KingTests(TestCase):
    def setUp(self):
        super(KingTests, self).setUp()
        self.king = self.board.set_piece(King, WHITE, 'b', 2)

    def test_allow_one_square_north(self):
        self.board.move_piece('b', 2, 'b', 3)

    def test_allow_one_square_north_east(self):
        self.board.move_piece('b', 2, 'c', 3)

    def test_allow_one_square_east(self):
        self.board.move_piece('b', 2, 'c', 2)

    def test_allow_one_square_south_east(self):
        self.board.move_piece('b', 2, 'c', 1)

    def test_allow_one_square_south(self):
        self.board.move_piece('b', 2, 'b', 1)

    def test_allow_one_square_south_west(self):
        self.board.move_piece('b', 2, 'a', 1)

    def test_allow_one_square_west(self):
        self.board.move_piece('b', 2, 'a', 2)

    def test_allow_one_square_north_west(self):
        self.board.move_piece('b', 2, 'a', 3)

    def test_disallow_two_square_north(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 4)

    def test_disallow_two_square_east(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'd', 2)

    def test_disallow_two_square_north_east(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'd', 4)

    def test_attack_squares_unblocked(self):
        self.assertPieceAttacks(self.king, 'b', 3)
        self.assertPieceAttacks(self.king, 'c', 2)
        self.assertPieceAttacks(self.king, 'c', 3)

        self.assertPieceDoesNotAttack(self.king, 'b', 4)
        self.assertPieceDoesNotAttack(self.king, 'd', 2)
        self.assertPieceDoesNotAttack(self.king, 'd', 4)

    def test_check(self):
        self.black_king = self.board.set_piece(King, BLACK, 'b', 8)
        rook = self.board.set_piece(Rook, WHITE, 'b', 3)
        self.assertTrue(self.black_king.in_check())
        self.assertFalse(self.king.in_check())

    def test_cannot_move_into_check(self):
        self.black_king = self.board.set_piece(King, BLACK, 'b', 4)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 3)


class CastlingTests(TestCase):
    def setUp(self):
        super(CastlingTests, self).setUp()
        self.king = self.board.set_piece(King, WHITE, 'e', 1)
        self.king_rook = self.board.set_piece(Rook, WHITE, 'h', 1)
        self.queen_rook = self.board.set_piece(Rook, WHITE, 'a', 1)

    def test_can_castle_king_side(self):
        self.board.move_piece('e', 1, 'g', 1)
        self.assertPieceOnSquare(King(self.board, WHITE, 'g', 1))
        self.assertPieceOnSquare(Rook(self.board, WHITE, 'f', 1))

    def test_can_castle_queen_side(self):
        self.board.move_piece('e', 1, 'c', 1)
        self.assertPieceOnSquare(King(self.board, WHITE, 'c', 1))
        self.assertPieceOnSquare(Rook(self.board, WHITE, 'd', 1))

    def test_cannot_castle_king_side_if_king_has_moved(self):
        self.board.move_piece('e', 1, 'd', 1)
        self.board.move_piece('d', 1, 'e', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_king_has_moved(self):
        self.board.move_piece('e', 1, 'd', 1)
        self.board.move_piece('d', 1, 'e', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_cannot_castle_king_side_if_h1_is_empty(self):
        self.board.remove_piece('h', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_a1_is_empty(self):
        self.board.remove_piece('a', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_cannot_castle_king_side_if_h1_is_not_a_rook(self):
        self.board.remove_piece('h', 1)
        self.board.set_piece(Queen, WHITE, 'h', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_a1_is_not_a_rook(self):
        self.board.remove_piece('a', 1)
        self.board.set_piece(Queen, WHITE, 'a', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_cannot_castle_king_side_if_in_check(self):
        self.board.set_piece(Rook, BLACK, 'e', 8)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_in_check(self):
        self.board.set_piece(Rook, BLACK, 'e', 8)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_cannot_castle_king_side_if_piece_in_between(self):
        self.board.set_piece(Bishop, WHITE, 'f', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_piece_in_between(self):
        self.board.set_piece(Bishop, WHITE, 'c', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_cannot_castle_king_side_if_check_along_king_path(self):
        self.board.set_piece(Rook, BLACK, 'f', 8)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'g', 1)

    def test_cannot_castle_queen_side_if_check_along_king_path(self):
        self.board.set_piece(Rook, BLACK, 'd', 8)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('e', 1, 'c', 1)

    def test_can_castle_queen_side_if_rook_on_b8(self):
        self.board.set_piece(Rook, BLACK, 'b', 8)
        self.board.move_piece('e', 1, 'c', 1)


class CheckmateTests(TestCase):
    def setUp(self):
        super(CheckmateTests, self).setUp()
        self.king = self.board.set_piece(King, WHITE, 'a', 1)

    def test_smothered_mate(self):
        self.board.set_piece(Rook, WHITE, 'b', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Knight, BLACK, 'c', 2)
        self.assertTrue(self.king.is_checkmated())

    def test_king_can_capture_unprotected_piece(self):
        self.board.set_piece(Rook, WHITE, 'b', 1)
        self.board.set_piece(Rook, BLACK, 'a', 2)
        self.assertFalse(self.king.is_checkmated())

    def test_king_cannot_capture_protected_piece(self):
        self.board.set_piece(Rook, WHITE, 'b', 1)
        self.board.set_piece(Rook, BLACK, 'a', 3)
        self.board.set_piece(Rook, BLACK, 'a', 2)
        self.assertTrue(self.king.is_checkmated())
