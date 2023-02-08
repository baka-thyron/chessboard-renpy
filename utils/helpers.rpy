# Parts borrowed and converted for Python 3.x from https://github.com/drkstarks/FCC_renpy-chess_RuolinZheng

init -10 python:

    import chess

    def get_color_name(color):
        return "WHITE" if color == chess.WHITE else "BLACK"

    def screen_coordinates_from_square(square, is_board_flipped=False):
        if is_board_flipped:
            x = ch.tile_size * (7 - chess.square_file(square))
            y = ch.tile_size * chess.square_rank(square)
        else:
            x = ch.tile_size * chess.square_file(square)
            y = ch.tile_size * (7 - chess.square_rank(square))

        return x, y
    
    def screen_coordinates_from_file_rank(file_index, rank_index, is_board_flipped=False):
        if is_board_flipped:
            x = ch.tile_size * (7 - file_index)
            y = ch.tile_size * rank_index
        else:
            x = ch.tile_size * file_index
            y = ch.tile_size * (7 - rank_index)

        return x, y

    def screen_coordinates_to_square(screen_x, screen_y, is_board_flipped=False):
        if is_board_flipped:
            file_index = 7 - (screen_x // ch.tile_size)
            rank_index = screen_y // ch.tile_size
        else:
            file_index = screen_x // ch.tile_size
            rank_index = 7 - (screen_y // ch.tile_size)

        return chess.square(int(file_index), int(rank_index))

    def tilesnapped_coordinates(x, y):
        # Snaps to the top left corner of the tile
        tile_x = x // ch.tile_size * ch.tile_size
        tile_y = y // ch.tile_size * ch.tile_size
        
        return tile_x, tile_y
    