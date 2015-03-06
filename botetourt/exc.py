class ChessException(Exception):
    pass

class NoPieceThere(ChessException):
    pass


class MoveNotAllowed(ChessException):
    pass


class NotAValidSquare(MoveNotAllowed):
    pass
