"""Benchmark engine performance."""
import time
import chess
from src.search import get_best_move


def benchmark(depth=3, num_positions=10):
    """Measure positions evaluated per second."""
    # Use a set of test positions
    positions = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
        "rnbqkb1r/pp1p1ppp/2p5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4",
    ]
    
    total_moves = 0
    start = time.time()
    
    for fen in positions[:num_positions]:
        board = chess.Board(fen)
        move = get_best_move(board, depth)
        total_moves += 1
        print(f"Position: {fen[:30]}... -> {move}")
    
    elapsed = time.time() - start
    print(f"\n⏱️  {total_moves} positions in {elapsed:.2f}s")
    print(f"📊 {total_moves / elapsed:.1f} positions/sec")


if __name__ == "__main__":
    benchmark(depth=3)