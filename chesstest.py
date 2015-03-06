import unittest

FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = range(1, 9)
WHITE = 'w'
BLACK = 'b'
INFINITY = 999
NORTH = 'north'
SOUTH = 'south'


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


class CannotMoveToOccupiedSquare(MoveNotAllowed):
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

    def _delta_file_rank(self, new_file, new_rank):
        delta_file = FILES.index(new_file) - FILES.index(self.file)
        delta_rank = new_rank - self.rank
        return delta_file, delta_rank

    def _get_ranks_in_between(self, new_rank):
        if self.rank < new_rank:
            return RANKS[self.rank:new_rank-1]
        else:
            return RANKS[new_rank:self.rank-1]

    def _is_file_blocked(self, new_rank):
        ranks_in_between = self._get_ranks_in_between(new_rank)

        for rank in ranks_in_between:
            if self.board[self.file][rank]:
                return True

        return False

    def _is_valid_file_move(self, new_file, new_rank, piece_range=INFINITY,
                            direction_allowed=None):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        if direction_allowed == NORTH and delta_rank < 0:
            return False
        elif direction_allowed == SOUTH and delta_rank > 0:
            return False
        else:
            return (delta_file == 0 and
                    abs(delta_rank) <= piece_range and 
                    not self._is_file_blocked(new_rank))

    def _get_files_in_between(self, new_file):
        orig_idx = FILES.index(self.file)
        new_idx = FILES.index(new_file)
        if orig_idx < new_idx:
            return FILES[orig_idx+1:new_idx]
        else:
            return FILES[new_idx+1:orig_idx]

    def _is_rank_blocked(self, new_file):
        files_in_between = self._get_files_in_between(new_file)

        for file in files_in_between:
            if self.board[file][self.rank]:
                return True

        return False

    def _is_valid_rank_move(self, new_file, new_rank, piece_range=INFINITY):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)
        return (delta_rank == 0 and
                abs(delta_file) <= piece_range and
                not self._is_rank_blocked(new_file))

    def _is_diagonal_blocked(self, new_file, new_rank):
        ranks_in_between = self._get_ranks_in_between(new_rank)
        files_in_between = self._get_files_in_between(new_file)

        for file, rank in zip(files_in_between, ranks_in_between):
            if self.board[file][rank]:
                return True

        return False

    def _is_valid_diagonal_move(self, new_file, new_rank, piece_range=INFINITY):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)
        rank_squares = abs(delta_rank)
        file_squares = abs(delta_file)
        return (rank_squares == file_squares and
                file_squares <= piece_range and
                not self._is_diagonal_blocked(new_file, new_rank))

    def _is_valid_move(self, new_file, new_rank):
        return False

    def move(self, new_file, new_rank):
        if not self._is_valid_move(new_file, new_rank):
            raise MoveNotAllowed
        self.file = new_file
        self.rank = new_rank
        self.moved = True


class Pawn(Piece):
    SYMBOL = 'P'

    def _is_valid_move(self, new_file, new_rank):
        # A pawn can push two squares forward on first move, otherwise it can
        # only push one square
        piece_range = 1 if self.moved else 2

        # White must march North, Black south
        direction_allowed = NORTH if self.color == WHITE else SOUTH

        return self._is_valid_file_move(new_file, new_rank,
                                        piece_range=piece_range,
                                        direction_allowed=direction_allowed)


class Knight(Piece):
    SYMBOL = 'K'

    def _is_valid_move(self, new_file, new_rank):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        # A knight can move 2 spaces along a rank but must move one space
        # along file or vice versa
        return ((abs(delta_rank) == 2 and abs(delta_file) == 1) or
                (abs(delta_file) == 2 and abs(delta_rank) == 1))


class Bishop(Piece):
    SYMBOL = 'B'

    def _is_valid_move(self, new_file, new_rank):
        return self._is_valid_diagonal_move(new_file, new_rank)


class Rook(Piece):
    SYMBOL = 'R'

    def _is_valid_move(self, new_file, new_rank):
        # A rook must move along a single rank or file
        return (self._is_valid_rank_move(new_file, new_rank) or
                self._is_valid_file_move(new_file, new_rank))


class Queen(Piece):
    SYMBOL = 'Q'
    
    def _is_valid_move(self, new_file, new_rank):
        return (self._is_valid_rank_move(new_file, new_rank) or
                self._is_valid_file_move(new_file, new_rank) or
                self._is_valid_diagonal_move(new_file, new_rank))


class King(Piece):
    SYMBOL = 'K'

    def _is_valid_move(self, new_file, new_rank):
        return (self._is_valid_rank_move(new_file, new_rank, piece_range=1) or
                self._is_valid_file_move(new_file, new_rank, piece_range=1) or
                self._is_valid_diagonal_move(new_file, new_rank, piece_range=1))


class Board(object):
    def __init__(self):
        self.clear()
        self.debug = False

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

    def clear(self):
        self.state = {}
        for file in FILES:
            self.state[file] = {}
            for rank in RANKS:
                self.state[file][rank] = None

        self.captured_pieces = {WHITE: [], BLACK: []}

    def set_piece(self, piece_class, color, file, rank):
        self.check_piece_placement(file, rank)
        piece = piece_class(self, color, file, rank)
        self[file][rank] = piece
        return piece

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
        # Make sure the file is on the board
        if file not in FILES:
            raise NotAValidFile

        # Make sure the rank is on the board
        if rank not in RANKS:
            raise NotAValidRank

    def move_piece(self, file, rank, new_file, new_rank):
        self.check_piece_placement(file, rank)

        # Make sure we're not moving to the same square
        if file == new_file and rank == new_rank:
            raise CannotMoveToSameSquare

        piece = self[file][rank]

        if not piece:
            raise NoPieceThere

        # Make sure we're not moving to square occupied by our own piece
        piece_on_dest_square = self[new_file][new_rank]
        if piece_on_dest_square:
            if piece_on_dest_square.color == piece.color:
                raise CannotMoveToOccupiedSquare
            else:
                self.captured_pieces[piece.color].append(piece_on_dest_square)

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

    def test_cannot_move_to_occupied_square(self):
        self.board.set_piece(Rook, WHITE, 'a', 1)
        self.board.set_piece(Pawn, WHITE, 'a', 2)
        with self.assertRaises(CannotMoveToOccupiedSquare):
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

    def test_disallow_two_square_north(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'b', 4)

    def test_disallow_two_square_east(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'd', 2)

    def test_disallow_two_square_north_east(self):
        with self.assertRaises(MoveNotAllowed):
            self.board.move_piece('b', 2, 'd', 4)


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


if __name__ == '__main__':
    unittest.main()
