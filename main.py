from tkinter import *
from tkinter import font

if __name__ == "__main__":
    images = {}
    cell_ids_cells = {}
    selected_piece = []
    check_cell = []
    checking_piece_cell = []
    white_king_cell = []
    black_king_cell = []
    white_pieces_attack_field = []
    black_pieces_attack_field = []
    self_check_moves = []
    cover_from_check_moves = []
    valid_moves = []
    white_turn = True
    marks = []
    check = False

    class Cell:
        __mark_color__ = "#22B14C"
        __check_color__ = "#ED1C24"
        marked = False
        contains_piece = ""
        contains_king = False

        def __init__(self, x, y, cell_id, color):
            self.x = x
            self.y = y
            self.cell_id = cell_id
            self.color = color
            Board.tag_bind(self.cell_id, "<Button-1>", lambda event, arg=cell_id: self.cell_click())

        @staticmethod
        def cell_click():
            if len(selected_piece) > 0:
                selected_piece[0].clear_marks()
                selected_piece.clear()
                if check:
                    Board.itemconfig(check_cell[0].cell_id, fill=check_cell[0].__check_color__)

        def mark(self, event):
            return Board.create_image(self.x, self.y, image=mark_image)


    class Piece:
        is_King = False
        first_turn = True
        binding_piece = None
        binded_piece = None
        binding_direction = ""
        binding_moves = []
        binded = False
        binding = False

        def __init__(self, cell, color, image):
            self.cell = cell
            self.color = color
            self.image = image
            self.moves = []
            Board.tag_bind(self.image, "<Button-1>", lambda event, arg=image: self.piece_click(event, arg))

        def show_moves(self, event):
            global check
            self.clear_marks()
            selected_piece.clear()
            selected_piece.append(self)
            Board.itemconfig(selected_piece[0].cell.cell_id, fill="#EAFC10")
            for cell in self.moves:
                if cell.contains_piece == "":
                    mark = cell.mark(event)
                    Board.tag_bind(mark, "<Button-1>", lambda event, arg=mark: self.move(event, arg))
                    marks.append(mark)
                else:
                    cell.marked = True
                    Board.itemconfig(cell.cell_id, fill=cell.__mark_color__)
            if check:
                Board.itemconfig(check_cell[0].cell_id, fill=check_cell[0].__check_color__)

        def find_moves(self):
            pass

        def validate_moves(self):
            if check:
                invalid_moves = []
                for move in self.moves:
                    valid = False
                    for valid_move in valid_moves:
                        if move == valid_move:
                            valid = True
                            break
                    if not valid:
                        invalid_moves.append(move)
                for invalid_move in invalid_moves:
                    self.moves.remove(invalid_move)

        def check(self, event):
            pass

        def clear_marks(self):
            for item in marks:
                Board.delete(item)
            marks.clear()
            for cell in selected_piece[0].moves:
                if cell.marked:
                    Board.itemconfig(cell.cell_id, fill=cell.color, width=1)
                    cell.marked = False
            if len(selected_piece) > 0:
                Board.itemconfig(selected_piece[0].cell.cell_id, fill=selected_piece[0].cell.color)

        def taking(self, event):
            global white_turn
            global check
            black_pieces_attack_field.clear()
            white_pieces_attack_field.clear()
            white_turn = not white_turn
            taking_piece_image = selected_piece[0].image
            position_to_move = (self.cell.x - selected_piece[0].cell.x, self.cell.y - selected_piece[0].cell.y)
            Board.move(taking_piece_image, position_to_move[0], position_to_move[1])
            Board.itemconfig(selected_piece[0].cell.cell_id, fill=selected_piece[0].cell.color)
            self.clear_marks()
            if selected_piece[0].is_King:
                if selected_piece[0].color == "White":
                    white_king_cell.clear()
                    white_king_cell.append(self.cell)
                else:
                    black_king_cell.clear()
                    black_king_cell.append(self.cell)
            selected_piece[0].cell.contains_piece = ""
            selected_piece[0].cell = get_cell(self.cell.x, self.cell.y)
            self.cell.contains_piece = selected_piece[0].color
            Board.delete(self.image)
            self.cell.marked = False
            self.first_turn = False
            if self.binded:
                self.binded = False
                self.binding_piece.binded_piece = None
                self.binding_piece = None
            if self.color == "White":
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
            valid_moves.clear()
            checking_piece_cell.clear()
            if selected_piece[0].color == "White":
                white_pieces_attack_field.clear()
                for white_piece in white_pieces:
                    white_piece.find_moves()
                    if type(white_piece) != Pawn:
                        white_pieces_attack_field.extend(white_piece.moves)
                    for move in white_piece.moves:
                        if move == black_king_cell[0]:
                            check = True
                            check_cell.append(black_king_cell[0])
                            checking_piece_cell.append(white_piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
                black_pieces_attack_field.clear()
                for black_piece in black_pieces:
                    black_piece.find_moves()
                    if type(black_piece) != Pawn:
                        black_pieces_attack_field.extend(black_piece.moves)
                    for move in black_piece.moves:
                        if move == white_king_cell[0]:
                            check = True
                            check_cell.append(white_king_cell[0])
                            checking_piece_cell.append(black_piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
            else:
                black_pieces_attack_field.clear()
                for black_piece in black_pieces:
                    black_piece.find_moves()
                    if type(black_piece) != Pawn:
                        black_pieces_attack_field.extend(black_piece.moves)
                    for move in black_piece.moves:
                        if move == white_king_cell[0]:
                            check = True
                            check_cell.append(white_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
                white_pieces_attack_field.clear()
                for white_piece in white_pieces:
                    white_piece.find_moves()
                    if type(white_piece) != Pawn:
                        white_pieces_attack_field.extend(white_piece.moves)
                    for move in white_piece.moves:
                        if move == black_king_cell[0]:
                            check = True
                            check_cell.append(black_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
            selected_piece.clear()

        def piece_click(self, event, arg):
            if image_pieces[arg].cell.marked:
                self.taking(event)
            else:
                if image_pieces[arg].color == "White" and white_turn:
                    selected_piece.append(image_pieces[arg])
                    image_pieces[arg].show_moves(event)
                elif image_pieces[arg].color == "Black" and not white_turn:
                    selected_piece.append(image_pieces[arg])
                    image_pieces[arg].show_moves(event)

        def move(self, event, arg):
            global white_turn
            global black_king_cell
            global white_king_cell
            global check
            if check:
                check = not check
                Board.itemconfig(check_cell[0].cell_id, fill=check_cell[0].color)
                check_cell.clear()
            white_turn = not white_turn
            self.first_turn = False
            Board.move(self.image, Board.coords(arg)[0] - Board.coords(self.image)[0], Board.coords(arg)[1] - Board.coords(self.image)[1])
            Board.itemconfig(self.cell.cell_id, fill=selected_piece[0].cell.color)
            self.cell.contains_piece = ""
            self.cell = get_cell(Board.coords(arg)[0], Board.coords(arg)[1])
            self.cell.contains_piece = self.color
            self.clear_marks()
            selected_piece.clear()
            if self.is_King:
                if self.color == "White":
                    white_king_cell.clear()
                    white_king_cell.append(self.cell)
                else:
                    black_king_cell.clear()
                    black_king_cell.append(self.cell)
            if self.color == "White":
                white_pieces_attack_field.clear()
                for piece in white_pieces:
                    piece.find_moves()
                    if type(piece) != Pawn:
                        white_pieces_attack_field.extend(piece.moves)
                    for move in piece.moves:
                        if move == black_king_cell[0]:
                            check = True
                            check_cell.append(black_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
                black_pieces_attack_field.clear()
                for piece in black_pieces:
                    piece.find_moves()
                    if type(piece) != Pawn:
                        black_pieces_attack_field.extend(piece.moves)
                    for move in piece.moves:
                        if move == white_king_cell[0]:
                            check = True
                            check_cell.append(white_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
            else:
                black_pieces_attack_field.clear()
                for piece in black_pieces:
                    piece.find_moves()
                    if type(piece) != Pawn:
                        black_pieces_attack_field.extend(piece.moves)
                    for move in piece.moves:
                        if move == white_king_cell[0]:
                            check = True
                            check_cell.append(white_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
                white_pieces_attack_field.clear()
                for piece in white_pieces:
                    piece.find_moves()
                    if type(piece) != Pawn:
                        white_pieces_attack_field.extend(piece.moves)
                    for move in piece.moves:
                        if move == black_king_cell[0]:
                            check = True
                            check_cell.append(black_king_cell[0])
                            checking_piece_cell.append(piece.cell)
                            valid_moves.extend(checking_piece_cell)
                            Board.itemconfig(move.cell_id, fill=move.__check_color__)
            valid_moves.clear()
            checking_piece_cell.clear()

        def validate_moves_binded(self):
            if self.binded:
                invalid_moves = []
                for move in self.moves:
                    valid_move = False
                    for bind_move in self.binding_piece.binding_moves:
                        if move == bind_move:
                            valid_move = True
                            break
                    if not valid_move:
                        invalid_moves.append(move)
                for invalid_move in invalid_moves:
                    self.moves.remove(invalid_move)

    class Pawn(Piece):

        def __init__(self, cell, color, image):
            super().__init__(cell, color, image)
            self.moves = []

        def find_moves(self):
            global check
            global check_cell
            global black_king_cell
            global valid_moves
            self.moves.clear()
            if self.color == "White" and self.cell.y != 40:
                if get_cell(self.cell.x, self.cell.y - 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x, self.cell.y - 80))
            elif self.color == "Black" and self.cell.y != 600:
                if get_cell(self.cell.x, self.cell.y + 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x, self.cell.y + 80))
            if self.first_turn:
                if self.color == "White":
                    if get_cell(self.cell.x, self.cell.y - 160).contains_piece == "" and get_cell(self.cell.x,
                                                                                                  self.cell.y - 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x, self.cell.y - 160))
                else:
                    if get_cell(self.cell.x, self.cell.y + 160).contains_piece == "" and get_cell(self.cell.x, self.cell.y + 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x, self.cell.y + 160))
            if self.color == "White" and self.cell.y != 40:
                if self.cell.x != 40:
                    if get_cell(self.cell.x - 80, self.cell.y - 80).contains_piece == "Black":
                        self.moves.append(get_cell(self.cell.x - 80, self.cell.y - 80))
                    elif get_cell(self.cell.x - 80, self.cell.y - 80).contains_piece == "":
                        white_pieces_attack_field.append(get_cell(self.cell.x - 80, self.cell.y - 80))
                if self.cell.x != 600:
                    if get_cell(self.cell.x + 80, self.cell.y - 80).contains_piece == "Black":
                        self.moves.append(get_cell(self.cell.x + 80, self.cell.y - 80))
                    elif get_cell(self.cell.x + 80, self.cell.y - 80).contains_piece == "":
                        white_pieces_attack_field.append(get_cell(self.cell.x + 80, self.cell.y - 80))
            elif self.color == "Black" and self.cell.y != 600:
                if self.cell.x != 40:
                    if get_cell(self.cell.x - 80, self.cell.y + 80).contains_piece == "White":
                        self.moves.append(get_cell(self.cell.x - 80, self.cell.y + 80))
                    elif get_cell(self.cell.x - 80, self.cell.y + 80).contains_piece == "":
                        black_pieces_attack_field.append(get_cell(self.cell.x - 80, self.cell.y + 80))
                if self.cell.x != 600:
                    if get_cell(self.cell.x + 80, self.cell.y + 80).contains_piece == "White":
                        self.moves.append(get_cell(self.cell.x + 80, self.cell.y + 80))
                    elif get_cell(self.cell.x + 80, self.cell.y + 80).contains_piece == "":
                        black_pieces_attack_field.append(get_cell(self.cell.x + 80, self.cell.y + 80))
            self.validate_moves()
            self.validate_moves_binded()

    class Bishop(Piece):
        def __int__(self, cell, color, image):
            super().__init__(cell, color, image)

        def find_moves(self):
            self.moves.clear()
            selected_piece.append(self)
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 600 and mark_y != 40:
                if get_cell(mark_x + 80, mark_y - 80).contains_piece == "":
                    mark_x = mark_x + 80
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)                                    #This block and so on adds to invalid moves move behind king in the direction of attack of the checking piece
                        check_mark_x = self.cell.x
                        check_mark_y = self.cell.y
                        enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell[0]
                        if target_cell == enemy_king_cell:
                            self.moves.pop()
                            while check_mark_x != enemy_king_cell.x:
                                check_mark_x = check_mark_x + 80
                                check_mark_y = check_mark_y - 80
                                valid_moves.append(get_cell(check_mark_x, check_mark_y))
                            if target_cell.x != 600 and target_cell.y != 40:
                                if self.color == "White":
                                    white_pieces_attack_field.append(get_cell(black_king_cell[0].x + 80, black_king_cell[0].y - 80))
                                else:
                                    black_pieces_attack_field.append(get_cell(white_king_cell[0].x + 80, white_king_cell[0].y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600 and mark_x != 40:
                if get_cell(mark_x - 80, mark_y + 80).contains_piece == "":
                    mark_x = mark_x - 80
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            check_mark_x = self.cell.x
                            check_mark_y = self.cell.y
                            enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell
                            if target_cell == enemy_king_cell:
                                self.moves.pop()
                                while check_mark_x != enemy_king_cell.x:
                                    check_mark_x = check_mark_x - 80
                                    check_mark_y = check_mark_y + 80
                                    valid_moves.append(get_cell(check_mark_x, check_mark_y))
                                if target_cell.x != 40 and target_cell.y != 600:
                                    if self.color == "White":
                                        white_pieces_attack_field.append(get_cell(black_king_cell[0].x - 80, black_king_cell[0].y + 80))
                                    else:
                                        black_pieces_attack_field.append(get_cell(white_king_cell[0].x - 80, white_king_cell[0].y + 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 40 and mark_x != 40:
                if get_cell(mark_x - 80, mark_y - 80).contains_piece == "":
                    mark_x = mark_x - 80
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            check_mark_x = self.cell.x
                            check_mark_y = self.cell.y
                            enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell[0]
                            if target_cell == enemy_king_cell:
                                self.moves.pop()
                                while check_mark_x != enemy_king_cell.x:
                                    check_mark_x = check_mark_x - 80
                                    check_mark_y = check_mark_y - 80
                                    valid_moves.append(get_cell(check_mark_x, check_mark_y))
                                if target_cell.x != 40 and target_cell.y != 40:
                                    if self.color == "White":
                                        white_pieces_attack_field.append(get_cell(black_king_cell[0].x - 80, black_king_cell[0].y - 80))
                                    else:
                                        black_pieces_attack_field.append(get_cell(white_king_cell[0].x - 80, white_king_cell[0].y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600 and mark_x != 600:
                if get_cell(mark_x + 80, mark_y + 80).contains_piece == "":
                    mark_x = mark_x + 80
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            check_mark_x = self.cell.x
                            check_mark_y = self.cell.y
                            enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell[0]
                            if target_cell == enemy_king_cell:
                                self.moves.pop()
                                while check_mark_x != black_king_cell[0].x:
                                    check_mark_x = check_mark_x + 80
                                    check_mark_y = check_mark_y + 80
                                    valid_moves.append(get_cell(check_mark_x, check_mark_y))
                                if target_cell.x != 600 and target_cell.y != 600:
                                    if self.color == "White":
                                        white_pieces_attack_field.append(get_cell(black_king_cell[0].x + 80, black_king_cell[0].y + 80))
                                    else:
                                        black_pieces_attack_field.append(get_cell(white_king_cell[0].x + 80, white_king_cell[0].y + 80))
                    break
            self.validate_moves()
            self.validate_moves_binded()

        def find_binding_moves(self):
            king_x = 0
            king_y = 0
            if self.color == "White":
                king_x = black_king_cell[0].x
                king_y = black_king_cell[0].x
                if self.cell.x - king_x == self.cell.y - king_y:
                    pass

    class Rook(Piece):
        def __init__(self, cell, color, image):
            super().__init__(cell, color, image)

        def find_moves(self):
            self.moves.clear()
            selected_piece.append(self)
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600:
                if get_cell(mark_x, mark_y + 80).contains_piece == "":
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        check_mark_x = self.cell.x
                        check_mark_y = self.cell.y
                        enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell[0]
                        if target_cell == enemy_king_cell:
                            while check_mark_y != enemy_king_cell.y:
                                check_mark_y = check_mark_y + 80
                                valid_moves.append(get_cell(check_mark_x, check_mark_y))
                            if target_cell.y != 600:
                                if self.color == "White":
                                    white_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y + 80))
                                else:
                                    black_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y + 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 40:
                if get_cell(mark_x, mark_y - 80).contains_piece == "":
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        check_mark_x = self.cell.x
                        check_mark_y = self.cell.y
                        enemy_king_cell = black_king_cell[0] if self.color == "White" else white_king_cell[0]
                        if target_cell == enemy_king_cell:
                            while check_mark_y != enemy_king_cell.y:
                                check_mark_y = check_mark_y - 80
                                valid_moves.append(get_cell(check_mark_x, check_mark_y))
                        if target_cell.y != 40:
                            if self.color == "White":
                                white_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y - 80))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 40:
                if get_cell(mark_x - 80, mark_y).contains_piece == "":
                    mark_x = mark_x - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        check_mark_x = self.cell.x
                        check_mark_y = self.cell.y
                        enemy_king_cell = black_king_cell[0] if self.color == "White" else black_king_cell[0]
                        if target_cell == enemy_king_cell:
                            while check_mark_x != enemy_king_cell.x:
                                check_mark_x = check_mark_x - 80
                                valid_moves.append(get_cell(check_mark_x, check_mark_y))
                        if target_cell.x != 40:
                            if self.color == "White":
                                white_pieces_attack_field.append(get_cell(target_cell.x - 80, target_cell.y))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x - 80, target_cell.y))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 600:
                if get_cell(mark_x + 80, mark_y).contains_piece == "":
                    mark_x = mark_x + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        check_mark_x = self.cell.x
                        check_mark_y = self.cell.y
                        enemy_king_cell = black_king_cell[0] if self.color == "White" else black_king_cell[0]
                        if target_cell == enemy_king_cell:
                            while check_mark_x != enemy_king_cell.x:
                                check_mark_x = check_mark_x + 80
                                valid_moves.append(get_cell(check_mark_x, check_mark_y))
                            if target_cell.x != 600:
                                if self.color == "White":
                                    white_pieces_attack_field.append(get_cell(target_cell.x + 80, target_cell.y))
                                else:
                                    black_pieces_attack_field.append(get_cell(target_cell.x + 80, target_cell.y))
                    break
            self.validate_moves()
            self.validate_moves_binded()
            self.find_binding_moves()

        def find_binding_moves(self):
            enemy_king_x = 0
            enemy_king_y = 0
            if self.color == "White":
                enemy_king_x = black_king_cell[0].x
                enemy_king_y = black_king_cell[0].y
            else:
                enemy_king_x = white_king_cell[0].x
                enemy_king_y = white_king_cell[0].y
            if self.binded_piece is None:
                if enemy_king_x == self.cell.x:
                    if self.color == "White":
                        for white_piece in white_pieces:
                            if white_piece.cell.x == enemy_king_x and enemy_king_y < white_piece.cell.y < self.cell.y:
                                return
                        in_between_pieces = []
                        for black_piece in black_pieces:
                            if black_piece.cell.x == enemy_king_x and enemy_king_y < black_piece.cell.y < self.cell.y:
                                in_between_pieces.append(black_piece)
                        if len(in_between_pieces) == 1:
                            in_between_pieces[0].binded = True
                            print("binded")
                            self.binding_direction = "vertical"
                            in_between_pieces[0].binding_piece = self
                            self.binded_piece = in_between_pieces[0]
                            step_y = enemy_king_y
                            while step_y != self.cell.y:
                                step_y = step_y + 80
                                target_cell = get_cell(enemy_king_x, step_y)
                                if target_cell.contains_piece == "":
                                    self.binding_moves.append(target_cell)
            else:
                if self.cell.x != enemy_king_x:
                    self.binded_piece.binded = False
                    self.binded_piece.binding_piece = None
                    self.binded_piece = None
                    self.binding_moves.clear()

    class Knight(Piece):

        def __init__(self, cell, color, image):
            super().__init__(cell, color, image)

        def find_moves(self):
            self.moves.clear()
            selected_piece.append(self)
            if self.cell.y > 120:
                if self.cell.x > 40:
                    if get_cell(self.cell.x - 80, self.cell.y - 160).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x - 80, self.cell.y - 160))
                    else:
                        target_cell = get_cell(self.cell.x - 80, self.cell.y - 160)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                if self.cell.x < 600:
                    if get_cell(self.cell.x + 80, self.cell.y - 160).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x + 80, self.cell.y - 160))
                    else:
                        target_cell = get_cell(self.cell.x + 80, self.cell.y - 160)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
            if self.cell.y < 520:
                if self.cell.x > 40:
                    if get_cell(self.cell.x - 80, self.cell.y + 160).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x - 80, self.cell.y + 160))
                    else:
                        target_cell = get_cell(self.cell.x - 80, self.cell.y + 160)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                if self.cell.x < 600:
                    if get_cell(self.cell.x + 80, self.cell.y + 160).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x + 80, self.cell.y + 160))
                    else:
                        target_cell = get_cell(self.cell.x + 80, self.cell.y + 160)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
            if self.cell.x > 120:
                if self.cell.y > 40:
                    if get_cell(self.cell.x - 160, self.cell.y - 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x - 160, self.cell.y - 80))
                    else:
                        target_cell = get_cell(self.cell.x - 160, self.cell.y - 80)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                if self.cell.y < 520:
                    if get_cell(self.cell.x - 160, self.cell.y + 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x - 160, self.cell.y + 80))
                    else:
                        target_cell = get_cell(self.cell.x - 160, self.cell.y + 80)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
            if self.cell.x < 520:
                if self.cell.y > 40:
                    if get_cell(self.cell.x + 160, self.cell.y - 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x + 160, self.cell.y - 80))
                    else:
                        target_cell = get_cell(self.cell.x + 160, self.cell.y - 80)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                if self.cell.y < 520:
                    if get_cell(self.cell.x + 160, self.cell.y + 80).contains_piece == "":
                        self.moves.append(get_cell(self.cell.x + 160, self.cell.y + 80))
                    else:
                        target_cell = get_cell(self.cell.x + 160, self.cell.y + 80)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)

            self.validate_moves()
            self.validate_moves_binded()

    class Queen(Piece):

        def __init__(self, cell, color, image):
            super().__init__(cell, color, image)

        def find_moves(self):
            self.moves.clear()
            selected_piece.append(self)
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600:
                if get_cell(mark_x, mark_y + 80).contains_piece == "":
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.y != 600:
                            if self.color == "White" and target_cell == black_king_cell[0]:
                                white_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y + 80))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y + 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 40:
                if get_cell(mark_x, mark_y - 80).contains_piece == "":
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.y != 40:
                            if self.color == "White" and target_cell == black_king_cell[0]:
                                white_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y - 80))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x, target_cell.y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 40:
                if get_cell(mark_x - 80, mark_y).contains_piece == "":
                    mark_x = mark_x - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.x != 40:
                            if self.color == "White" and target_cell == black_king_cell[0]:
                                white_pieces_attack_field.append(get_cell(target_cell.x - 80, target_cell.y))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x - 80, target_cell.y))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 600:
                if get_cell(mark_x + 80, mark_y).contains_piece == "":
                    mark_x = mark_x + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.x != 600:
                            if self.color == "White" and target_cell == black_king_cell[0]:
                                white_pieces_attack_field.append(get_cell(target_cell.x + 80, target_cell.y))
                            else:
                                black_pieces_attack_field.append(get_cell(target_cell.x + 80, target_cell.y))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_x != 600 and mark_y != 40:
                if get_cell(mark_x + 80, mark_y - 80).contains_piece == "":
                    mark_x = mark_x + 80
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.x != 600 and target_cell.y != 40:
                            if self.color == "White" and target_cell == black_king_cell[0]:                                         # This block and so on adds to invalid moves move behind king in
                                white_pieces_attack_field.append(get_cell(black_king_cell[0].x + 80, black_king_cell[0].y - 80))    # the direction of attack of the checking piece
                            elif self.color == "Black" and target_cell == white_king_cell[0]:
                                black_pieces_attack_field.append(
                                    get_cell(white_king_cell[0].x + 80, white_king_cell[0].y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600 and mark_x != 40:
                if get_cell(mark_x - 80, mark_y + 80).contains_piece == "":
                    mark_x = mark_x - 80
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            if target_cell.x != 40 and target_cell.y != 600:
                                if self.color == "White" and target_cell == black_king_cell[0]:
                                    white_pieces_attack_field.append(
                                        get_cell(black_king_cell[0].x - 80, black_king_cell[0].y + 80))
                                elif self.color == "Black" and target_cell == white_king_cell[0]:
                                    black_pieces_attack_field.append(
                                        get_cell(white_king_cell[0].x - 80, white_king_cell[0].y + 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 40 and mark_x != 40:
                if get_cell(mark_x - 80, mark_y - 80).contains_piece == "":
                    mark_x = mark_x - 80
                    mark_y = mark_y - 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x - 80, mark_y - 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            if target_cell.x != 40 and target_cell.y != 40:
                                if self.color == "White" and target_cell == black_king_cell[0]:
                                    white_pieces_attack_field.append(
                                        get_cell(black_king_cell[0].x - 80, black_king_cell[0].y - 80))
                                elif self.color == "Black" and target_cell == white_king_cell[0]:
                                    black_pieces_attack_field.append(
                                        get_cell(white_king_cell[0].x - 80, white_king_cell[0].y - 80))
                    break
            mark_x = self.cell.x
            mark_y = self.cell.y
            while mark_y != 600 and mark_x != 600:
                if get_cell(mark_x + 80, mark_y + 80).contains_piece == "":
                    mark_x = mark_x + 80
                    mark_y = mark_y + 80
                    self.moves.append(get_cell(mark_x, mark_y))
                else:
                    target_cell = get_cell(mark_x + 80, mark_y + 80)
                    if target_cell.contains_piece != self.color:
                        self.moves.append(target_cell)
                        if target_cell.contains_piece != self.color:
                            self.moves.append(target_cell)
                            if target_cell.x != 600 and target_cell.y != 600:
                                if self.color == "White" and target_cell == black_king_cell[0]:
                                    white_pieces_attack_field.append(
                                        get_cell(black_king_cell[0].x + 80, black_king_cell[0].y + 80))
                                elif self.color == "Black" and target_cell == white_king_cell[0]:
                                    black_pieces_attack_field.append(
                                        get_cell(white_king_cell[0].x + 80, white_king_cell[0].y + 80))
                    break
            self.validate_moves()
            self.validate_moves_binded()

    class King(Piece):

        def __int__(self, cell, color, image):
            super().__init__(cell, color, image)

        def castle(self, side, event, arg):
            global white_turn
            white_turn = not white_turn
            self.first_turn = False
            Board.move(self.image, Board.coords(arg)[0] - Board.coords(self.image)[0], Board.coords(arg)[1] - Board.coords(self.image)[1])
            Board.itemconfig(self.cell.cell_id, fill=selected_piece[0].cell.color)
            self.cell.contains_piece = ""
            self.cell = get_cell(Board.coords(arg)[0], Board.coords(arg)[1])
            self.cell.contains_piece = self.color
            if self.color == "White" and side == "ks":
                pieces["white_rook_ks"].first_turn = False
                Board.move(pieces["white_rook_ks"].image, -160, 0)
                pieces["white_rook_ks"].cell.contains_piece = ""
                pieces["white_rook_ks"].cell = get_cell(pieces["white_rook_ks"].cell.x - 160, self.cell.y)
                pieces["white_rook_ks"].cell.contains_piece = pieces["white_rook_ks"].color
            if self.color == "White" and side == "qs":
                pieces["white_rook_qs"].first_turn = False
                Board.move(pieces["white_rook_qs"].image, 240, 0)
                pieces["white_rook_qs"].cell.contains_piece = ""
                pieces["white_rook_qs"].cell = get_cell(pieces["white_rook_qs"].cell.x + 240, self.cell.y)
                pieces["white_rook_qs"].cell.contains_piece = pieces["white_rook_qs"].color
            self.clear_marks()

        def find_moves(self):
            self.moves.clear()
            selected_piece.append(self)
            if self.cell.y != 40:
                if get_cell(self.cell.x, self.cell.y - 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x, self.cell.y - 80))
                elif get_cell(self.cell.x, self.cell.y - 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x, self.cell.y - 80))
            if self.cell.y != 600:
                if get_cell(self.cell.x, self.cell.y + 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x, self.cell.y + 80))
                elif get_cell(self.cell.x, self.cell.y + 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x, self.cell.y + 80))
            if self.cell.x != 40:
                if get_cell(self.cell.x - 80, self.cell.y).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y))
                elif get_cell(self.cell.x - 80, self.cell.y).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y))
            if self.cell.x != 600:
                if get_cell(self.cell.x + 80, self.cell.y).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y))
                elif get_cell(self.cell.x + 80, self.cell.y).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y))
            if self.cell.x != 40 and self.cell.y != 40:
                if get_cell(self.cell.x - 80, self.cell.y - 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y - 80))
                elif get_cell(self.cell.x - 80, self.cell.y - 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y - 80))
            if self.cell.x != 600 and self.cell.y != 600:
                if get_cell(self.cell.x + 80, self.cell.y + 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y + 80))
                elif get_cell(self.cell.x + 80, self.cell.y + 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y + 80))
            if self.cell.x != 40 and self.cell.y != 600:
                if get_cell(self.cell.x - 80, self.cell.y + 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y + 80))
                elif get_cell(self.cell.x - 80, self.cell.y + 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x - 80, self.cell.y + 80))
            if self.cell.x != 600 and self.cell.y != 40:
                if get_cell(self.cell.x + 80, self.cell.y - 80).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y - 80))
                elif get_cell(self.cell.x + 80, self.cell.y - 80).contains_piece != self.color:
                    self.moves.append(get_cell(self.cell.x + 80, self.cell.y - 80))
            if self.first_turn:
                if self.color == "White" and pieces["white_rook_qs"].first_turn == True and get_cell(self.cell.x - 80, self.cell.y).contains_piece == "" and get_cell(self.cell.x - 160, self.cell.y).contains_piece == "" and get_cell(self.cell.x - 240, self.cell.y):
                    self.moves.append(get_cell(self.cell.x - 160, self.cell.y))
                if self.color == "White" and pieces["white_rook_ks"].first_turn == True and get_cell(self.cell.x + 80, self.cell.y).contains_piece == "" and get_cell(self.cell.x + 160, self.cell.y).contains_piece == "":
                    self.moves.append(get_cell(self.cell.x + 160, self.cell.y))
            if self.color == "White":
                for piece_move in black_pieces_attack_field:
                    for king_move in self.moves:
                        if piece_move == king_move:
                            self.moves.remove(king_move)
            else:
                for piece_move in white_pieces_attack_field:
                    for king_move in self.moves:
                        if piece_move == king_move:
                            self.moves.remove(king_move)

        def show_moves(self, event):
            self.clear_marks()
            selected_piece.clear()
            selected_piece.append(self)
            Board.itemconfig(selected_piece[0].cell.cell_id, fill="#EAFC10")
            for cell in self.moves:
                if cell.contains_piece == "":
                    if self.first_turn and ((cell.x == 200 and cell.y == 40) or (cell.x == 200 and cell.y == 600)):
                        mark = cell.mark(event)
                        Board.tag_bind(mark, "<Button-1>", lambda event, arg=mark: self.castle("qs", event, arg))
                        marks.append(mark)
                    elif self.first_turn and ((cell.x == 520 and cell.y == 40) or (cell.x == 520 and cell.y == 600)):
                        mark = cell.mark(event)
                        Board.tag_bind(mark, "<Button-1>", lambda event, arg=mark: self.castle("ks", event, arg))
                        marks.append(mark)
                    else:
                        mark = cell.mark(event)
                        Board.tag_bind(mark, "<Button-1>", lambda event, arg=mark: self.move(event, arg))
                        marks.append(mark)
                else:
                    cell.marked = True
                    Board.itemconfig(cell.cell_id, fill=cell.__mark_color__)

    def get_cell(x_coord, y_coord):     # Returns cell with inputted coordinates
        return board_cells[x_coord, y_coord]

    def create_axis():
        Board.place(x=160, y=160)
        x_digits_l = 115
        x_digits_r = 825
        y_digits = 185
        x_letters = 190
        y_letters_u = 120
        y_letters_d = 820
        axis_font = font.Font(family="Arial", size=16)
        for i in range(1, 9):
            digit_left = Label(text="{}".format(i), font=axis_font, anchor="e", fg="#784504")
            digit_right = Label(text="{}".format(i), font=axis_font, anchor="e", fg="#784504")
            digit_left.place(x=x_digits_l, y=y_digits + (i - 1) * 80)
            digit_right.place(x=x_digits_r, y=y_digits + (i - 1) * 80)
            letter_up = Label(text="{}".format(chr(65 + i - 1)).upper(), font=axis_font, anchor="e", fg="#784504")
            letter_down = Label(text="{}".format(chr(65 + i - 1)).upper(), font=axis_font, anchor="e", fg="#784504")
            letter_up.place(x=x_letters + (i - 1) * 80, y=y_letters_u)
            letter_down.place(x=x_letters + (i - 1) * 80, y=y_letters_d)

    white_pieces = []
    black_pieces = []

    def place_pieces():
        for i in range(1, 9):
            image_id = Board.create_image(cells_list[i][7].x, cells_list[i][7].y, image=white_pawn_image)
            pieces["white_pawn_{}".format(i)] = Pawn(cells_list[i][7], "White", image_id)
            cells_list[i][7].contains_piece = "White"
            image_pieces[image_id] = pieces["white_pawn_{}".format(i)]
            image_id = Board.create_image(cells_list[i][2].x, cells_list[i][2].y, image=black_pawn_image)
            white_pieces.append(pieces["white_pawn_{}".format(i)])
            pieces["black_pawn_{}".format(i + 8)] = Pawn(cells_list[i][2], "Black", image_id)
            cells_list[i][2].contains_piece = "Black"
            image_pieces[image_id] = pieces["black_pawn_{}".format(i + 8)]
            black_pieces.append(pieces["black_pawn_{}".format(i + 8)])
        white_bishop_image_id = Board.create_image(cells_list[3][8].x, cells_list[3][8].y, image=white_bishop_image)
        pieces["white_bishop_bc"] = Bishop(cells_list[3][8], "White", white_bishop_image_id)
        image_pieces[white_bishop_image_id] = pieces["white_bishop_bc"]
        all_field_pieces_white.append(pieces["white_bishop_bc"])
        pieces["white_bishop_bc"].cell.contains_piece = "White"
        white_pieces.append(pieces["white_bishop_bc"])
        white_bishop_image_id = Board.create_image(cells_list[6][8].x, cells_list[6][8].y, image=white_bishop_image)
        pieces["white_bishop_wc"] = Bishop(cells_list[6][8], "White", white_bishop_image_id)
        pieces["white_bishop_wc"].cell.piece = pieces["white_bishop_wc"]
        image_pieces[white_bishop_image_id] = pieces["white_bishop_wc"]
        all_field_pieces_white.append(pieces["white_bishop_wc"])
        pieces["white_bishop_wc"].cell.contains_piece = "White"
        white_pieces.append(pieces["white_bishop_wc"])
        black_bishop_image_id = Board.create_image(cells_list[3][1].x, cells_list[3][1].y, image=black_bishop_image)
        pieces["black_bishop_wc"] = Bishop(cells_list[3][1], "Black", black_bishop_image_id)
        pieces["black_bishop_wc"].cell.piece = pieces["black_bishop_wc"]
        all_field_pieces_black.append(pieces["black_bishop_wc"])
        image_pieces[black_bishop_image_id] = pieces["black_bishop_wc"]
        pieces["black_bishop_wc"].cell.contains_piece = "Black"
        black_pieces.append(pieces["black_bishop_wc"])
        black_bishop_image_id = Board.create_image(cells_list[6][1].x, cells_list[6][1].y, image=black_bishop_image)
        pieces["black_bishop_bc"] = Bishop(cells_list[6][1], "Black", black_bishop_image_id)
        pieces["black_bishop_bc"].cell.piece = pieces["black_bishop_bc"]
        all_field_pieces_black.append(pieces["black_bishop_bc"])
        image_pieces[black_bishop_image_id] = pieces["black_bishop_bc"]
        pieces["black_bishop_bc"].cell.contains_piece = "Black"
        black_pieces.append(pieces["black_bishop_bc"])
        white_rook_image_id = Board.create_image(cells_list[1][8].x, cells_list[1][8].y, image=white_rook_image)
        pieces["white_rook_qs"] = Rook(cells_list[1][8], "White", white_rook_image_id)
        pieces["white_rook_qs"].cell.piece = pieces["white_rook_qs"]
        image_pieces[white_rook_image_id] = pieces["white_rook_qs"]
        all_field_pieces_white.append(pieces["white_rook_qs"])
        white_pieces.append(pieces["white_rook_qs"])
        pieces["white_rook_qs"].cell.contains_piece = "White"
        white_rook_image_id = Board.create_image(cells_list[8][8].x, cells_list[8][8].y, image=white_rook_image)
        pieces["white_rook_ks"] = Rook(cells_list[8][8], "White", white_rook_image_id)
        pieces["white_rook_ks"].cell.piece = pieces["white_rook_ks"]
        image_pieces[white_rook_image_id] = pieces["white_rook_ks"]
        all_field_pieces_white.append(pieces["white_rook_ks"])
        white_pieces.append(pieces["white_rook_ks"])
        pieces["white_rook_ks"].cell.contains_piece = "White"
        black_rook_image_id = Board.create_image(cells_list[1][1].x, cells_list[1][1].y, image=black_rook_image)
        pieces["black_rook_ks"] = Rook(cells_list[1][1], "Black", black_rook_image_id)
        pieces["black_rook_ks"].cell.piece = pieces["black_rook_ks"]
        image_pieces[black_rook_image_id] = pieces["black_rook_ks"]
        all_field_pieces_black.append(pieces["black_rook_ks"])
        pieces["black_rook_ks"].cell.contains_piece = "Black"
        black_pieces.append(pieces["black_rook_ks"])
        black_rook_image_id = Board.create_image(cells_list[8][1].x, cells_list[8][1].y, image=black_rook_image)
        pieces["black_rook_qs"] = Rook(cells_list[8][1], "Black", black_rook_image_id)
        pieces["black_rook_qs"].cell.piece = pieces["black_rook_qs"]
        image_pieces[black_rook_image_id] = pieces["black_rook_qs"]
        all_field_pieces_black.append(pieces["black_rook_qs"])
        black_pieces.append(pieces["black_rook_qs"])
        pieces["black_rook_qs"].cell.contains_piece = "Black"
        white_knight_image_id = Board.create_image(cells_list[2][8].x, cells_list[2][8].y, image=white_knight_image)
        pieces["white_knight_ks"] = Knight(cells_list[2][8], "White", white_knight_image_id)
        pieces["white_knight_ks"].cell.contains_piece = "White"
        pieces["white_knight_ks"].cell.piece = "White"
        image_pieces[white_knight_image_id] = pieces["white_knight_ks"]
        white_pieces.append(pieces["white_knight_ks"])
        white_knight_image_id = Board.create_image(cells_list[7][8].x, cells_list[7][8].y, image=white_knight_image)
        pieces["white_knight_qs"] = Knight(cells_list[7][8], "White", white_knight_image_id)
        pieces["white_knight_qs"].cell.contains_piece = "White"
        pieces["white_knight_qs"].cell.piece = "White"
        image_pieces[white_knight_image_id] = pieces["white_knight_qs"]
        white_pieces.append(pieces["white_knight_qs"])
        black_knight_image_id = Board.create_image(cells_list[2][1].x, cells_list[2][1].y, image=black_knight_image)
        pieces["black_knight_qs"] = Knight(cells_list[2][1], "Black", black_knight_image_id)
        pieces["black_knight_qs"].cell.contains_piece = "Black"
        pieces["black_knight_qs"].cell.piece = "Black"
        image_pieces[black_knight_image_id] = pieces["black_knight_qs"]
        black_pieces.append(pieces["black_knight_qs"])
        black_knight_image_id = Board.create_image(cells_list[7][1].x, cells_list[7][1].y, image=black_knight_image)
        pieces["black_knight_ks"] = Knight(cells_list[7][1], "Black", black_knight_image_id)
        pieces["black_knight_ks"].cell.contains_piece = "Black"
        pieces["black_knight_ks"].cell.piece = "Black"
        image_pieces[black_knight_image_id] = pieces["black_knight_ks"]
        black_pieces.append(pieces["black_knight_ks"])
        white_queen_image_id = Board.create_image(cells_list[4][8].x, cells_list[4][8].y, image=white_queen_image)
        pieces["white_queen"] = Queen(cells_list[4][8], "White", white_queen_image_id)
        pieces["white_queen"].cell.contains_piece = "White"
        pieces["white_queen"].cell.piece = "White"
        all_field_pieces_white.append(pieces["white_queen"])
        image_pieces[white_queen_image_id] = pieces["white_queen"]
        white_pieces.append(pieces["white_queen"])
        black_queen_image_id = Board.create_image(cells_list[4][1].x, cells_list[4][1].y, image=black_queen_image)
        pieces["black_queen"] = Queen(cells_list[4][1], "Black", black_queen_image_id)
        pieces["black_queen"].cell.contains_piece = "Black"
        pieces["black_queen"].cell.piece = "Black"
        all_field_pieces_black.append(pieces["black_queen"])
        black_pieces.append(pieces["black_queen"])
        image_pieces[black_queen_image_id] = pieces["black_queen"]
        white_king_image_id = Board.create_image(cells_list[5][8].x, cells_list[5][8].y, image=white_king_image)
        white_king_cell.append(cells_list[5][8])
        pieces["white_king"] = King(cells_list[5][8], "White", white_king_image_id)
        pieces["white_king"].cell.contains_piece = "White"
        pieces["white_king"].cell.piece = "White"
        pieces["white_king"].is_King = True
        image_pieces[white_king_image_id] = pieces["white_king"]
        white_pieces.append(pieces["white_king"])
        black_king_image_id = Board.create_image(cells_list[5][1].x, cells_list[5][1].y, image=black_king_image)
        black_king_cell.append(cells_list[5][1])
        pieces["black_king"] = King(cells_list[5][1], "Black", black_king_image_id)
        pieces["black_king"].cell.contains_piece = "Black"
        pieces["black_king"].cell.piece = "Black"
        pieces["black_king"].is_King = True
        image_pieces[black_king_image_id] = pieces["black_king"]
        black_pieces.append(pieces["black_king"])
    pieces = {}
    image_pieces = {}
    moves = []
    all_field_pieces_black = []
    all_field_pieces_white = []
    Window = Tk()
    Window.title("Chess")
    Window.geometry("960x960")
    Board = Canvas(width=640, height=640, bg="white")
    white_pawn_image = PhotoImage(file="./white_pawn_image.png")  # Images
    white_bishop_image = PhotoImage(file="./white_bishop_image.png")
    white_knight_image = PhotoImage(file="./white_knight_image.png")
    white_rook_image = PhotoImage(file="./white_rook_image.png")
    white_queen_image = PhotoImage(file="./white_queen_image.png")
    white_king_image = PhotoImage(file="./white_king_image.png")
    black_pawn_image = PhotoImage(file="./black_pawn_image.png")
    black_bishop_image = PhotoImage(file="./black_bishop_image.png")
    black_knight_image = PhotoImage(file="./black_knight_image.png")
    black_rook_image = PhotoImage(file="./black_rook_image.png")
    black_queen_image = PhotoImage(file="./black_queen_image.png")
    black_king_image = PhotoImage(file="./black_king_image.png")
    mark_image = PhotoImage(file="./mark.png")
    fill = {True: "#784504",
            False: "#E0CE88"}  # Black and white colors, respectively
    fill_flag = True
    board_cells = {}  # Dictionary containing cells numbers with coordinates. Essential for piece movement
    cells_list = [None]  # 2 level array, 1st index - column, 2nd - row
    for row in range(1, 9):
        fill_flag = not fill_flag
        cells_list.append([])
        cells_list[row].append(None)
        for col in range(1, 9):
            cell_id = Board.create_rectangle((row - 1) * 80, (col - 1) * 80, row * 80, col * 80, fill=fill[fill_flag])
            cell_obj = Cell((row - 1) * 80 + 40, (col - 1) * 80 + 40, cell_id, fill[fill_flag])
            fill_flag = not fill_flag
            board_cells[((row - 1) * 80 + 40, (col - 1) * 80 + 40)] = cell_obj
            cells_list[row].append(cell_obj)
            cell_ids_cells[cell_id] = cell_obj

    create_axis()
    place_pieces()
    for piece in white_pieces:
        piece.find_moves()
    Window.mainloop()

    #  Instead of creating new images for marks, I can try to simply create one in every cell and then just
    #   show / disable them when needed
