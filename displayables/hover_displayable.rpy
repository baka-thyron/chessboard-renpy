# Borrowed from https://github.com/drkstarks/FCC_renpy-chess_RuolinZheng

init python:
    class HoverDisplayable(renpy.Displayable):
        def __init__(self, colors=ch.colors):
            super(HoverDisplayable, self).__init__()
            self.hover_coord = None
            self.hover_img = Solid(colors.hovered, xysize=ch.tile_dimensions)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            if self.hover_coord:
                render.place(
                    self.hover_img, 
                    x=self.hover_coord[0],
                    y=self.hover_coord[1], 
                    width=ch.tile_size,
                    height=ch.tile_size
                )
            return render

        def event(self, ev, x, y, st):
            if 0 < x < ch.board_size and 0 < y < ch.board_size:
                self.hover_coord = tilesnapped_coordinates(x, y)
                renpy.redraw(self, 0)
            elif self.hover_coord:
                self.hover_coord = None
                renpy.redraw(self, 0)