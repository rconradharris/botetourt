from botetourt.consts import WHITE, BLACK, FILES, RANKS
from botetourt.exc import MoveNotAllowed 

INFINITY = 999


class Piece(object):
    def __init__(self, board, color, file, rank):
        self.board = board
        self.color = color
        self.file = file
        self.rank = rank
        self.moved = False

    def __eq__(self, piece):
        """This equality allows us to compare two separate piece instances and
        determine if they are 'meaningfully' the same, e.g. same board
        position, color and class.
        """
        return (self.__class__ == piece.__class__ and
                self.color == piece.color and
                self.file == piece.file and
                self.rank == piece.rank)

    @property
    def class_name(self):
        return self.__class__.__name__

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
            for file, rank in zip(file_dir, rank_dir)[1:self.RANGE+1]:
                piece = self.board[file][rank]
                if piece and piece.color == self.color:
                    break
                elif piece and piece.color != self.color:
                    squares.add((file, rank))
                    break
                else:
                    squares.add((file, rank))

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
            files = self._get_files_in_between_inclusive(end_file)[1:self.RANGE+1]
            for file in files:
                piece = self.board[file][self.rank]
                if piece and piece.color == self.color:
                    break
                elif piece and piece.color != self.color:
                    squares.add((file, self.rank))
                    break
                else:
                    squares.add((file, self.rank))

        # Going east
        _traverse_files(FILES[-1])

        # Going west
        _traverse_files(FILES[0])

        return squares

    def _file_squares(self, range=None, can_capture=True):
        """Return all squares attacked along the file by a piece."""
        squares = set()
        if range is None:
            range = self.RANGE

        def _traverse_ranks(end_rank):
            ranks = self._get_ranks_in_between_inclusive(end_rank)[1:range+1]
            for rank in ranks:
                piece = self.board[self.file][rank]
                if piece and piece.color == self.color:
                    break
                elif piece and piece.color != self.color:
                    if can_capture:
                        squares.add((self.file, rank))
                    break
                else:
                    squares.add((self.file, rank))

        # Going north
        if self.OMNIDIRECTIONAL or self.color == WHITE:
            _traverse_ranks(RANKS[-1])

        # Going south
        if self.OMNIDIRECTIONAL or self.color == BLACK:
            _traverse_ranks(RANKS[0])

        return squares

    def _get_ranks_in_between_inclusive(self, new_rank):
        if self.rank < new_rank:
            return RANKS[self.rank-1:new_rank]
        else:
            ranks = RANKS[new_rank-1:self.rank]
            ranks.reverse()
            return ranks

    def _get_files_in_between_inclusive(self, new_file):
        orig_idx = FILES.index(self.file)
        new_idx = FILES.index(new_file)
        if orig_idx < new_idx:
            return FILES[orig_idx:new_idx+1]
        else:
            files = FILES[new_idx:orig_idx+1]
            files.reverse()
            return files

    def _capture(self, piece):
        self.board.captured_pieces[self.color].append(piece)

    def _pre_move_hook(self, new_file, new_rank):
        pass

    def remove(self):
        self.board[self.file][self.rank] = None
        self.file = self.rank = self.board = None

    def move(self, new_file, new_rank):
        if (new_file, new_rank) not in self.legal_moves():
            raise MoveNotAllowed

        other_piece = self.board[new_file][new_rank]
        if other_piece and other_piece.color != self.color:
            self._capture(other_piece)

        self._pre_move_hook(new_file, new_rank)

        self.board[self.file][self.rank] = None

        self.board[new_file][new_rank] = self
        self.file = new_file
        self.rank = new_rank

        self.moved = True

    def attacks(self):
        raise NotImplementedError

    def legal_moves(self):
        return self.attacks()


class Pawn(Piece):
    SYMBOL = 'P'
    RANGE = 1
    OMNIDIRECTIONAL = False

    def attacks(self):
        return self._diagonal_squares()

    def legal_moves(self):
        # A pawn can push two squares forward on first move, otherwise it can
        # only push one square
        range = self.RANGE if self.moved else 2
        return (self._file_squares(range=range, can_capture=False) |
                self._diagonal_squares())


class Knight(Piece):
    SYMBOL = 'N'
    RANGE = None
    OMNIDIRECTIONAL = True
    MOVE_MAP = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def attacks(self):
        squares = set()
        old_file_idx = FILES.index(self.file)
        old_rank_idx = RANKS.index(self.rank)

        def _traverse_knight(file_delta, rank_delta):
            try:
                new_file = FILES[old_file_idx + file_delta]
            except IndexError:
                return
            try:
                new_rank = RANKS[old_rank_idx + rank_delta]
            except IndexError:
                return

            piece = self.board[new_file][new_rank]
            if piece and piece.color == self.color:
                pass
            else:
                squares.add((new_file, new_rank))

        for file_delta, rank_delta in self.MOVE_MAP:
            _traverse_knight(file_delta, rank_delta)

        return squares


class Bishop(Piece):
    SYMBOL = 'B'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return self._diagonal_squares()


class Rook(Piece):
    SYMBOL = 'R'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return self._rank_squares() | self._file_squares()


class Queen(Piece):
    SYMBOL = 'Q'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())


class King(Piece):
    SYMBOL = 'K'
    RANGE = 1
    OMNIDIRECTIONAL = True

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())

    def _can_castle(self, king_target_file, rook_file, attacked_squares):
        piece = self.board[rook_file][1]

        if not piece:
            return False

        if piece.__class__ != Rook:
            return False

        # King cannot pass through an attacked square
        king_path = {(f, 1) for f in self._get_files_in_between_inclusive(king_target_file)[1:]}
        if king_path & attacked_squares:
            return False

        return not self.moved and not self.in_check()

    def legal_moves(self):
        attacked_squares = self.board.attacked_squares(self.color)

        squares = self.attacks() - attacked_squares

        # King-side castling
        if self._can_castle('g', 'h', attacked_squares):
            squares.add(('g', 1))

        # Queen-side castling
        if self._can_castle('c', 'a', attacked_squares):
            squares.add(('c', 1))

        return squares

    def _pre_move_hook(self, new_file, new_rank):
        if (self.file, self.rank) == ('e', 1):
            if (new_file, new_rank) == ('g', 1):
                # King-side castling so move king-side rook
                self.board['h'][1].move('f', 1)
            elif (new_file, new_rank) == ('c', 1):
                # Queen-side castling so move queen-side rook
                self.board['a'][1].move('d', 1)

    def in_check(self):
        """A king is in check if he is attacked by any of his opponents
        pieces
        """
        return (self.file, self.rank) in self.board.attacked_squares(self.color)
