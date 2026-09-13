# Minimax Chess Engine

A Python chess engine built from scratch using the Minimax algorithm with Alpha-Beta pruning.

## 🎯 Features

- ✅ Full legal move generation (via `python-chess`)
- ✅ Minimax search with alpha-beta pruning
- ✅ Material + piece-square table evaluation
- ✅ Configurable search depth
- ✅ Human vs AI and AI vs AI modes
- ✅ Performance benchmarking

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/minimax-chess-engine.git
cd minimax-chess-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Play against the engine
python examples/play_vs_engine.py