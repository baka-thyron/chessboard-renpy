style chessboard_frame is default

init python:
    config.window_auto_hide.append("board")

screen chess_screen(engine=None, engine_limit=None, colors=ch.colors):
    default chess_displayable = ChessDisplayable(engine=engine, engine_limit=engine_limit)
    default hover_displayable = HoverDisplayable()
    
    style_prefix "chessboard"
    modal True

    frame:
        background Frame("ch_asset texture wood")
        xfill True
        yfill True

        add Solid(colors.bg_tint)
        
    fixed:
        fit_first True
        align (0.5, 0.5)

        use chessboard(chess_displayable, hover_displayable)

    use draggable(align=(1.0, 0.5), xoffset=-40):
        use move_table(*chess_displayable.history, chess_displayable.player_color)
    use misc
    use controls(chess_displayable)


screen controls(chess_displayable):
    use draggable(offset=(-650, 100), align=(0.5, 0.5)):
        add Transform("ch_asset props coin"):
            fit "contain"
            xsize 150
            align (0.5, 0.5)
            offset (-650, 100)
            if get_color_name(chess_displayable.current_color) == "WHITE":
                matrixcolor ColorizeMatrix(black_color="#fff", white_color="#000")

    textbutton "Reset Board":
        align (0.0, 1.0)
        offset (70, -110)
        action Function(chess_displayable.reset_board)
        text_size 42
        text_font ch.pencil_font
        text_bold True

    imagebutton:
        action Function(chess_displayable.flip_board)
        align (0.5, 0.5)
        offset (-470, 400)

        idle Transform(
            "ch_asset props flip_icon",
            fit="contain",
            xsize=150
        )

        hover Transform(
            "ch_asset props flip_icon",
            fit="contain",
            xsize=150,
            matrixcolor=TintMatrix("#fffa")
        )

    imagebutton:
        action Function(chess_displayable.undo_move)
        focus_mask Transform(
            "ch_asset props eraser",
            fit="contain",
            xsize=150
        )
        align (1.0, 1.0)
        offset (-400, -100)

        idle Transform(
            "ch_asset props eraser",
            fit="contain",
            xsize=150
        )

        hover Transform(
            "ch_asset props eraser",
            fit="contain",
            xsize=150,
            matrixcolor=TintMatrix("#666")
        )

screen misc():
    use draggable(pos=(0,0)):
        fixed:
            fit_first True
            # align (0.0, 0.0)
            # offset (-200, -200)
            add Transform("ch_asset props coffee"):
                fit "contain"
                xsize 400
                align (0.5, 0.5)
                rotate 160
                rotate_pad False
    
    use draggable(align=(1.0, 1.0), offset=(-20, 0)):
        add Transform("ch_asset props pencil"):
            fit "contain"
            ysize 500
            rotate 20
            rotate_pad False
