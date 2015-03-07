from botetourt.board import WHITE, BLACK, FILES, RANKS
from botetourt.exc import MoveNotAllowed 

INFINITY = 999


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

    def _file_squares(self):
        """Return all squares attacked along the file by a piece."""
        squares = set()

        def _traverse_ranks(end_rank):
            ranks = self._get_ranks_in_between_inclusive(end_rank)[1:self.RANGE+1]
            for rank in ranks:
                piece = self.board[self.file][rank]
                if piece and piece.color == self.color:
                    break
                elif piece and piece.color != self.color:
                    squares.add((self.file, rank))
                    break
                else:
                    squares.add((self.file, rank))

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

        #if piece_on_dest_square and piece_on_dest_square.color == self.color:
        #    raise MoveNotAllowed

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
    SYMBOL = 'N'
    RANGE = None
    OMNIDIRECTIONAL = True

    def _is_valid_move(self, new_file, new_rank):
        delta_file, delta_rank = self._delta_file_rank(new_file, new_rank)

        # A knight can move 2 spaces along a rank but must move one space
        # along file or vice versa
        return ((abs(delta_rank) == 2 and abs(delta_file) == 1) or
                (abs(delta_file) == 2 and abs(delta_rank) == 1))


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
            squares.add((new_file, new_rank))

        _traverse_knight(2, 1)
        _traverse_knight(1, 2)
        _traverse_knight(-1, 2)
        _traverse_knight(-2, 1)
        _traverse_knight(-2, -1)
        _traverse_knight(-1, -2)
        _traverse_knight(1, -2)
        _traverse_knight(2, -1)

        return squares


class Bishop(Piece):
    SYMBOL = 'B'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return self._diagonal_squares()

    def legal_moves(self):
        return self.attacks()

    def _is_valid_move(self, new_file, new_rank):
        return (new_file, new_rank) in self.legal_moves()


class Rook(Piece):
    SYMBOL = 'R'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return self._rank_squares() | self._file_squares()

    def legal_moves(self):
        return self.attacks()

    def _is_valid_move(self, new_file, new_rank):
        return (new_file, new_rank) in self.legal_moves()



class Queen(Piece):
    SYMBOL = 'Q'
    RANGE = INFINITY
    OMNIDIRECTIONAL = True

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())

    def legal_moves(self):
        return self.attacks()

    def _is_valid_move(self, new_file, new_rank):
        return (new_file, new_rank) in self.legal_moves()


class King(Piece):
    SYMBOL = 'K'
    RANGE = 1
    OMNIDIRECTIONAL = True

    def attacks(self):
        return (self._rank_squares() |
                self._file_squares() |
                self._diagonal_squares())

    def legal_moves(self):
        return self.attacks() - self.board.attacked_squares(self.color)

    def _is_valid_move(self, new_file, new_rank):
        return (new_file, new_rank) in self.legal_moves()

    def in_check(self):
        """A king is in check if he is attacked by any of his opponents
        pieces
        """
        return (self.file, self.rank) in self.board.attacked_squares(self.color)
