from pieces import can_bishop_move, can_king_move, can_knight_move, can_queen_move, can_rook_move, can_pawn_move

def is_square_attacked(board, x, y, attacker_color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '.':
                continue
            
            is_attacker = (attacker_color == 'white' and piece.islower()) or \
                          (attacker_color == 'black' and piece.isupper())
            if not is_attacker:
                continue
            
            piece_type = piece.lower()
            
            if piece_type == 'p':
                if piece.islower():
                    attack_row = row - 1
                else:
                    attack_row = row + 1
                
                if y == attack_row and abs(x - col) == 1:
                    return True
            elif piece_type == 'n':
                if can_knight_move(board, col, row, x, y):
                    return True
            elif piece_type == 'k':
                if can_king_move(board, col, row, x, y):
                    return True
            elif piece_type == 'r':
                if can_rook_move(board, col, row, x, y):
                    return True
            elif piece_type == 'b':
                if can_bishop_move(board, col, row, x, y):
                    return True
            elif piece_type == 'q':
                if can_queen_move(board, col, row, x, y):
                    return True
    
    return False

def is_in_check(board, color):
    king_char = 'k' if color == 'white' else 'K'
    king_x, king_y = None, None
    
    for row in range(8):
        for col in range(8):
            if board[row][col] == king_char:
                king_x = col
                king_y = row
                break
        if king_x is not None:
            break
    
    if king_x is None:
        return False

    opponent = 'black' if color == 'white' else 'white'
    return is_square_attacked(board, king_x, king_y, opponent)

def is_valid_piece_move(piece, board, col, row, dest_col, dest_row, color):
    piece_type = piece.lower()
    
    if piece_type == 'n':
        return can_knight_move(board, col, row, dest_col, dest_row)
    elif piece_type == 'k':
        return can_king_move(board, col, row, dest_col, dest_row)
    elif piece_type == 'r':
        return can_rook_move(board, col, row, dest_col, dest_row)
    elif piece_type == 'q':
        return can_queen_move(board, col, row, dest_col, dest_row)
    elif piece_type == 'b':
        return can_bishop_move(board, col, row, dest_col, dest_row)
    elif piece_type == 'p':
        return can_pawn_move(board, col, row, dest_col, dest_row, color)
    
    return False

def get_all_legal_moves(board, color):
    legal_moves = []
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '.':
                continue
            
            is_mine = (color == 'white' and piece.islower()) or \
                      (color == 'black' and piece.isupper())
            if not is_mine:
                continue
            
            for dest_row in range(8):
                for dest_col in range(8):
                    if col == dest_col and row == dest_row:
                        continue
                    
                    if is_valid_piece_move(piece, board, col, row, dest_col, dest_row, color):
                        dest_piece = board[dest_row][dest_col]
                        if dest_piece != '.':
                            dest_is_mine = (color == 'white' and dest_piece.islower()) or \
                                          (color == 'black' and dest_piece.isupper())
                            if dest_is_mine:
                                continue
                        
                        saved_start = board[row][col]
                        saved_dest = board[dest_row][dest_col]
                        
                        board[dest_row][dest_col] = piece
                        board[row][col] = '.'
                        
                        if not is_in_check(board, color):
                            legal_moves.append((col, row, dest_col, dest_row))
                        
                        board[row][col] = saved_start
                        board[dest_row][dest_col] = saved_dest
    
    return legal_moves

def is_checkmate(board, color):
    if not is_in_check(board, color):
        return False
    
    legal_moves = get_all_legal_moves(board, color)
    return len(legal_moves) == 0

def is_stalemate(board, color):
    if is_in_check(board, color):
        return False
    
    legal_moves = get_all_legal_moves(board, color)
    return len(legal_moves) == 0

# ==================== DRAW CONDITIONS ====================

def is_insufficient_material(board):
    """Check if neither side has enough material to checkmate"""
    white_pieces = []
    black_pieces = []
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '.':
                continue
            if piece.islower():
                white_pieces.append(piece)
            else:
                black_pieces.append(piece)
    
    # Remove kings
    white_pieces = [p for p in white_pieces if p != 'k']
    black_pieces = [p for p in black_pieces if p != 'K']
    
    # If either side has pieces other than knights/bishops, there's enough material
    for piece in white_pieces:
        if piece not in ['n', 'b']:
            return False
    
    for piece in black_pieces:
        if piece not in ['N', 'B']:
            return False
    
    # King vs King
    if len(white_pieces) == 0 and len(black_pieces) == 0:
        return True
    
    # King + minor piece vs King
    if len(white_pieces) == 0 and len(black_pieces) == 1:
        return True
    if len(black_pieces) == 0 and len(white_pieces) == 1:
        return True
    
    # King + Bishop vs King + Bishop (same color bishops)
    if len(white_pieces) == 1 and len(black_pieces) == 1:
        if white_pieces[0] == 'b' and black_pieces[0] == 'B':
            white_bishop_pos = None
            black_bishop_pos = None
            for row in range(8):
                for col in range(8):
                    if board[row][col] == 'b':
                        white_bishop_pos = (col, row)
                    elif board[row][col] == 'B':
                        black_bishop_pos = (col, row)
            
            if white_bishop_pos and black_bishop_pos:
                white_color = (white_bishop_pos[0] + white_bishop_pos[1]) % 2
                black_color = (black_bishop_pos[0] + black_bishop_pos[1]) % 2
                if white_color == black_color:
                    return True
    
    return False

def get_board_hash(board, current_turn):
    """Create a hash of the board position for repetition detection"""
    board_str = ""
    for row in board:
        board_str += "".join(row)
    board_str += current_turn
    return hash(board_str)

def is_threefold_repetition(position_history):
    """Check if the current position has occurred 3 times"""
    if len(position_history) < 3:
        return False
    
    current_position = position_history[-1]
    count = position_history.count(current_position)
    
    return count >= 3

def is_50_move_rule(fifty_move_counter):
    """Check if 50 moves have passed without pawn move or capture"""
    return fifty_move_counter >= 100  # 100 half-moves = 50 full moves