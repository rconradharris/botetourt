import unittest

FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = range(1, 9)
WHITE = 'w'
BLACK = 'b'


class ChessException(Exception):
    pass


class NoPieceThere(ChessException):
    pass


class MoveNotAllowed(ChessException):
    pass


class NotAValidFile(MoveNotAllowed):
    pass


class NotAValidRank(MoveNotAllowed):
    pass


class CannotMoveToSameSquare(MoveNotAllowed):
    pass


class PawnCannotMoveSideways(MoveNotAllowed):
    pass


class CannotMoveThatManySquares(MoveNotAllowed):
    pass


class PawnCannotMoveBackwards(MoveNotAllowed):
    pass


class RookCannotMoveDiagonal(MoveNotAllowed):
    pass


class BishopMustMoveDiagonal(MoveNotAllowed):
    pass


class Piece(object):
    def __init__(self, board, color, file, rank):
        self.board = board
        self.color = color
        self.file = file
        self.rank = rank
        self.moved = False

    def __str__(self):
        sym = self.SYMBOL
        return sym.lower() if self.color == BLACK else sym.upper()

    def __repr__(self):
        return str(self)

    def check_valid_move(self, new_file, new_rank):
        pass

    def move(self, new_file, new_rank):
        self.check_valid_move(new_file, new_rank)
        self.file = new_file
        self.rank = new_rank
        self.moved = True


class Pawn(Piece):
    SYMBOL = 'P'

    def check_valid_move(self, new_file, new_rank):
        # A pawn can only push forward or backward
        if new_file != self.file:
            raise PawnCannotMoveSideways

        delta_rank = new_rank - self.rank

        # A pawn can push two squares forward on first move, otherwise it can
        # only push one square
        max_squares = 1 if self.moved else 2

        if abs(delta_rank) > max_squares:
            raise CannotMoveThatManySquares

        # White can only move North
        if delta_rank < 0 and self.color == WHITE:
            raise PawnCannotMoveBackwards

        # Black can only move South
        if delta_rank > 0 and self.color == BLACK:
            raise PawnCannotMoveBackwards


class Knight(Piece):
    SYMBOL = 'K'

    def check_valid_move(self, new_file, new_rank):
        delta_rank = new_rank - self.rank
        delta_file = FILES.index(new_file) - FILES.index(self.file)
        # A knight can move 2 spaces along a rank but must move one space
        # along file
        if abs(delta_rank) == 2 and abs(delta_file) == 1:
            pass
        # Or vice versa...
        elif abs(delta_file) == 2 and abs(delta_rank) == 1:
            pass
        else:
            raise MoveNotAllowed


class Bishop(Piece):
    SYMBOL = 'B'

    def check_valid_move(self, new_file, new_rank):
        delta_rank = new_rank - self.rank
        delta_file = FILES.index(new_file) - FILES.index(self.file)

        # A bishop must move along a diagonal
        if abs(delta_rank) != abs(delta_file):
            raise BishopMustMoveDiagonal


class Rook(Piece):
    SYMBOL = 'R'

    def check_valid_move(self, new_file, new_rank):
        # A rook must move along a single rank or file
        if new_file != self.file and new_rank != self.rank:
            raise RookCannotMoveDiagonal


class Queen(Piece):
    SYMBOL = 'Q'
    
    def check_valid_move(self, new_file, new_rank):
        delta_rank = new_rank - self.rank
        delta_file = FILES.index(new_file) - FILES.index(self.file)

        # A queen can move along any file
        if new_file == self.file:
            pass
        # Or any rank
        elif new_rank == self.rank:
            pass
        # Or along any diagonal
        elif abs(delta_file) != abs(delta_rank):
            raise MoveNotAllowed


class King(Piece):
    SYMBOL = 'K'

    def check_valid_move(self, new_file, new_rank):
        # A king can move one square in any direction
        delta_rank = new_rank - self.rank
        if abs(delta_rank) > 1:
            raise CannotMoveThatManySquares

        delta_file = FILES.index(new_file) - FILES.index(self.file)
        if abs(delta_file) > 1:
            raise CannotMoveThatManySquares



class Board(object):
    def __init__(self):
        self.clear_board()

    def as_grid(self):
        ranks = []
        for rank in reversed(RANKS):
            ranks.append([self.state[file][rank] for file in FILES])
        return ranks

    def __str__(self):
        grid = self.as_grid()
        str_ranks = []
        for rank in grid:
            str_rank = []
            for piece in rank:
                contents = str(piece) if piece else ' '
                str_rank.append('[%s]' % contents)
            str_ranks.append(''.join(str_rank))
        return '\n'.join(str_ranks)

    def __getitem__(self, file):
        return self.state[file]

    def clear_board(self):
        self.state = {}
        for file in FILES:
            self.state[file] = {}
            for rank in RANKS:
                self.state[file][rank] = None

    def set_piece(self, piece_class, color, file, rank):
        self.check_piece_placement(file, rank)
        piece = piece_class(self, color, file, rank)
        self[file][rank] = piece

    def setup_pieces(self):
        for rank in RANKS:
            self.set_piece(Pawn, WHITE, 'b', rank)
            self.set_piece(Pawn, BLACK, 'g', rank)

        for file, color in (('a', WHITE), ('h', BLACK)):
            self.set_piece(Rook, color, file, 1)
            self.set_piece(Rook, color, file, 8)
            self.set_piece(Knight, color, file, 2)
            self.set_piece(Knight, color, file, 7)
            self.set_piece(Bishop, color, file, 3)
            self.set_piece(Bishop, color, file, 6)
            self.set_piece(Queen, color, file, 4)
            self.set_piece(King, color, file, 5)

    def check_piece_placement(self, file, rank):
        if file not in FILES:
            raise NotAValidFile

        if rank not in RANKS:
            raise NotAValidRank

    def move_piece(self, file, rank, new_file, new_rank):
        self.check_piece_placement(file, rank)

        if file == new_file and rank == new_rank:
            raise CannotMoveToSameSquare

        piece = self[file][rank]
        if not piece:
            raise NoPieceThere
        piece.move(new_file, new_rank)
        self[new_file][new_rank] = piece
        self[file][rank] = None



class BoardTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_invalid_file(self):
        with self.assertRaises(NotAValidFile):
            self.board.set_piece(Pawn, WHITE, 'i', 2)

    def test_invalid_rank(self):
        with self.assertRaises(NotAValidRank):
            self.board.set_piece(Pawn, WHITE, 'h', 0)

        with self.assertRaises(NotAValidRank):
            self.board.set_piece(Pawn, WHITE, 'h', 9)

    def test_cannot_move_to_same_square(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(CannotMoveToSameSquare):
            self.board.move_piece('b', 2, 'b', 2)


class _PieceTests(unittest.TestCase):
    def setUp(self):
        self.board = Board()



class BishopTests(_PieceTests):
    def test_cannot_move_north(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(BishopMustMoveDiagonal):
            self.board.move_piece('b', 2, 'b', 3)

    def test_can_move_north_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(BishopMustMoveDiagonal):
            self.board.move_piece('b', 2, 'c', 2)

    def test_can_move_south_east(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_south(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(BishopMustMoveDiagonal):
            self.board.move_piece('b', 2, 'b', 1)

    def test_can_move_south_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'a', 1)

    def test_cannot_move_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        with self.assertRaises(BishopMustMoveDiagonal):
            self.board.move_piece('b', 2, 'a', 2)

    def test_can_move_north_west(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'a', 3)

    def test_can_move_north_east_two_spaces(self):
        self.board.set_piece(Bishop, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'd', 4)


class KingTests(_PieceTests):
    def setUp(self):
        super(KingTests, self).setUp()
        self.board.set_piece(King, WHITE, 'b', 2)

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

    def test_disallow_two_square_move(self):
        with self.assertRaises(CannotMoveThatManySquares):
            self.board.move_piece('b', 2, 'b', 4)


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
        with self.assertRaises(RookCannotMoveDiagonal):
            self.board.move_piece('b', 2, 'c', 3)

    def test_cannot_move_south_east(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(RookCannotMoveDiagonal):
            self.board.move_piece('b', 2, 'c', 1)

    def test_cannot_move_south_west(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(RookCannotMoveDiagonal):
            self.board.move_piece('b', 2, 'a', 1)

    def test_cannot_move_north_west(self):
        self.board.set_piece(Rook, WHITE, 'b', 2)
        with self.assertRaises(RookCannotMoveDiagonal):
            self.board.move_piece('b', 2, 'a', 3)


class PawnTests(_PieceTests):
    def test_allow_one_square_push_forward(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 3)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 6)

    def test_disallow_push_sideways(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(PawnCannotMoveSideways):
            self.board.move_piece('b', 2, 'c', 2)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(PawnCannotMoveSideways):
            self.board.move_piece('g', 7, 'h', 7)

    def test_disallow_push_three_squares(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(CannotMoveThatManySquares):
            self.board.move_piece('b', 2, 'b', 5)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(CannotMoveThatManySquares):
            self.board.move_piece('g', 7, 'g', 4)

    def test_disallow_push_backwards(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        with self.assertRaises(PawnCannotMoveBackwards):
            self.board.move_piece('b', 2, 'b', 1)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        with self.assertRaises(PawnCannotMoveBackwards):
            self.board.move_piece('g', 7, 'g', 8)

    def test_allow_two_square_push_on_first_move(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 4)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 5)

    def test_disallow_two_square_push_on_second_move(self):
        self.board.set_piece(Pawn, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'b', 4)
        with self.assertRaises(CannotMoveThatManySquares):
            self.board.move_piece('b', 4, 'b', 6)

        self.board.set_piece(Pawn, BLACK, 'g', 7)
        self.board.move_piece('g', 7, 'g', 5)
        with self.assertRaises(CannotMoveThatManySquares):
            self.board.move_piece('g', 5, 'g', 3)


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


class KnightTests(_PieceTests):
    def test_can_move_two_spaces_east_and_one_space_north(self):
        self.board.set_piece(Knight, WHITE, 'b', 2)
        self.board.move_piece('b', 2, 'd', 3)

    def test_cannot_move_one_space_east(self):
        self.board.set_piece(Knight, WHITE, 'b', 2)
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'c', 2)


if __name__ == '__main__':
    unittest.main()
