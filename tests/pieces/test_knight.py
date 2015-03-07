from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class KnightTests(TestCase):
    def test_can_move_two_spaces_east_and_one_space_north(self):
        self.board.set_piece(Knight, WHITE, 'b', 1)
        self.board.move_piece('b', 1, 'c', 3)

    def test_cannot_move_one_space_east(self):
        self.board.set_piece(Knight, WHITE, 'b', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 1, 'c', 1)

    def test_can_jump_over_pieces(self):
        self.board.set_piece(Knight, WHITE, 'b', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Pawn, WHITE, 'c', 2)

        self.board.move_piece('b', 1, 'c', 3)

    def test_attack_squares(self):
        knight = self.board.set_piece(Knight, WHITE, 'd', 4)
        self.assertPieceAttacks(knight, 'e', 6)
        self.assertPieceAttacks(knight, 'f', 5)
        self.assertPieceAttacks(knight, 'f', 3)
        self.assertPieceAttacks(knight, 'e', 2)

        self.assertPieceAttacks(knight, 'c', 2)
        self.assertPieceAttacks(knight, 'b', 3)
        self.assertPieceAttacks(knight, 'b', 5)
        self.assertPieceAttacks(knight, 'c', 6)

    def test_knight_can_capture_opposite_color(self):
        knight = self.board.set_piece(Knight, WHITE, 'd', 4)
        self.board.set_piece(Pawn, BLACK, 'f', 3)
        self.board.move_piece('d', 4, 'f', 3)

    def test_knight_cannot_capture_same_color(self):
        knight = self.board.set_piece(Knight, WHITE, 'd', 4)
        self.board.set_piece(Pawn, WHITE, 'f', 3)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('d', 4, 'f', 3)
