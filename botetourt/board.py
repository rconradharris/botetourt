from botetourt.exc import MoveNotAllowed, NoPieceThere
from botetourt.consts import WHITE, BLACK, FILES, RANKS
from botetourt.pieces import Queen, Pawn


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

    def _get_pieces(self):
        for file in FILES:
            for rank in RANKS:
                piece = self.state[file][rank]
                if piece:
                    yield piece

    def _get_pieces_by_color(self, color):
        for piece in self._get_pieces():
            if piece.color == color:
                yield piece

    def clear(self):
        self.state = {}
        for file in FILES:
            self.state[file] = {}
            for rank in RANKS:
                self.state[file][rank] = None

        self.captured_pieces = {WHITE: [], BLACK: []}

    def set_piece(self, piece_class, color, file, rank):
        if not self._is_valid_square(file, rank):
            raise MoveNotAllowed

        piece = piece_class(self, color, file, rank)
        self[file][rank] = piece
        return piece

    def remove_piece(self, file, rank):
        piece = self[file][rank]
        if not piece:
            raise NoPieceThere
        piece.remove()

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

    def _is_valid_square(self, file, rank):
        return file in FILES and rank in RANKS

    def _promote_pawn(self, piece):
        file = piece.file
        rank = piece.rank
        color = piece.color

        piece.remove()

        # FIXME: for now just auto-promoting to queen
        self.set_piece(Queen, color, file, rank)

    def move_piece(self, file, rank, new_file, new_rank):
        if not self._is_valid_square(file, rank):
            raise MoveNotAllowed

        piece = self[file][rank]
        if not piece:
            raise NoPieceThere

        piece.move(new_file, new_rank)

        if piece.__class__ == Pawn:
            if piece.color == WHITE and piece.rank == 8:
                self._promote_pawn(piece)
            elif piece.color == BLACK and piece.rank == 1:
                self._promote_pawn(piece)

    def occupied_squares(self, color):
        """Return all squares occupied by a given color"""
        squares = set()
        for piece in self._get_pieces_by_color(color):
            squares.add((piece.file, piece.rank))
        return squares

    def attacked_squares(self, color):
        """Return all attacked squares for a given color"""
        squares = set()

        opposite_color = BLACK if color == WHITE else WHITE
        for piece in self._get_pieces_by_color(opposite_color):
            squares |= piece.get_squares_this_piece_attacks()

        return squares
