def can_knight_move(board,x1,y1,x2,y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if((dx == 2 and dy == 1) or (dx==1 and dy==2)):
        return True
    else:
        return False

def can_king_move(board,x1,y1,x2,y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if(((dx == 1 and dy == 0) or (dy == 1 and dx == 0)) or (dx ==1 and dy ==1)):
        return True
    else:
        return False

def can_rook_move(board,x1,y1,x2,y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if not ((dx == 0 and dy in range(1,8)) or (dy == 0 and dx in range(1,8))):
        return False

    #Direction
    step_x =0 if dx == 0 else (1 if x2 > x1 else -1)
    step_y =0 if dy == 0 else (1 if y2 > y1 else -1)

     # Check for obstacles
    current_x = x1 + step_x
    current_y = y1 + step_y
    
    while (current_x, current_y) != (x2, y2):
        if board[current_y][current_x] != '.':
            return False
        current_x += step_x
        current_y += step_y

    return True


def can_bishop_move(board, x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Diagonal
    if not (dx == dy and dx in range(1, 8)):
        return False
    
    # Calculate direction separately for x and y
    step_x = 1 if x2 > x1 else -1
    step_y = 1 if y2 > y1 else -1
    
    # Check for obstacles
    current_x = x1 + step_x
    current_y = y1 + step_y
    
    while (current_x, current_y) != (x2, y2):
        if board[current_y][current_x] != '.':
            return False
        current_x += step_x
        current_y += step_y
    
    return True

def can_queen_move(board, x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Check if it's a valid queen move (diagonal OR straight line)
    if not ((dx == dy and dx in range(1, 8)) or ((dx == 0 and dy in range(1,8)) or (dy == 0 and dx in range(1,8)))):
        return False
    
    # Calculate direction separately for x and y (handle straight lines)
    step_x = 0 if x1 == x2 else (1 if x2 > x1 else -1)
    step_y = 0 if y1 == y2 else (1 if y2 > y1 else -1)
    
    # Check for obstacles
    current_x = x1 + step_x
    current_y = y1 + step_y
    
    while (current_x, current_y) != (x2, y2):
        if board[current_y][current_x] != '.':
            return False
        current_x += step_x
        current_y += step_y
    
    return True

def can_pawn_move(board, x1, y1, x2, y2, current_turn):
    dx = x2 - x1          # Signed! (not absolute)
    dy = y2 - y1          # Signed! (not absolute)
    piece = board[y1][x1]
    dest = board[y2][x2]
    
    # Step 1: Determine direction based on color
    # White (lowercase) moves up: dy should be negative
    # Black (uppercase) moves down: dy should be positive
    if piece.islower():  # White pawn
        forward = -1     # Moving up (row decreases)
    else:                # Black pawn
        forward = 1      # Moving down (row increases)
    
    # Step 2: Check the 4 cases
    # Case A: Normal forward move (1 square)
    if dx == 0 and dy == forward:
        if (board[y2][x2] != '.'):
            return False
        else:
            return True
    
    # Case B: First move (2 squares)
    elif dx == 0 and dy == 2 * forward:
        # Check if pawn is on starting row
        start_row = 6 if piece.islower() else 1
        if y1 != start_row:
            return False
        
        # Check if intermediate square is empty
        intermediate_y = y1 + forward
        if board[intermediate_y][x1] != '.':
            return False
        
        # Check if destination is empty
        if dest != '.':
            return False
        
        return True
    
    # Case C: Diagonal capture
    elif abs(dx) == 1 and dy == forward:
        # Destination must have an enemy piece
        if dest == '.':
            return False  # Can't capture empty square
        
        # Check if it's an enemy piece
        if piece.islower():  # White pawn
            if dest.islower():  # Another white piece
                return False
        else:  # Black pawn
            if dest.isupper():  # Another black piece
                return False
        
        return True
        
    
    # Case D: Invalid
    else:
        return False

def promote_pawn(board, x, y, color):
    print("Pawn reached the end! Choose promotion piece:")
    print("q = Queen, r = Rook, b = Bishop, n = Knight")
    
    choice = input("Your choice: ").lower()
    
    # Map choice to piece character
    if color == 'white':
        piece_map = {'q': 'q', 'r': 'r', 'b': 'b', 'n': 'n'}
    else:
        piece_map = {'q': 'Q', 'r': 'R', 'b': 'B', 'n': 'N'}
    
    if choice in piece_map:
        board[y][x] = piece_map[choice]
        print(f"Promoted to {choice.upper()}!")
    else:
        print("Invalid choice, defaulting to Queen")
        board[y][x] = piece_map['q']