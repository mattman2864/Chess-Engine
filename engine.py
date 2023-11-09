import random

def find_random_move(valid_moves, gamestate):
    move = random.choice(valid_moves)
    return move

def blind_take(valid_moves, gamestate):
    
    for move in valid_moves:
        if move.piece_captured != '--':
            return move
    return find_random_move(valid_moves, gamestate)

def get_move(valid_moves, gamestate, algorithm):
    return algorithms[algorithm](valid_moves, gamestate)

algorithms = {
    "random":find_random_move,
    "blind_take":blind_take,
}