import unittest

# Consts
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = [1, 2, 3, 4, 5, 6, 7, 8]
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


class NotAValidSquare(MoveNotAllowed):
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

    def _diagonal_squares(self):
        """Return all squares attacked along the diagonals by a piece."""
        squares = set()

        easterly = self._get_files_in_between_inclusive(FILES[-1])
        westerly = self._get_files_in_between_inclusive(FILES[0])
        northerly = self._get_ranks_in_between_inclusive(RANKS[-1])
        southerly = self._get_ranks_in_between_inclusive(RANKS[0])

        def _traverse_diag(file_dir, rank_dir):
            for file, rank in zip(file_dir, rank_dir)[:self.RANGE+1]:
                squares.add((file, rank))
                if file != self.file and rank != self.rank and self.board[file][rank]:
                    break

        # Pawns are not omnidirection and therefore must atack north if white,
        # or south if black
        if self.OMNIDIRECTIONAL or self.color == WHITE:
            # Going north east
            _traverse_diag(easterly, northerly)

            # Going north west
            _traverse_diag(westerly, northerly)

        if self.OMNIDIRECTIONAL or self.color == BLACK:
            # Going south east
            _traverse_diag(easterly, southerly)

            # Going south west
            _traverse_diag(westerly, southerly)

        return squares

    def _rank_squares(self):
        """Return all squares attacked along the rank by a piece."""
        squares = set()

        def _traverse_files(end_file):
            files = self._get_files_in_between_inclusive(end_file)[:self.RANGE+1]
            for file in files:
                squares.add((file, self.rank))
                if file != self.file and self.board[file][self.rank]:
                    break

        # Going east
        _traverse_files(FILES[-1])

        # Going west
        _traverse_files(FILES[0])

        return squares

    def _file_squares(self):
        """Return all squares attacked along the file by a piece."""
        squares = set()

        def _traverse_ranks(end_rank):
            ranks = self._get_ranks_in_between_inclusive(end_rank)[:self.RANGE+1]
            for rank in ranks:
                squares.add((self.file, rank))
                if rank != self.rank and self.board[self.file][rank]:
                    break

        # Going north
        _traverse_ranks(RANKS[-1])

        # Going south
        _traverse_ranks(RANKS[0])

        return squares

    def _delta_file_rank(self, new_file, new_rank):
        delta_file = FILES.index(new_file) - FILES.index(self.file)
        delta_rank = new_rank - self.rank
        return delta_file, delta_rank

    def _get_ranks_in_between_inclusive(self, new_rank):
        if self.rank < new_rank:
            return RANKS[self.rank-1:new_rank]
        else:
            ranks = RANKS[new_rank-1:self.rank]
            ranks.reverse()
            return ranks

    def _get_ranks_in_between_exclusive(self, new_rank):
        return self._get_ranks_in_between_inclusive(new_rank)[1:-1]

    def _is_file_blocked(self, new_rank):
        ranks_in_between = self._get_ranks_in_between_exclusive(new_rank)

        for rank in ranks_in_between:
            if self.board[self.file][rank]:
                return True

        return False

    def _is_valid_file_move(self, new_file, new_rank, piece_range=None):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        if self.OMNIDIRECTIONAL:
            pass
        elif self.color == WHITE and delta_rank < 0:
            return False
        elif self.color == BLACK and delta_rank > 0:
            return False

        if piece_range is None:
            piece_range = self.RANGE

        return (delta_file == 0 and
                abs(delta_rank) <= piece_range and
                not self._is_file_blocked(new_rank))

    def _get_files_in_between_inclusive(self, new_file):
        orig_idx = FILES.index(self.file)
        new_idx = FILES.index(new_file)
        if orig_idx < new_idx:
            return FILES[orig_idx:new_idx+1]
        else:
            files = FILES[new_idx:orig_idx+1]
            files.reverse()
            return files

    def _get_files_in_between_exclusive(self, new_file):
        return self._get_files_in_between_inclusive(new_file)[1:-1]

    def _is_rank_blocked(self, new_file):
        files_in_between = self._get_files_in_between_exclusive(new_file)

        for file in files_in_between:
            if self.board[file][self.rank]:
                return True

        return False

    def _is_valid_rank_move(self, new_file, new_rank, piece_range=None):
        if piece_range is None:
            piece_range = self.RANGE

        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)
        return (delta_rank == 0 and
                abs(delta_file) <= piece_range and
                not self._is_rank_blocked(new_file))

    def _is_diagonal_blocked(self, new_file, new_rank):
        ranks_in_between = self._get_ranks_in_between_exclusive(new_rank)
        files_in_between = self._get_files_in_between_exclusive(new_file)

        for file, rank in zip(files_in_between, ranks_in_between):
            if self.board[file][rank]:
                return True

        return False

    def _is_valid_diagonal_move(self, new_file, new_rank, piece_range=None):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        if self.OMNIDIRECTIONAL:
            pass
        elif self.color == WHITE and delta_rank < 0:
            return False
        elif self.color == BLACK and delta_rank > 0:
            return False

        if piece_range is None:
            piece_range = self.RANGE
        rank_squares = abs(delta_rank)
        file_squares = abs(delta_file)
        return (rank_squares == file_squares and
                file_squares <= piece_range and
                not self._is_diagonal_blocked(new_file, new_rank))

    def _is_valid_move(self, new_file, new_rank):
        return False

    def _capture(self, piece):
        self.board.captured_pieces[self.color].append(piece)

    def move(self, new_file, new_rank):
        piece_on_dest_square = self.board[new_file][new_rank]

        if piece_on_dest_square and piece_on_dest_square.color == self.color:
            raise CannotMoveToOccupiedSquare

        if not self._is_valid_move(new_file, new_rank):
            raise MoveNotAllowed

        if piece_on_dest_square and piece_on_dest_square.color != self.color:
            self._capture(piece_on_dest_square)

        self.file = new_file
        self.rank = new_rank
        self.moved = True

    def attacks(self):
        raise NotImplementedError


