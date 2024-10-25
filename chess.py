import enum
import tkinter as tk
from tkinter import messagebox

# Enums for Color and Piece Types
class Color(enum.Enum):
    WHITE = 1
    BLACK = 0

class PieceType(enum.Enum):
    KING = 1
    QUEEN = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6

# Piece Class
class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def __str__(self):
        if self.color == Color.WHITE:
            if self.piece_type == PieceType.KING:
                return 'K'
            elif self.piece_type == PieceType.QUEEN:
                return 'Q'
            elif self.piece_type == PieceType.ROOK:
                return 'R'
            elif self.piece_type == PieceType.BISHOP:
                return 'B'
            elif self.piece_type == PieceType.KNIGHT:
                return 'N'
            elif self.piece_type == PieceType.PAWN:
                return 'P'
        else:
            if self.piece_type == PieceType.KING:
                return 'k'
            elif self.piece_type == PieceType.QUEEN:
                return 'q'
            elif self.piece_type == PieceType.ROOK:
                return 'r'
            elif self.piece_type == PieceType.BISHOP:
                return 'b'
            elif self.piece_type == PieceType.KNIGHT:
                return 'n'
            elif self.piece_type == PieceType.PAWN:
                return 'p'

# Board Class
class Board:
    def __init__(self):
        self.board = self.reset_board()
        self.turn = Color.WHITE  # White starts first

    # Set up initial board configuration
    def reset_board(self):
        board = [[None]*8 for _ in range(8)]

        # Pawns
        for i in range(8):
            board[1][i] = Piece(PieceType.PAWN, Color.WHITE)
            board[6][i] = Piece(PieceType.PAWN, Color.BLACK)

        # Rooks
        board[0][0] = Piece(PieceType.ROOK, Color.WHITE)
        board[0][7] = Piece(PieceType.ROOK, Color.WHITE)
        board[7][0] = Piece(PieceType.ROOK, Color.BLACK)
        board[7][7] = Piece(PieceType.ROOK, Color.BLACK)

        # Knights
        board[0][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        board[0][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        board[7][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        board[7][6] = Piece(PieceType.KNIGHT, Color.BLACK)

        # Bishops
        board[0][2] = Piece(PieceType.BISHOP, Color.WHITE)
        board[0][5] = Piece(PieceType.BISHOP, Color.WHITE)
        board[7][2] = Piece(PieceType.BISHOP, Color.BLACK)
        board[7][5] = Piece(PieceType.BISHOP, Color.BLACK)

        # Queens
        board[0][3] = Piece(PieceType.QUEEN, Color.WHITE)
        board[7][3] = Piece(PieceType.QUEEN, Color.BLACK)

        # Kings
        board[0][4] = Piece(PieceType.KING, Color.WHITE)
        board[7][4] = Piece(PieceType.KING, Color.BLACK)

        return board

    # Validate if the move is legal
    def is_valid_move(self, start, end):
        start_x = ord(start[0]) - 97
        start_y = int(start[1]) - 1
        end_x = ord(end[0]) - 97
        end_y = int(end[1]) - 1

        piece = self.board[start_y][start_x]
        target_piece = self.board[end_y][end_x]

        if piece is None:
            return False, "No piece at the start position."
        
        if piece.color != self.turn:
            return False, "It's not your turn."

        # Add basic move rules for each piece
        if piece.piece_type == PieceType.KING:
            if max(abs(start_x - end_x), abs(start_y - end_y)) > 1:
                return False, "Invalid move for the King."
        elif piece.piece_type == PieceType.QUEEN:
            # Allow both straight and diagonal moves (add full logic)
            pass
        elif piece.piece_type == PieceType.ROOK:
            # S
            pass
        elif piece.piece_type == PieceType.BISHOP:
            pass
        elif piece.piece_type == PieceType.KNIGHT:
            pass
        elif piece.piece_type == PieceType.PAWN:
            pass

        if target_piece is not None and target_piece.color == piece.color:
            return False, "You cannot capture your own piece."

      
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        return True, ""


    def move_piece(self, start, end):
        valid, msg = self.is_valid_move(start, end)
        if not valid:
            return False, msg

        start_x = ord(start[0]) - 97
        start_y = int(start[1]) - 1
        end_x = ord(end[0]) - 97
        end_y = int(end[1]) - 1

        self.board[end_y][end_x] = self.board[start_y][start_x]
        self.board[start_y][start_x] = None

        return True, "Move successful"

    def print_board(self, text_box):
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, '  a b c d e f g h\n')
        for i in range(8):
            text_box.insert(tk.END, str(i + 1) + ' ')
            for j in range(8):
                if self.board[i][j] is None:
                    text_box.insert(tk.END, '- ')
                else:
                    text_box.insert(tk.END, str(self.board[i][j]) + ' ')
            text_box.insert(tk.END, '\n')


def main():
    root = tk.Tk()
    root.title("Chess Game")

    board = Board()

    text_box = tk.Text(root, height=10, width=20)
    text_box.pack()

    start_label = tk.Label(root, text="Start position (e.g. a2):")
    start_label.pack()
    start_entry = tk.Entry(root)
    start_entry.pack()

    end_label = tk.Label(root, text="End position (e.g. a3):")
    end_label.pack()
    end_entry = tk.Entry(root)
    end_entry.pack()

    def reset_board():
        board.board = board.reset_board()
        board.print_board(text_box)

    def make_move():
        start = start_entry.get()
        end = end_entry.get()
        if len(start) != 2 or len(end) != 2:
            messagebox.showerror("Error", "Invalid input. Please enter a letter and a number.")
            return
        if start[0] < 'a' or start[0] > 'h' or end[0] < 'a' or end[0] > 'h':
            messagebox.showerror("Error", "Invalid input. Please enter a letter between a and h.")
            return
        if start[1] < '1' or start[1] > '8' or end[1] < '1' or end[1] > '8':
            messagebox.showerror("Error", "Invalid input. Please enter a number between 1 and 8.")
            return

        success, msg = board.move_piece(start, end)
        if not success:
            messagebox.showerror("Error", msg)
        else:
            board.print_board(text_box)

    reset_button = tk.Button(root, text="Reset Board", command=reset_board)
    reset_button.pack()

    move_button = tk.Button(root, text="Make Move", command=make_move)
    move_button.pack()

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack()

    board.print_board(text_box)

    root.mainloop()

if __name__ == "__main__":
    main()
