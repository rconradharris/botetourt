from botetourt.consts import WHITE, BLACK, FILES, RANKS, INFINITY
from botetourt.exc import MoveNotAllowed 


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

    def _attack_vector(self, files, ranks, range=None, can_capture=True):
        """A vector pointing away from a piece in all of the direction which
        it attacks.

        The vectors length is given by the pieces `RANGE`, and the direction
        is given by the piece's class.

        A bishop will have four attack vectors in the middle of the board: NE,
        SE, SW, and NW.
        """
        if range is None:
            range = self.RANGE

        vector = []
        for file, rank in zip(files, ranks)[1:range+1]:
            piece = self.board[file][rank]

            # If piece is opposite color and we can't capture it, don't
            # add the square
            if not (piece and piece.color != self.color and not can_capture):
                vector.append((file, rank))

            if piece:
                break

        return vector

    def _attack_vectors(self, directions, range=None, can_capture=True):
        """Return the attack vectors given a set of directions.

        `directions` is a set of compass directions (e.g. N, NE, E, etc.) that
        describe along which rank, files, and diagonals a piece attacks.
        """
        vectors = []

        def add_vector(file, rank):
            vectors.append(self._attack_vector(file, rank, range=range,
                                               can_capture=can_capture))

        east = self._get_files_in_between_inclusive(FILES[-1])
        west = self._get_files_in_between_inclusive(FILES[0])
        north = self._get_ranks_in_between_inclusive(RANKS[-1])
        south = self._get_ranks_in_between_inclusive(RANKS[0])
        const_ranks = [self.rank] * len(RANKS)
        const_files = [self.file] * len(RANKS)

        if 'E' in directions:
           add_vector(east, const_ranks)
        if 'W' in directions:
           add_vector(west, const_ranks)
        if 'NE' in directions:
           add_vector(east, north)
        if 'NW' in directions:
           add_vector(west, north)
        if 'SE' in directions:
           add_vector(east, south)
        if 'SW' in directions:
           add_vector(west, south)
        if 'N' in directions:
           add_vector(const_files, north)
        if 'S' in directions:
           add_vector(const_files, south)

        return vectors

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
        if (new_file, new_rank) not in self.get_legal_moves():
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

    def get_attack_vector_directions(self):
        raise NotImplementedError

    def get_attack_vectors(self):
        """Return all attack vectors for this piece."""
        directions = self.get_attack_vector_directions()
        return self._attack_vectors(directions)

    def get_squares_this_piece_attacks(self):
        """Return all squares attacked by this piece as a set."""
        vectors = self.get_attack_vectors()
        return {sq for v in vectors for sq in v}

    def get_legal_moves(self):
        attacks = self.get_squares_this_piece_attacks()
        occupied = self.board.occupied_squares(self.color)
        return attacks - occupied

    def _get_vectors_attacking_this_piece(self, exclude_knights=False):
        vectors = []
        for piece in self.board.get_pieces_by_opposite_color(self.color):
            if piece.__class__ == Knight and exclude_knights:
                continue
            vectors = piece.get_attack_vectors()
            for vector in vectors:
                if (self.file, self.rank) in vector:
                    yield vector

    def _can_interpose_upon_attack(self):
        """Determine whether there is a piece of our color that can interpose
        upon an attack on us.
        """
        legal_moves = set()
        for piece in self.board.get_pieces_by_color(self.color):
            legal_moves |= piece.get_legal_moves()

        # Can't interpose between a knight and another piece (it jumps...)
        for vector in self._get_vectors_attacking_this_piece(exclude_knights=True):
            if set(vector) & legal_moves:
                return True

        return False


class Pawn(Piece):
    SYMBOL = 'P'
    RANGE = 1

    def get_attack_vector_directions(self):
        return ['NE', 'NW'] if self.color == WHITE else ['SE', 'SW']

    def get_legal_moves(self):
        # A pawn can push two squares forward on first move, otherwise it can
        # only push one square
        range = self.RANGE if self.moved else 2

        if self.color == WHITE:
            file_vector = self._attack_vectors(
                    ['N'], range=range, can_capture=False)[0]
        else:
            file_vector = self._attack_vectors(
                    ['S'], range=range, can_capture=False)[0]

        file_squares = {sq for sq in file_vector}
        return super(Pawn, self).get_legal_moves() | file_squares


class Knight(Piece):
    SYMBOL = 'N'
    RANGE = None
    MOVE_MAP = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def get_attack_vectors(self):
        vectors = []
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
                vector = [(new_file, new_rank)]
                vectors.append(vector)

        for file_delta, rank_delta in self.MOVE_MAP:
            _traverse_knight(file_delta, rank_delta)

        return vectors


class Bishop(Piece):
    SYMBOL = 'B'
    RANGE = INFINITY

    def get_attack_vector_directions(self):
        return ['NE', 'SE', 'SW', 'NW']


class Rook(Piece):
    SYMBOL = 'R'
    RANGE = INFINITY

    def get_attack_vector_directions(self):
        return ['N', 'E', 'S', 'W']


class Queen(Piece):
    SYMBOL = 'Q'
    RANGE = INFINITY

    def get_attack_vector_directions(self):
        return ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


class King(Piece):
    SYMBOL = 'K'
    RANGE = 1

    def get_attack_vector_directions(self):
        return ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def _can_castle(self, king_target_file, rook_file):
        attacked_squares = self.board.attacked_squares(self.color)

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

    def can_castle_king_side(self):
        return self._can_castle('g', 'h')

    def can_castle_queen_side(self):
        return self._can_castle('c', 'a')

    def get_legal_moves(self):
        attacked_squares = self.board.attacked_squares(self.color)
        castle_squares = set()

        # King-side castling
        if self.can_castle_king_side():
            castle_squares.add(('g', 1))

        # Queen-side castling
        if self.can_castle_queen_side():
            castle_squares.add(('c', 1))

        return super(King, self).get_legal_moves() - attacked_squares | castle_squares

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

    def is_checkmated(self):
        return (self.in_check() and not
                self.get_legal_moves() and not
                self._can_interpose_upon_attack())
