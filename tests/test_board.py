from botetourt.board import Board, WHITE, BLACK
from botetourt.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from botetourt.exc import MoveNotAllowed, NotAValidSquare

from tests import TestCase


class BoardTests(TestCase):
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

    def test_cannot_capture_own_piece_along_file(self):
        # White can capture black
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Pawn, BLACK, 'a', 3)
        self.board.move_piece('a', 1, 'a', 3)

        # But not white
        self.board.set_piece(Rook, WHITE, 'h', 1)
        self.board.set_piece(Pawn, WHITE, 'h', 3)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('h', 1, 'h', 3)

    def test_cannot_capture_own_piece_along_rank(self):
        # White can capture black
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Bishop, BLACK, 'c', 1)
        self.board.move_piece('a', 1, 'c', 1)

        # But not white
        self.board.set_piece(Rook, WHITE, 'h', 1)
        self.board.set_piece(Bishop, WHITE, 'f', 1)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('h', 1, 'f', 1)
