"""Minimax search with alpha-beta pruning."""
import chess
from .evaluation import evaluate_board


def minimax(board: chess.Board, depth: int, alpha: int, beta: int, 
            maximizing: bool) -> int:
    """Recursive minimax with alpha-beta pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board: chess.Board, depth: int = 3) -> chess.Move:
    """Find the best move for the current side to move."""
    best_move = None
    best_eval = float('-inf') if board.turn == chess.WHITE else float('inf')
    maximizing = board.turn == chess.WHITE
    
    for move in board.legal_moves:
        board.push(move)
        eval_score = minimax(board, depth - 1, float('-inf'), float('inf'), 
                             not maximizing)
        board.pop()
        
        if maximizing and eval_score > best_eval:
            best_eval = eval_score
            best_move = move
        elif not maximizing and eval_score < best_eval:
            best_eval = eval_score
            best_move = move
    
    return best_move