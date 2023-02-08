# Refactored and ported to Python 3.x version of https://github.com/drkstarks/FCC_renpy-chess_RuolinZheng

init python:

    import chess
    import pygame
    import logging
    import pprint as pp
    from collections import deque

    logging.basicConfig(
        format="[chess] @(%(funcName)s) :: %(message)s",
        level=logging.INFO if config.developer else logging.NOTSET
    )

    class ChessDisplayable(renpy.Displayable):

        draw_test_fen = "4q3/7K/8/1k6/8/6r1/8/8 w - - 0 1" # chess.STARTING_FEN
        
        def __init__(self, fen=chess.STARTING_FEN, player_color=chess.WHITE, engine=None, engine_limit=None, move_history_length=5, colors=ch.colors):
            super(ChessDisplayable, self).__init__()

            self.init_fen = fen
            self.board = chess.Board(fen=fen)
            self.move_history_length = move_history_length
            self.engine = engine
            self.engine_limit = engine_limit

            self.player_color = player_color
            self.is_board_flipped = False if player_color == chess.WHITE else True

            self.colors = colors
            self.piece_images = self.load_piece_images()

            self.selected_square = None
            self.legal_squares = []
            self.previous_move = []

            self.outcome = None

        @property
        def current_color(self):
            return self.board.turn

        @property
        def current_color_string(self):
            return get_color_name(self.board.turn)

        @property
        def history(self): # Not proud of this monstrosity, but works how I want..(index juggling about to begin:skull_emoji:)
            # NOTE: Will probably rewrite this later

            opener = self.board.move_stack[0] if self.board.move_stack else None

            # Since two moves are considered as one entry in the history(on screen) it needs to be doubled
            recent_moves = self.board.move_stack[(-self.move_history_length * 2):]
            
            # There's alway a white move to display in history
            white_moves = recent_moves[::2]
            # But when the player plays as black - game doesn't have move to show in pair with CPU's move in the row of history, so there's a limit
            black_moves = recent_moves[1::2] if self.player_color == chess.WHITE else deque(recent_moves[1::2], maxlen=self.move_history_length - 1)
            
            current_turn = len(self.board.move_stack[::2])

            # Renpy is not so hot on generators inside of screens, so making it a list?(works without, but for safety I guess?)
            turns = list(range(max(0, current_turn - self.move_history_length) + 1, current_turn + 1))

            return opener, white_moves, black_moves, turns

        def render(self, width, height, st, at):
            # logging.info(f"board rendered at {at:.4f}")
            render = renpy.Render(width, height)

            # Add highlight to selected square
            if self.selected_square:
                tile_screen_x, tile_screen_y = screen_coordinates_from_square(self.selected_square, self.is_board_flipped)
                render.place(self.highlight_tile(self.colors.selected), x=tile_screen_x, y=tile_screen_y)

            for file_index in range(8):
                for rank_index in range(8):
                    tile_screen_x, tile_screen_y = screen_coordinates_from_file_rank(file_index, rank_index, self.is_board_flipped)
                    current_square = chess.square(file_index, rank_index)

                    # Add highlight on legal move squares
                    if current_square in self.legal_squares:
                        render.place(self.highlight_tile(self.colors.legal), x=tile_screen_x, y=tile_screen_y)
                    
                    # Add highlight for previous move of CPU
                    if current_square in self.previous_move:
                        render.place(self.highlight_tile(self.colors.previous_move), x=tile_screen_x, y=tile_screen_y)

                    # Draw piece if there's one on the tile
                    piece = self.board.piece_at(current_square)
                    if piece and piece.symbol() in self.piece_images.keys():
                        render.place(self.piece_images[piece.symbol()], x=tile_screen_x, y=tile_screen_y)
            
            renpy.restart_interaction()

            return render
        
        def highlight_tile(self, color):
            return Solid(color, xysize=ch.tile_dimensions)
        
        def event(self, ev, x, y, st):
            # TODO: remove later(used for color changer)
            self.piece_images = self.load_piece_images()

            if self.board.outcome():
                self.handle_outcome(self.board.outcome())
                return

            if self.current_color != self.player_color:
                result = self.engine.play(self.board, self.engine_limit)
                self.make_move(result.move)
                logging.info(f"CPU's turn ({self.current_color_string}): {result.move}")
                renpy.redraw(self, 0)
                return
            
            # Check for interaction(and skip if there's none)
            # if ev.type != pygame.MOUSEBUTTONDOWN or ev.button != 1 or (x < 0 or x > ch.board_size) or (y < 0 or y > ch.board_size):
            #     return
            # TODO: SWITCH TO THE STATEMENT ABOVE BEFORE SHIPPING!!!!!! (written this way to allow dynamic color picker)
            if 0 < x < ch.board_size and 0 < y < ch.board_size and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                selected_square = screen_coordinates_to_square(x, y, self.is_board_flipped)
                logging.info(f"selected square: {selected_square}")

                if self.selected_square is None:
                    self.handle_select(selected_square)
                else:
                    self.handle_move(selected_square)
                    
                self.check_game_status()

            renpy.redraw(self, 0)
        
        def get_legal_move_squares_from(self, square):
            logging.info(f"legal moves from [{square}]: {list(filter(lambda m: m.from_square == square, self.board.legal_moves))}")
            return [legal_move.to_square for legal_move in filter(lambda m: m.from_square == square, self.board.legal_moves)]

        def select_square(self, square):
            self.selected_square = square
            self.legal_squares = self.get_legal_move_squares_from(square)

        def deselect_square(self):
            self.selected_square = None
            self.legal_squares.clear()
        
        def handle_select(self, square):
            piece = self.board.piece_at(square)
            if piece and piece.color == self.current_color:
                logging.info(f"selected piece: {piece}")
                self.select_square(square)

        def handle_move(self, next_square):
            # Deselect if it's the same square
            if next_square == self.selected_square:
                self.deselect_square()
                return

            # Change selected square if different piece is chosen
            piece = self.board.piece_at(next_square)
            if piece and piece.color == self.current_color:
                self.select_square(next_square)
                return

            move = chess.Move(self.selected_square, next_square)
            if move in self.board.legal_moves:
                self.make_move(move)

        def make_move(self, move):
            self.board.push(move)
            self.previous_move = [move.from_square, move.to_square]
            self.deselect_square()
        
        def undo_move(self):
            if len(self.board.move_stack) < 2:
                return
            
            self.board.pop() # CPU's move
            self.board.pop() # Player's move

            self.deselect_square()
            self.previous_move.clear()

        def check_game_status(self):
            if self.board.can_claim_threefold_repetition():
                pass
        
        def handle_outcome(self, outcome):
            # TODO: Remove later?
            if self.outcome is None:
                logging.info(f"game ended: {self.board.outcome()}")
            self.outcome = outcome
            
            # TODO: Figure out how to end the game
            if outcome.termination == chess.Termination.CHECKMATE:
                renpy.notify(f"Checkmate! The winner is {get_color_name(outcome.winner)}")
                return
            
            if outcome.termination == chess.Termination.STALEMATE:
                renpy.notify('Stalemate~')
                return

            logging.info(f"Can claim threefold? ({self.board.can_claim_threefold_repetition()})")
            if self.board.can_claim_threefold_repetition():
                self.prompt_draw(reason='Fivefold repetition rule')
            if outcome.termination == chess.Termination.FIFTY_MOVES:
                self.prompt_draw(reason='Fifty moves rule')

        def prompt_draw(self, reason=''):
            renpy.show_screen(
                'confirm',
                message=f"{reason}: Would you like to claim draw?",
                yes_action=[
                    Hide('confirm'),
                    Return(self.outcome)
                ],
                no_action=Hide('confirm')
            )

            renpy.restart_interaction()
        
        def reset_board(self):
            self.board.reset()
            self.board.set_fen(self.init_fen)
            self.selected_square = None
            self.legal_squares.clear()
            self.previous_move.clear()

        def flip_board(self):
            self.is_board_flipped = not self.is_board_flipped

        def load_piece_images(self):
            piece_types = ('p', 'r', 'b', 'n', 'k', 'q')

            piece_images = {}
            for piece in piece_types:
                piece_image = f"{ch.new_piece_images_path}/{piece}.png"

                white_piece, black_piece = piece.upper(), piece

                white_piece_asset = Transform(
                    piece_image,
                    xysize=ch.piece_dimensions,
                    matrixcolor=ColorizeMatrix(
                        black_color=self.colors.piece_black,
                        white_color=self.colors.piece_white
                    )
                )
                black_piece_asset = Transform(
                    piece_image,
                    xysize=ch.piece_dimensions,
                    matrixcolor=ColorizeMatrix(
                        black_color=self.colors.piece_white,
                        white_color=self.colors.piece_black
                    )
                )

                piece_images[white_piece] = white_piece_asset
                piece_images[black_piece] = black_piece_asset

            return piece_images
