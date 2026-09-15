from pieces import can_knight_move, can_king_move, can_rook_move, can_bishop_move, can_queen_move, can_pawn_move, promote_pawn
from game_rules import (is_in_check, is_square_attacked, get_all_legal_moves, is_checkmate, 
                        is_stalemate, is_insufficient_material, is_threefold_repetition, 
                        is_50_move_rule, get_board_hash)

#Declarations
board =[['R' ,'N' ,'B' ,'Q' ,'K' ,'B' ,'N' ,'R'],
        ['P' ,'P' ,'P' ,'P' ,'P' ,'P' ,'P' ,'P'],
        ['.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.'],
        ['.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.'],
        ['.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.'],
        ['.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.' ,'.'],
        ['p' ,'p' ,'p' ,'p' ,'p' ,'p' ,'p' ,'p'],
        ['r' , 'n','b' ,'q' ,'k' ,'b' ,'n' ,'r']]

colmn = [' ','a','b','c','d','e','f','g','h']
current_turn = 'white'

#------------------------------------------------------
#Print the board
def print_board(board,c):
    for c in colmn:
        print(*c,end=" ")
    print()
    for rw_idx,row in enumerate(board):
        print(8-rw_idx,*row)

print_board(board,colmn)

#-----------------------------------------------------------------------------------
#CASTLING FUNCTIONS
#-----------------------------------------------------------------------------------

def is_castling_move(piece, x1, y1, x2, y2):
    """Check if this is a castling move (king moves 2 squares horizontally)"""
    if piece.lower() != 'k':
        return False
    
    if abs(x2 - x1) == 2 and y1 == y2:
        return True
    
    return False

def can_castle(board, x1, y1, x2, y2, current_turn, white_kingside, white_queenside, black_kingside, black_queenside):
    """Check if castling is legal"""
    piece = board[y1][x1]
    
    if x2 > x1:
        kingside = True
    else:
        kingside = False
    
    if current_turn == 'white':
        if kingside and not white_kingside:
            return False, "White can't castle kingside (king or rook has moved)"
        if not kingside and not white_queenside:
            return False, "White can't castle queenside (king or rook has moved)"
    else:
        if kingside and not black_kingside:
            return False, "Black can't castle kingside (king or rook has moved)"
        if not kingside and not black_queenside:
            return False, "Black can't castle queenside (king or rook has moved)"
    
    if is_in_check(board, current_turn):
        return False, "Can't castle while in check"
    
    opponent = 'black' if current_turn == 'white' else 'white'
    
    if kingside:
        for x in range(x1 + 1, x2 + 1):
            if board[y1][x] != '.':
                return False, "Path is blocked"
        
        for x in [x1 + 1, x2]:
            if is_square_attacked(board, x, y1, opponent):
                return False, "Square is under attack"
    else:
        for x in range(x2, x1):
            if board[y1][x] != '.':
                return False, "Path is blocked"
        
        for x in [x1 - 1, x2]:
            if is_square_attacked(board, x, y1, opponent):
                return False, "Square is under attack"
    
    return True, ""

def execute_castling(board, x1, y1, x2, y2):
    """Execute castling move (move both king and rook)"""
    board[y2][x2] = board[y1][x1]
    board[y1][x1] = '.'
    
    if x2 > x1:
        rook_x = 7
        new_rook_x = x2 - 1
    else:
        rook_x = 0
        new_rook_x = x2 + 1
    
    board[y2][new_rook_x] = board[y1][rook_x]
    board[y1][rook_x] = '.'

