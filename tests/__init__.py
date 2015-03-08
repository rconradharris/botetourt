import unittest

from botetourt.board import Board


class TestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assertPieceOnSquare(self, piece, file, rank):
        self.assertEqual((file, rank),
                         (piece.file, piece.rank),
                         '{0} is not on {1}{2}'.format(
                             piece.class_name, file, rank))

    def assertPieceAttacks(self, piece, file, rank):
        self.assertIn((file, rank), piece.attacks())

    def assertPieceDoesNotAttack(self, piece, file, rank):
        self.assertNotIn((file, rank), piece.attacks())