class Pawn(Piece):
    SYMBOL = 'P'
    RANGE = 1
    OMNIDIRECTIONAL = False

    def _is_valid_move(self, new_file, new_rank):
        piece_on_dest_square = self.board[new_file][new_rank]
        if piece_on_dest_square:
            return self._is_valid_diagonal_move(new_file, new_rank)
        else:
            # A pawn can push two squares forward on first move, otherwise it can
            # only push one square
            piece_range = self.RANGE if self.moved else 2

            # A pawn is blocked by a piece in front of it
            return self._is_valid_file_move(new_file, new_rank,
                                            piece_range=piece_range)

    def attacks(self):
        return self._diagonal_squares()


class Knight(Piece):
    SYMBOL = 'K'
    RANGE = None
    OMNIDIRECTIONAL = True

    def _is_valid_move(self, new_file, new_rank):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        # A knight can move 2 spaces along a rank but must move one space
        # along file or vice versa
        return ((abs(delta_rank) == 2 and abs(delta_file) == 1) or
                (abs(delta_file) == 2 and abs(delta_rank) == 1))


class Bishop(Piece):
    SYMBOL = 'B'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def _is_valid_move(self, new_file, new_rank):
        return self._is_valid_diagonal_move(new_file, new_rank)

    def attacks(self):
        return self._diagonal_squares()


class Rook(Piece):
    SYMBOL = 'R'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def _is_valid_move(self, new_file, new_rank):
        # A rook must move along a single rank or file
        return (self._is_valid_rank_move(new_file, new_rank) or
                self._is_valid_file_move(new_file, new_rank))

    def attacks(self):
        return self._rank_squares() | self._file_squares()


class Queen(Piece):
    SYMBOL = 'Q'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True
    
    def _is_valid_move(self, new_file, new_rank):
        return (self._is_valid_rank_move(new_file, new_rank) or
                self._is_valid_file_move(new_file, new_rank) or
                self._is_valid_diagonal_move(new_file, new_rank))

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())


class King(Piece):
    SYMBOL = 'K'
    RANGE = 1
    OMNIDIRECTIONAL = True

    def _is_valid_move(self, new_file, new_rank):
        return (self._is_valid_rank_move(new_file, new_rank) or
                self._is_valid_file_move(new_file, new_rank) or
                self._is_valid_diagonal_move(new_file, new_rank))

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())


class Board(object):
    def __init__(self):
        self.clear()

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
        if not self.is_valid_square(file, rank):
            raise NotAValidSquare

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

    def is_valid_square(self, file, rank):
        return file in FILES and rank in RANKS

    def move_piece(self, file, rank, new_file, new_rank):
        if not self.is_valid_square(file, rank):
            raise NotAValidSquare

        # Make sure we're not moving to the same square
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
        with self.assertRaises(NotAValidSquare):
            self.board.set_piece(Pawn, WHITE, 'i', 2)

    def test_invalid_rank(self):
        with self.assertRaises(NotAValidSquare):
            self.board.set_piece(Pawn, WHITE, 'h', 0)

        with self.assertRaises(NotAValidSquare):
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


if __name__ == '__main__':
    unittest.main()
