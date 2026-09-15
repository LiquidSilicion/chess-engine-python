# Chess Movement Algorithms: A Mathematical Crash Course

## 1. Coordinate System Fundamentals

### Board as a Grid
```
    a  b  c  d  e  f  g  h
   ┌──┬──┬──┬──┬──┬──┬──┬──┐
 8 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 7 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 6 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 5 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 4 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 3 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 2 │  │  │  │  │  │  │  │  │
   ├──┼──┼──┼──┼──┼──┼──┼──┤
 1 │  │  │  │  │  │  │  │  │
   └──┴──┴──┴──┴──┴──┴──┴──┘
```

### Coordinate Transformation
- **Chess notation**: (letter, number) → e.g., (e, 4)
- **Array indices**: (row, col) → e.g., (4, 4)
- **Conversion formula**:
  - `col = letter_to_number(file)` where a=0, b=1, ..., h=7
  - `row = 8 - rank` where rank is 1-8

---

## 2. Distance Metrics in Chess

Different pieces use different distance calculations:

### Manhattan Distance (for Rooks)
```
D_manhattan = |x₂ - x₁| + |y₂ - y₁|
```
- Measures horizontal + vertical distance
- Used for: Rook movement (must be on same rank/file)
- Example: e4 to e6 → |4-4| + |6-4| = 0 + 2 = 2

### Chebyshev Distance (for Kings)
```
D_chebyshev = max(|x₂ - x₁|, |y₂ - y₁|)
```
- Measures maximum of horizontal/vertical distance
- Used for: King movement (one square any direction)
- Example: e4 to f5 → max(|5-4|, |5-4|) = max(1, 1) = 1

### Euclidean Distance (for general distance)
```
D_euclidean = √((x₂ - x₁)² + (y₂ - y₁)²)
```
- Straight-line distance
- Used for: General position analysis
- Example: e4 to f6 → √((5-4)² + (6-4)²) = √(1+4) = √5 ≈ 2.24

---

## 3. Direction Vectors

### Concept
A direction vector represents movement as (Δx, Δy):
- Δx = change in column (horizontal)
- Δy = change in row (vertical)

### Piece Direction Sets

**King (8 directions):**
```
(-1,-1), (0,-1), (1,-1)
(-1, 0),        (1, 0)
(-1, 1), (0, 1), (1, 1)
```

**Knight (8 L-shapes):**
```
(-2,-1), (-2, 1)
(-1,-2), (-1, 2)
( 1,-2), ( 1, 2)
( 2,-1), ( 2, 1)
```

**Rook (4 directions, unlimited distance):**
```
(0, -1), (0, 1)  # Vertical
(-1, 0), (1, 0)  # Horizontal
```

**Bishop (4 directions, unlimited distance):**
```
(-1,-1), (-1, 1)
( 1,-1), ( 1, 1)
```

**Queen (8 directions, unlimited distance):**
- Combination of Rook + Bishop

---

## 4. Movement Validation Algorithms

### Algorithm 1: Fixed-Distance Movement (King, Knight)

**Concept:** Check if the move matches a predefined set of valid vectors.

**Steps:**
1. Calculate the displacement: (dx, dy) = (x₂-x₁, y₂-y₁)
2. Check if (dx, dy) is in the set of valid moves for that piece
3. Return True if found, False otherwise

**Knight Example:**
```
Valid moves = {(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)}
Move from (4,4) to (5,6):
  dx = 5-4 = 1
  dy = 6-4 = 2
  Is (1,2) in valid moves? YES ✓
```

**Mathematical Shortcut for Knights:**
```
Valid if: (|dx| = 2 AND |dy| = 1) OR (|dx| = 1 AND |dy| = 2)
```

### Algorithm 2: Line-of-Sight Movement (Rook, Bishop, Queen)

**Concept:** Movement must follow a straight line with no obstacles.

**Steps:**
1. Calculate displacement: (dx, dy) = (x₂-x₁, y₂-y₁)
2. Determine direction vector (unit vector):
   - If dx ≠ 0: dir_x = dx/|dx| (gives -1 or 1)
   - If dy ≠ 0: dir_y = dy/|dy| (gives -1 or 1)
3. Check if direction is valid for the piece
4. Check path for obstacles:
   - Step from (x₁, y₁) to (x₂, y₂) using direction vector
   - At each intermediate square, check if occupied
5. Return True if path is clear, False otherwise

**Rook Example:**
```
Move from e4 (4,4) to e7 (4,7):
  dx = 4-4 = 0
  dy = 7-4 = 3
  Direction: (0, 1) - vertical movement ✓
  Path check: (4,5), (4,6) must be empty
```

**Bishop Example:**
```
Move from e4 (4,4) to g6 (6,6):
  dx = 6-4 = 2
  dy = 6-4 = 2
  Direction: (1, 1) - diagonal movement ✓
  Path check: (5,5) must be empty
```

### Algorithm 3: Pawn Movement (Special Case)

**Concept:** Pawns have asymmetric movement (forward only, diagonal capture).

