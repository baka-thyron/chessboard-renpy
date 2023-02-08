init -99 python: # -99 for now

    import chess
    import chess.engine
    import os

    def get_stockfish_exec_file(bin_dir="bin"):
        if renpy.android:
            stockfish_bin = 'stockfish_armv7'
        elif renpy.linux:
            stockfish_bin = 'stockfish_linux_x64'
        elif renpy.windows:
            stockfish_bin = 'stockfish_win_x64.exe'

        return os.path.join(renpy.config.gamedir, bin_dir, stockfish_bin)

    # build.executable(os.path.join(stockfish_dir, 'stockfish-11-64')) # mac
    # build.executable(os.path.join(stockfish_dir, 'stockfish_20011801_x64')) # linux
    
    def open_engine(search_time=0.1, search_depth=1):
        # Just to be safe - close all other launched engines(rollback?)
        # (Maybe there's a better way with Renpy that I haven't think of yet..)
        close_engine()

        engine = chess.engine.SimpleEngine.popen_uci(get_stockfish_exec_file())
        limit = chess.engine.Limit(
            time=search_time,
            depth=search_depth
        )
        config.at_exit_callbacks.append(engine.quit)
        return engine, limit
    
    def close_engine():
        for callback in list(config.at_exit_callbacks):
            if callback.__func__ == chess.engine.SimpleEngine.quit:
                callback()
                config.at_exit_callbacks.remove(callback)

init python:
    def test_stockfish():
        engine, limit = open_engine()
        board = chess.Board()
        while not board.is_game_over():
            result = engine.play(board, limit)
            print(result)
            board.push(result.move)

        engine.quit()