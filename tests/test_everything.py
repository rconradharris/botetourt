import unittest

from botetourt.board import Board, WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed, NotAValidSquare



class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_invalid_file(self):
        with self.assertRaises(NotAValidSquare):
            self.board.set_piece(Pawn, WHITE, 'i', 2)

    def test_invalid_rank(self):
        with self.assertRaises(NotAValidSquare):
            self.board.set_piece(Pawn, WHITE, 'h', 0)

        with self.assertRaises(NotAValidSquare):
            self.board.set_piece(Pawn, WHITE, 'h', 9)

    def test_cannot_move_to_same_square(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 2)

    def test_cannot_move_to_occupied_square(self):
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('a', 1, 'a', 2)

    def test_cannot_move_along_blocked_file(self):
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('a', 1, 'a', 3)

    def test_cannot_move_along_blocked_rank(self):
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Knight, WHITE, 'b', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('a', 1, 'c', 1)

    def test_cannot_move_along_blocked_diagonal(self):
        self.board.set_piece(Bishop, WHITE, 'c', 1)
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('c', 1, 'a', 3)

    def test_capture(self):
        self.assertEqual([], self.board.captured_pieces[WHITE])
        self.board.set_piece(Rook, WHITE, 'a', 1)
        black_pawn = self.board.set_piece(Pawn, BLACK, 'a', 7)
        self.board.move_piece('a', 1, 'a', 7)
        self.assertEqual([black_pawn], self.board.captured_pieces[WHITE])


class _PieceTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assertPieceAttacks(self, piece, file, rank):
        self.assertIn((file, rank), piece.attacks())

    def assertPieceDoesNotAttack(self, piece, file, rank):
        self.assertNotIn((file, rank), piece.attacks())


class BishopTests(_PieceTests):
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


class KingTests(_PieceTests):
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


class RookTests(_PieceTests):
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



class PawnTests(_PieceTests):
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
        self.board.set_piece(Pawn, BLACK, 'a', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 3)

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


class QueenTests(_PieceTests):
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


class KnightTests(_PieceTests):
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


if __name__ == '__main__':
    unittest.main()