**Rules:**
1. **Normal move:** Forward 1 square (if empty)
2. **First move:** Forward 2 squares (if both squares empty)
3. **Capture:** Diagonally forward 1 square (must have enemy piece)
4. **En passant:** Special diagonal capture (complex rules)

**Mathematical Representation:**
```
White pawn at (x, y):
  Normal move: (x, y-1) if empty
  First move: (x, y-2) if (x, y-1) and (x, y-2) both empty
  Capture: (x-1, y-1) or (x+1, y-1) if enemy piece present

Black pawn at (x, y):
  Normal move: (x, y+1) if empty
  First move: (x, y+2) if (x, y+1) and (x, y+2) both empty
  Capture: (x-1, y+1) or (x+1, y+1) if enemy piece present
```

---

## 5. Path Obstruction Checking

### The Ray-Casting Algorithm

**Concept:** Check all squares between start and end for obstacles.

**Steps:**
1. Calculate step size:
   - step_x = sign(x₂ - x₁) → -1, 0, or 1
   - step_y = sign(y₂ - y₁) → -1, 0, or 1
2. Start at (x₁ + step_x, y₁ + step_y)
3. Loop until reaching (x₂, y₂):
   - Check if current square is occupied
   - If occupied → path blocked, return False
   - Move to next square: (x + step_x, y + step_y)
4. Return True (path is clear)

**Example: Rook from e4 to e7**
```
Start: (4, 4)
End: (4, 7)
Step: (0, 1)

Check squares:
  (4, 5) - empty? 
  (4, 6) - empty?
  (4, 7) - destination (don't check)
```

---

## 6. Boundary Checking

### Board Edge Validation

**Concept:** All moves must stay within the 8×8 board.

**Formula:**
```
Valid if: 0 ≤ x ≤ 7 AND 0 ≤ y ≤ 7
```

**Example:**
```
Knight at a1 (0, 7) trying to move to:
  (-2, 6) → Invalid (x < 0)
  (2, 6) → Valid ✓
```

---

## 7. Advanced: Attack Detection

### Checking if a Square is Under Attack

**Concept:** Determine if any enemy piece can reach a target square.

**Algorithm:**
1. For each enemy piece on the board:
2. Calculate if it can move to the target square (using piece-specific algorithm)
3. If any piece can reach it → square is under attack

**Optimization:** Instead of checking all pieces, work backwards:
- For each piece type, calculate which squares could attack the target
- Check if an enemy piece of that type is on any of those squares

**Example: Is e4 under attack by enemy knights?**
```
Calculate all squares that could attack e4:
  (2,3), (2,5), (3,2), (3,6), (5,2), (5,6), (6,3), (6,5)
Check if any enemy knight is on these squares
```

---

## 8. Mathematical Patterns

### Diagonal Detection
```
Two squares are on the same diagonal if:
  |x₂ - x₁| = |y₂ - y₁|
```

### Same Row/Column Detection
```
Same row: y₁ = y₂
Same column: x₁ = x₂
```

### Knight Move Pattern
```
A move is a knight move if:
  {|dx|, |dy|} = {1, 2}
```

---

## 9. Implementation Strategy

### Modular Design
```
Piece Movement Validation
├── Boundary Check (all pieces)
├── Piece-Specific Movement
│   ├── Fixed-Distance (King, Knight)
│   ├── Line-of-Sight (Rook, Bishop, Queen)
│   └── Special Rules (Pawn)
├── Path Obstruction Check (Rook, Bishop, Queen, Pawn)
└── Capture Validation (Pawn diagonal capture)
```

### Order of Checks
1. **Boundary check** (fastest, rejects obviously invalid moves)
2. **Piece movement pattern** (validates the move shape)
3. **Path obstruction** (checks for blocking pieces)
4. **Capture rules** (validates if capture is legal)

---

## 10. Performance Considerations

### Early Exit Strategy
```
if not boundary_check(x, y):
    return False  # Reject immediately
if not piece_pattern_check(...):
    return False  # Reject before expensive path check
if not path_clear(...):
    return False
return True
```

### Precomputed Move Tables
For knights and kings, precompute all valid moves from each square:
```
knight_moves[e4] = [(c3, c5, d2, d6, f2, f6, g3, g5)]
```
- Lookup is O(1) instead of calculating
- Uses more memory but much faster

---

## Summary Table

| Piece | Distance Type | Direction Set | Path Check | Special Rules |
|-------|--------------|---------------|------------|---------------|
| King | Chebyshev = 1 | 8 directions | No | Castling |
| Knight | L-shape pattern | 8 L-shapes | No (jumps) | - |
| Rook | Manhattan | 4 cardinal | Yes | Castling |
| Bishop | Diagonal | 4 diagonals | Yes | - |
| Queen | Euclidean | 8 directions | Yes | - |
| Pawn | Asymmetric | Forward/diagonal | Yes | En passant, promotion |

---

## Key Takeaways

1. **Coordinate transformation** is the foundation
2. **Distance metrics** determine which pieces can reach which squares
3. **Direction vectors** define movement patterns
4. **Path checking** prevents pieces from jumping (except knights)
5. **Boundary validation** keeps everything on the board
6. **Modular design** makes code maintainable and testable
