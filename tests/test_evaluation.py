"""Tests for evaluation module."""
import chess
from src.evaluation import evaluate_board


def test_starting_position():
    """Starting position should be roughly equal."""
    board = chess.Board()
    score = evaluate_board(board)
    assert abs(score) < 100  # Should be near 0


def test_white_up_material():
    """White with extra queen should have big advantage."""
    board = chess.Board("rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    score = evaluate_board(board)
    assert score > 0


def test_checkmate_detection():
    """Checkmate should return extreme score."""
    # Fool's mate position
    board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
    score = evaluate_board(board)
    assert score == -99999  # White is checkmated