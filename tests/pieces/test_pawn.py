from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class PawnTests(TestCase):
    def test_allow_one_square_push_forward(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 3)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 6)

    def test_disallow_push_sideways(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 2)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('g', 7, 'h', 7)

    def test_disallow_push_three_squares(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 5)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('g', 7, 'g', 4)

    def test_disallow_push_backwards(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 1)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('g', 7, 'g', 8)

    def test_allow_two_square_push_on_first_move(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 4)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 5)

    def test_disallow_two_square_push_on_second_move(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 4)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 4, 'b', 6)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 5)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('g', 5, 'g', 3)

    def test_white_cannot_capture_north(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Pawn, BLACK, 'b', 3)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 3)

    def test_white_captures_diagonally_north_east(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Pawn, BLACK, 'c', 3)
        self.board.move_piece('b', 2, 'c', 3)

    def test_white_cannot_capture_south(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Pawn, BLACK, 'b', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 1)

    def test_white_cannot_capture_south_east(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.set_piece(Pawn, BLACK, 'c', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 1)

    def test_black_can_capture_south_east(self):
        self.board.set_piece(Pawn, BLACK, 'b', 2)
        self.board.set_piece(Pawn, WHITE, 'c', 1)
        self.board.move_piece('b', 2, 'c', 1)

    def test_attack_squares_unblocked(self):
        pawn = self.board.set_piece(Pawn, WHITE, 'd', 4)
        self.assertPieceAttacks(pawn, 'c', 5)
        self.assertPieceDoesNotAttack(pawn, 'd', 5)
        self.assertPieceAttacks(pawn, 'e', 5)
        self.assertPieceDoesNotAttack(pawn, 'f', 6)
        self.assertPieceDoesNotAttack(pawn, 'e', 3)
