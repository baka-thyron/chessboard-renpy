label open_chessboard(engine_move_time=0.1, engine_depth=1):
    window hide
    python:
        engine, engine_limit = open_engine(engine_move_time, engine_depth)
        renpy.call_screen("chess_screen", engine, engine_limit)
        close_engine()