"""Play a game against the engine in the terminal."""
import chess
from src.engine import ChessEngine


def main():
    engine = ChessEngine(depth=3)
    print("♟️  Chess Engine - You play White")
    print("Enter moves in UCI format (e.g., 'e2e4')")
    print("Type 'quit' to exit\n")
    
    while not engine.board.is_game_over():
        print(engine.board)
        print(f"Evaluation: {engine.evaluate()}\n")
        
        if engine.board.turn == chess.WHITE:
            move = input("Your move: ").strip()
            if move.lower() == 'quit':
                break
            if not engine.make_move(move):
                print("❌ Invalid move, try again\n")
                continue
        else:
            print("🤖 Engine thinking...")
            best_move = engine.get_move()
            engine.board.push(best_move)
            print(f"Engine plays: {best_move}\n")
    
    print("\n" + "=" * 40)
    print(engine.board)
    print(f"Game over! Result: {engine.board.result()}")


if __name__ == "__main__":
    main()