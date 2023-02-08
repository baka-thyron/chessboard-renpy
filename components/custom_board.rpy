transform tile_shadow(color_1, color_2):
    gradient_left_diagonal(
        color_1=color_1,
        color_2=color_2
    )

screen custom_tile(asset, color, shadow, colors=ch.colors):
    add Transform(asset):
        at tile_shadow(shadow, color)
        xysize ch.tile_dimensions

screen custom_board(colors=ch.colors):
    hbox:
        for ci, column index column in enumerate(ch.letters):
            vbox:
                for ri, row index row in enumerate(ch.numbers):
                    if (ci + ri) % 2 == 0:
                        use custom_tile(
                            "#ffff",
                            colors.custom_board_white,
                            colors.custom_board_white_shadow
                        )
                    else:
                        use custom_tile(
                            "#ffff",
                            colors.custom_board_black,
                            colors.custom_board_black_shadow
                        )
