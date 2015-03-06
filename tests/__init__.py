import unittest

from botetourt.board import Board


class TestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assertPieceAttacks(self, piece, file, rank):
        self.assertIn((file, rank), piece.attacks())

    def assertPieceDoesNotAttack(self, piece, file, rank):
        self.assertNotIn((file, rank), piece.attacks())