def update_castling_rights(white_kingside, white_queenside, black_kingside, black_queenside, piece, x1, y1, x2, y2):
    """Update castling rights after a move"""
    piece_lower = piece.lower()
    
    if piece_lower == 'k':
        if piece.islower():
            white_kingside = False
            white_queenside = False
        else:
            black_kingside = False
            black_queenside = False
    
    if x1 == 0 and y1 == 7 and piece_lower == 'r':
        white_queenside = False
    if x1 == 7 and y1 == 7 and piece_lower == 'r':
        white_kingside = False
    
    if x1 == 0 and y1 == 0 and piece_lower == 'r':
        black_queenside = False
    if x1 == 7 and y1 == 0 and piece_lower == 'r':
        black_kingside = False
    
    if x2 == 0 and y2 == 7:
        white_queenside = False
    if x2 == 7 and y2 == 7:
        white_kingside = False
    if x2 == 0 and y2 == 0:
        black_queenside = False
    if x2 == 7 and y2 == 0:
        black_kingside = False
    
    return white_kingside, white_queenside, black_kingside, black_queenside

#-----------------------------------------------------------------------------------
#Make move
# Returns: (move_info, wk, wq, bk, bq, captured_piece)
# move_info is None if move failed, or (x1, y1, x2, y2, piece) if successful
def make_move(board, pos_chg, current_turn, last_move, white_kingside, white_queenside, black_kingside, black_queenside):
    col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    coordinates = list(pos_chg)
    x1 = col_map[coordinates[0]]
    y1 = 8 - int(coordinates[1])
    x2 = col_map[coordinates[2]]
    y2 = 8 - int(coordinates[3])
    piece = board[y1][x1]
    
    fail = (None, white_kingside, white_queenside, black_kingside, black_queenside, None)
    
    if piece == ".":
        print("There is nothing to move!")
        return fail
    
    if current_turn == 'white' and not piece.islower():
        print("That's not your piece! You can only move white (lowercase) pieces.")
        return fail
    elif current_turn == 'black' and not piece.isupper():
        print("That's not your piece! You can only move black (uppercase) pieces.")
        return fail

    # === CHECK FOR CASTLING ===
    if is_castling_move(piece, x1, y1, x2, y2):
        can_castle_result, error_msg = can_castle(board, x1, y1, x2, y2, current_turn, 
                                                   white_kingside, white_queenside, 
                                                   black_kingside, black_queenside)
        if not can_castle_result:
            print(f"Invalid castling: {error_msg}")
            return fail
        
        execute_castling(board, x1, y1, x2, y2)
        
        white_kingside, white_queenside, black_kingside, black_queenside = update_castling_rights(
            white_kingside, white_queenside, black_kingside, black_queenside,
            piece, x1, y1, x2, y2
        )
        
        print("Castling!")
        
        opponent = 'black' if current_turn == 'white' else 'white'
        if is_in_check(board, opponent):
            print(f"Check! {opponent}'s king is under attack!")
        
        return (x1, y1, x2, y2, piece), white_kingside, white_queenside, black_kingside, black_queenside, None

    # Check for en passant capture
    is_en_passant = False
    if piece.lower() == "p" and last_move:
        if abs(last_move[1] - last_move[3]) == 2:
            last_piece = last_move[4]
            if last_piece.lower() == 'p':
                if y1 == last_move[3] and abs(x1 - last_move[2]) == 1 and x2 == last_move[2]:
                    is_en_passant = True

    # Check piece-specific movement
    if piece.lower() == "n":
        if not can_knight_move(board, x1, y1, x2, y2):
            print("Invalid knight move!")
            return fail
    elif piece.lower() == "k":
        if not can_king_move(board, x1, y1, x2, y2):
            print("Invalid king move!")
            return fail
    elif piece.lower() == "r":
        if not can_rook_move(board, x1, y1, x2, y2):
            print("Invalid rook move!")
            return fail
    elif piece.lower() == "b":
        if not can_bishop_move(board, x1, y1, x2, y2):
            print("Invalid bishop move!")
            return fail
    elif piece.lower() == "q":
        if not can_queen_move(board, x1, y1, x2, y2):
            print("Invalid queen move!")
            return fail
    elif piece.lower() == "p":
        if not can_pawn_move(board, x1, y1, x2, y2, current_turn) and not is_en_passant:
            print("Invalid pawn move!")
            return fail
    
    # Check if destination has friendly piece (skip for en passant)
    dest_piece = board[y2][x2]
    if dest_piece != '.' and not is_en_passant:
        if current_turn == 'white' and dest_piece.islower():
            print("You can't capture your own piece!")
            return fail
        elif current_turn == 'black' and dest_piece.isupper():
            print("You can't capture your own piece!")
            return fail
    
    # === SAVE STATE FOR POTENTIAL UNDO ===
    saved_dest = board[y2][x2]
    saved_start = board[y1][x1]
    en_passant_captured = None
    en_passant_pos = None
    
    # Make the move temporarily
    board[y2][x2] = piece
    board[y1][x1] = '.'
    
    # Handle en passant capture
    if is_en_passant:
        en_passant_pos = (last_move[3], last_move[2])
        en_passant_captured = board[en_passant_pos[0]][en_passant_pos[1]]
        board[en_passant_pos[0]][en_passant_pos[1]] = '.'
    
    # === CHECK IF THIS MOVE LEAVES YOUR KING IN CHECK ===
    if is_in_check(board, current_turn):
        print("Illegal move! You can't leave your king in check.")
        board[y1][x1] = saved_start
        board[y2][x2] = saved_dest
        if is_en_passant and en_passant_pos:
            board[en_passant_pos[0]][en_passant_pos[1]] = en_passant_captured
        return fail
    
    # === CHECK IF OPPONENT IS NOW IN CHECK ===
    opponent = 'black' if current_turn == 'white' else 'white'
    if is_in_check(board, opponent):
        print(f"Check! {opponent}'s king is under attack!")
    
    # Handle pawn promotion
    if piece.lower() == 'p':
        if piece.islower() and y2 == 0:
            promote_pawn(board, x2, y2, 'white')
        elif piece.isupper() and y2 == 7:
            promote_pawn(board, x2, y2, 'black')
    
    # Update castling rights
    white_kingside, white_queenside, black_kingside, black_queenside = update_castling_rights(
        white_kingside, white_queenside, black_kingside, black_queenside,
        piece, x1, y1, x2, y2
    )
    
    # Determine captured piece for 50-move rule tracking
    # For en passant, the captured pawn is en_passant_captured
    # For normal moves, it's saved_dest
    if is_en_passant:
        captured_piece = en_passant_captured
    else:
        captured_piece = saved_dest
    
    return (x1, y1, x2, y2, piece), white_kingside, white_queenside, black_kingside, black_queenside, captured_piece

