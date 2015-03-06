from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class RookTests(TestCase):
    def test_can_move_north(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 8)

    def test_can_move_south(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 1)

    def test_can_move_east(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'c', 2)

    def test_can_move_west(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'a', 2)

    def test_cannot_move_north_east(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_south_east(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 1)

    def test_cannot_move_south_west(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'a', 1)

    def test_cannot_move_north_west(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'a', 3)

    def test_attacks_unblocked(self):
        rook = self.board.set_piece(Rook, WHITE, 'd', 4)
        self.assertPieceAttacks(rook, 'd', 4)
        self.assertPieceAttacks(rook, 'f', 4)
        self.assertPieceAttacks(rook, 'd', 6)
        self.assertPieceDoesNotAttack(rook, 'f', 5)

    def test_attacks_blocked(self):
        rook = self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        self.assertPieceAttacks(rook, 'a', 1)
        self.assertPieceAttacks(rook, 'a', 2)
        self.assertPieceDoesNotAttack(rook, 'a', 3)

        self.assertPieceAttacks(rook, 'c', 1)

        self.board.set_piece(Pawn, WHITE, 'b', 1)

        self.assertPieceAttacks(rook, 'b', 1)
        self.assertPieceDoesNotAttack(rook, 'c', 1)



