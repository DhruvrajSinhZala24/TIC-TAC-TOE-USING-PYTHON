import tkinter as tk
from tkinter import messagebox

def check_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(all(cell != "" for cell in row) for row in board)

def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, "O"):  # AI wins
        return 10 - depth
    if check_winner(board, "X"):  # Player wins
        return depth - 10
    if is_full(board):  # Draw
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def best_move():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False, -float("inf"), float("inf"))
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = "O"
        buttons[move[0]][move[1]].config(text="O", state=tk.DISABLED, bg="#FF5757", fg="white")
        check_game_state()

def check_game_state():
    if check_winner(board, "X"):
        messagebox.showinfo("Game Over", "You Win!")
        restart_game()
    elif check_winner(board, "O"):
        messagebox.showinfo("Game Over", "AI Wins!")
        restart_game()
    elif is_full(board):
        messagebox.showinfo("Game Over", "It's a Draw!")
        restart_game()

def restart_game():
    answer = messagebox.askquestion("Play Again?", "Do you want to play a new game?")
    if answer == "yes":
        reset_board()
    else:
        root.quit()

def reset_board():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=tk.NORMAL, bg="#F0F0F0")

def on_click(row, col):
    if board[row][col] == "":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state=tk.DISABLED, bg="#57A0FF", fg="white")
        check_game_state()
        root.after(200, best_move)

root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg="#2C3E50")

board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=20)

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(frame, text="", font=("Arial", 24, "bold"), width=5, height=2, bg="#F0F0F0", fg="black",
                                  relief=tk.RAISED, borderwidth=3, command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

title_label = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 20, "bold"), bg="#2C3E50", fg="white")
title_label.pack()

root.mainloop()