#-----------------------------------------------------------------------------------
#Switch Turns
def switch_turn(current_turn):
    return 'black' if current_turn == 'white' else 'white'

#-----------------------------------------------------------------------------------
#MASTER     Play Game
def play_game(board, colmn):
    current_turn = "white"
    last_move = None
    white_kingside = True
    white_queenside = True
    black_kingside = True
    black_queenside = True
    position_history = []
    fifty_move_counter = 0
    
    # Add initial position
    position_history.append(get_board_hash(board, current_turn))
    
    while True:
        print(current_turn, "turn")
        pos_chg = input(str("Enter your next move (in UCI) or exit: "))
        if pos_chg == "exit":
            break
        
        result = make_move(board, pos_chg, current_turn, last_move,
                          white_kingside, white_queenside, black_kingside, black_queenside)
        
        if result[0] is not None:
            last_move = result[0]
            white_kingside = result[1]
            white_queenside = result[2]
            black_kingside = result[3]
            black_queenside = result[4]
            captured_piece = result[5]
            
            # Update 50-move counter
            piece_moved = board[result[0][3]][result[0][2]]
            is_pawn_move = piece_moved.lower() == 'p'
            is_capture = captured_piece is not None and captured_piece != '.'
            
            if is_pawn_move or is_capture:
                fifty_move_counter = 0
            else:
                fifty_move_counter += 1
            
            # Switch turn and track position
            current_turn = switch_turn(current_turn)
            position_history.append(get_board_hash(board, current_turn))
            
            print_board(board, colmn)
            
            # === CHECK FOR GAME END CONDITIONS ===
            opponent = 'black' if current_turn == 'white' else 'white'
            
            if is_checkmate(board, opponent):
                print(f"\n{'='*50}")
                print(f"CHECKMATE! {current_turn.upper()} wins!")
                print(f"{'='*50}")
                break
            elif is_stalemate(board, opponent):
                print(f"\n{'='*50}")
                print(f"STALEMATE! The game is a draw!")
                print(f"{'='*50}")
                break
            elif is_insufficient_material(board):
                print(f"\n{'='*50}")
                print(f"DRAW! Insufficient material to checkmate!")
                print(f"{'='*50}")
                break
            elif is_threefold_repetition(position_history):
                print(f"\n{'='*50}")
                print(f"DRAW! Threefold repetition!")
                print(f"{'='*50}")
                break
            elif is_50_move_rule(fifty_move_counter):
                print(f"\n{'='*50}")
                print(f"DRAW! 50-move rule!")
                print(f"{'='*50}")
                break
        else:
            # Move failed, don't switch turn
            pass
        
        # Only switch turn if move was successful (already done above)
        # But we need to switch for next iteration - wait, we already switched above
        # Let me fix this logic...
        # Actually we switched current_turn above when tracking position,
        # so we need to switch it back for the loop logic
        # Let me restructure this properly

