import unittest

from botetourt.board import Board


class TestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assertPieceOnSquare(self, piece):
        msg = '{0} {1} is not on {2}{3}'.format(
                piece.color, piece.class_name, piece.file, piece.rank)
        other_piece = piece.board[piece.file][piece.rank]
        self.assertIsNot(None, other_piece, msg)
        self.assertEqual(piece, other_piece)

    def assertPieceAttacks(self, piece, file, rank):
        squares = piece.get_squares_this_piece_attacks()
        self.assertIn((file, rank), squares)

    def assertPieceDoesNotAttack(self, piece, file, rank):
        squares = piece.get_squares_this_piece_attacks()
        self.assertNotIn((file, rank), squares)
