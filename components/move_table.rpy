init:
    define ch.move_table_width = 500
    define ch.writing_size = 40
    define ch.table_start_offset = 40
    define ch.column_width = 120
    define ch.column_width_small = 40
    define ch.checkmark_width = 40

screen move_table(opener, white_moves, black_moves, turns, player_color, colors=ch.colors, **properties):
    fixed:
        fit_first True
        properties properties

        vbox:
            add Transform("ch_asset notepad_header"):
                fit "contain"
                xsize ch.move_table_width
                matrixcolor TintMatrix(colors.paper)

            frame:
                background colors.paper
                add Transform("ch_asset move_table"):
                    fit "contain"
                    xsize ch.move_table_width
        
        frame:
            xpadding system.spacing
            align (0.5, 0.0)
            yoffset ch.table_start_offset

            vbox:
                first_spacing system.spacing_xmedium

                hbox:
                    spacing system.spacing_small
                    xfill True

                    use color_mark("W", player_color)
                    use color_mark("B", player_color)

                    frame:
                        xfill True
                        has hbox
                        spacing system.spacing

                        text "Opening:":
                            size ch.writing_size
                            font ch.pencil_font
                            color colors.writing
                            bold True
                            italic True

                        if opener:
                            text "[opener]":
                                size ch.writing_size
                                font ch.pencil_font
                                color colors.writing
                                bold True
                                italic True
                hbox:
                    xfill True
                    first_spacing system.spacing
                    use table_column(turns, width=ch.column_width_small, xoffset=system.spacing)
                    use table_column(white_moves)
                    use table_column(black_moves)

screen color_mark(color_letter, player_color, colors=ch.colors):
    hbox:
        spacing system.spacing_small

        text "[color_letter]:":
            size ch.writing_size
            font ch.pencil_font
            color colors.writing
            bold True
            italic True

        if get_color_name(player_color)[0].lower() == color_letter.lower():
            add Transform("ch_asset props checkmark"):
                fit "contain"
                xsize ch.checkmark_width
        else:
            null width ch.checkmark_width

screen table_column(entries, width=ch.column_width, colors=ch.colors, **properties):
    vbox:
        xsize width
        spacing system.spacing_medium

        properties properties
        
        for e in entries:
            text "[e]":
                xalign 0.5
                size ch.writing_size
                font ch.pencil_font
                color colors.writing
                bold True
                italic True