# Fix: Restructure the turn switching
def play_game(board, colmn):
    current_turn = "white"
    last_move = None
    white_kingside = True
    white_queenside = True
    black_kingside = True
    black_queenside = True
    position_history = []
    fifty_move_counter = 0
    
    # Add initial position
    position_history.append(get_board_hash(board, current_turn))
    
    while True:
        print(current_turn, "turn")
        pos_chg = input(str("Enter your next move (in UCI) or exit: "))
        if pos_chg == "exit":
            break
        
        result = make_move(board, pos_chg, current_turn, last_move,
                          white_kingside, white_queenside, black_kingside, black_queenside)
        
        if result[0] is not None:
            last_move = result[0]
            white_kingside = result[1]
            white_queenside = result[2]
            black_kingside = result[3]
            black_queenside = result[4]
            captured_piece = result[5]
            
            # Update 50-move counter
            piece_moved = board[result[0][3]][result[0][2]]
            is_pawn_move = piece_moved.lower() == 'p'
            is_capture = captured_piece is not None and captured_piece != '.'
            
            if is_pawn_move or is_capture:
                fifty_move_counter = 0
            else:
                fifty_move_counter += 1
            
            print_board(board, colmn)
            
            # === CHECK FOR GAME END CONDITIONS ===
            opponent = 'black' if current_turn == 'white' else 'white'
            
            if is_checkmate(board, opponent):
                print(f"\n{'='*50}")
                print(f"CHECKMATE! {current_turn.upper()} wins!")
                print(f"{'='*50}")
                break
            elif is_stalemate(board, opponent):
                print(f"\n{'='*50}")
                print(f"STALEMATE! The game is a draw!")
                print(f"{'='*50}")
                break
            elif is_insufficient_material(board):
                print(f"\n{'='*50}")
                print(f"DRAW! Insufficient material to checkmate!")
                print(f"{'='*50}")
                break
            
            # Track position AFTER the move (from opponent's perspective)
            current_turn = switch_turn(current_turn)
            position_history.append(get_board_hash(board, current_turn))
            
            # Check draw conditions that depend on position history
            if is_threefold_repetition(position_history):
                print(f"\n{'='*50}")
                print(f"DRAW! Threefold repetition!")
                print(f"{'='*50}")
                break
            elif is_50_move_rule(fifty_move_counter):
                print(f"\n{'='*50}")
                print(f"DRAW! 50-move rule!")
                print(f"{'='*50}")
                break
        else:
            # Move failed, don't switch turn - player tries again
            pass

play_game(board, colmn)