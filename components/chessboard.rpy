init:
    # Welp, the only way I see to prevent generators inside screens....
    define ch.numbers = list(range(8, 0, -1))
    define ch.letters = [chr(n).upper() for n in range(ord("a"), ord("h") + 1)]

    define ch.numbers_flipped = list(range(1, 9))
    define ch.letters_flipped = [chr(n).upper() for n in range(ord("h"), ord("a") - 1, -1)]

screen text_label(label_text, font=None):
    text "[label_text]":
        align (0.5, 0.5)
        text_align 0.5
        size 14
        min_width 20
        bold True
        if font:
            font font

screen label_row(is_board_flipped=False, font=None, **properties):
    frame:
        xfill True
        ysize system.spacing
        xpadding system.spacing

        properties properties

        frame:
            yalign 0.5
            has hbox
            xfill True
            if is_board_flipped:
                for label_text in ch.letters_flipped:
                    use text_label(label_text, font)
            else:
                for label_text in ch.letters:
                    use text_label(label_text, font)

screen label_column(is_board_flipped=False, font=None, **properties):
    frame:
        xsize system.spacing
        yfill True
        ypadding system.spacing

        properties properties

        frame:
            xalign 0.5
            has vbox
            yfill True
            if is_board_flipped:
                for label_text in ch.numbers_flipped:
                    use text_label(label_text, font)
            else:
                for label_text in ch.numbers:
                    use text_label(label_text, font)


screen chessboard(chess_displayable, hover_displayable, colors=ch.colors):
    frame:
        background At(
            Flatten(system.frame_rounded_full),
            tile_shadow(colors.custom_board_bg_shadow, colors.custom_board_bg)
        )
        padding (system.spacing_xmedium, system.spacing_xmedium)

        fixed:
            fit_first True

            use custom_board
            add chess_displayable
            add hover_displayable

    use label_row(
        is_board_flipped=chess_displayable.is_board_flipped,
        align=(0.5, 1.0),
        ysize=system.spacing_xmedium,
        xpadding=system.spacing_xmedium,
        font=system.ui_font_test
    )
    use label_column(
        is_board_flipped=chess_displayable.is_board_flipped,
        align=(1.0, 0.5),
        xsize=system.spacing_xmedium,
        ypadding=system.spacing_xmedium,
        font=system.ui_font_test
    )
