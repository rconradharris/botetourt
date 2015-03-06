from botetourt.board import WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed

from tests import TestCase


class QueenTests(TestCase):
    def test_can_move_two_spaces_east(self):
        self.board.set_piece(Queen, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 4)

    def test_can_move_two_spaces_north_east(self):
        self.board.set_piece(Queen, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'd', 4)

    def test_cannot_move_two_spaces_east_and_one_space_north(self):
        self.board.set_piece(Queen, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'd', 3)

    def test_attack_squares_unblocked(self):
        queen = self.board.set_piece(Queen, WHITE, 'd', 4)
        self.assertPieceAttacks(queen, 'h', 4)
        self.assertPieceAttacks(queen, 'd', 1)
        self.assertPieceAttacks(queen, 'e', 5)
        self.assertPieceDoesNotAttack(queen, 'e', 6)
