from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class BishopTests(TestCase):
    def test_cannot_move_north(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 3)

    def test_can_move_north_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 2)

    def test_can_move_south_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_south(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 1)

    def test_can_move_south_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'a', 1)

    def test_cannot_move_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'a', 2)

    def test_can_move_north_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'a', 3)

    def test_can_move_north_east_two_spaces(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'd', 4)

    def test_attack_squares_unblocked(self):
        bishop = self.board.set_piece(Bishop, WHITE, 'd', 4)
        self.assertPieceAttacks(bishop, 'd', 4)
        self.assertPieceAttacks(bishop, 'e', 5)
        self.assertPieceAttacks(bishop, 'f', 6)
        self.assertPieceAttacks(bishop, 'c', 3)
        self.assertPieceDoesNotAttack(bishop, 'd', 5)

    def test_attack_squares_blocked(self):
        bishop = self.board.set_piece(Bishop, WHITE, 'd', 4)
        pawn = self.board.set_piece(Pawn, WHITE, 'e', 5)
        self.assertPieceAttacks(bishop, 'd', 4)
        self.assertPieceAttacks(bishop, 'e', 5)
        self.assertPieceDoesNotAttack(bishop, 'f', 6)


