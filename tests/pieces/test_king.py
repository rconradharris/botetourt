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


