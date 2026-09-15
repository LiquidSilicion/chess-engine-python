"""Main chess engine interface."""
import chess
from .search import get_best_move
from .evaluation import evaluate_board


class ChessEngine:
    """A simple minimax chess engine."""
    
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.board = chess.Board()
        self.nodes_searched = 0
    
    def get_move(self) -> chess.Move:
        """Get the engine's best move."""
        return get_best_move(self.board, self.depth)
    
    def evaluate(self) -> int:
        """Get current board evaluation."""
        return evaluate_board(self.board)
    
    def make_move(self, move: str) -> bool:
        """Make a move in UCI format (e.g., 'e2e4')."""
        try:
            self.board.push_uci(move)
            return True
        except ValueError:
            return False
    
    def reset(self):
        """Reset the board to starting position."""
        self.board = chess.Board()
        self.nodes_searched = 0