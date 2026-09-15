"""Board evaluation functions."""
import chess
from .utils import PIECE_VALUES, PIECE_SQUARE_TABLES


def evaluate_board(board: chess.Board) -> int:
    """Evaluate the board from White's perspective.
    
    Positive = White advantage
    Negative = Black advantage
    """
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
            
        value = PIECE_VALUES[piece.piece_type]
        
        # Add positional bonus from piece-square tables
        pst = PIECE_SQUARE_TABLES.get(piece.piece_type)
        if pst:
            # Mirror the table for Black pieces
            idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
            value += pst[idx]
        
        score += value if piece.color == chess.WHITE else -value
    
    return score