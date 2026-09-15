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

```

## 2. Directory Structure

```text
minimax-chess-engine/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── setup.py
├── .github/
│   └── workflows/
│       └── python-app.yml       # GitHub Actions CI
│
├── src/
│   ├── __init__.py
│   ├── board.py                 # Board wrapper (optional)
│   ├── evaluation.py            # Evaluation functions
│   ├── search.py                # Minimax + alpha-beta
│   ├── engine.py                # Main engine class
│   └── utils.py                 # Helpers (PST tables, etc.)
│
├── tests/
│   ├── __init__.py
│   ├── test_evaluation.py
│   └── test_search.py
│
├── examples/
│   ├── play_vs_engine.py        # Human vs AI
│   ├── engine_vs_engine.py      # AI vs AI
│   └── benchmark.py             # Positions/sec benchmark
│
├── data/                        # For future SCNN dataset
│   └── .gitkeep
│
├── docs/
│   ├── ALGORITHM.md             # How minimax works
│   └── EVALUATION.md            # How the eval function works
│
└── assets/
    └── demo.gif                 # Screenshot/gif of gameplay
```

---

## 📁 Project Structure

```
src/
├── evaluation.py   # Board scoring (material + PST)
├── search.py       # Minimax + alpha-beta
└── engine.py       # Main engine interface
```

## 🧠 Algorithm

The engine uses:
- **Minimax** with **alpha-beta pruning** to search the game tree
- **Material evaluation** (piece values)
- **Piece-square tables** for positional awareness

See [docs/ALGORITHM.md](docs/ALGORITHM.md) for details.

## 📊 Performance

| Depth | Avg Time/Move | Positions/sec |
|-------|---------------|---------------|
| 2     | ~0.1s         | ~500          |
| 3     | ~1.5s         | ~200          |
| 4     | ~15s          | ~50           |

