import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("800x400")

        self.init_start_screen()

    def init_start_screen(self):
        self.label = tk.Label(self.root, text="Choose number of players:")
        self.label.pack(pady=10)
        
        self.single_player_button = tk.Button(self.root, text="Single Player", command=self.single_player)
        self.single_player_button.pack(pady=5)
        
        self.two_player_button = tk.Button(self.root, text="Two Players", command=self.two_player)
        self.two_player_button.pack(pady=5)
    
    def single_player(self):
        self.num_players = 1
        self.setup_game()

    def two_player(self):
        self.num_players = 2
        self.setup_game()
    
    def setup_game(self):
        self.single_player_button.pack_forget()
        self.two_player_button.pack_forget()
        
        self.label.config(text="Enter the range for the number to be guessed:")
        
        self.range_frame = tk.Frame(self.root)
        self.range_frame.pack(pady=5)

        self.min_label = tk.Label(self.range_frame, text="Min:")
        self.min_label.pack(side=tk.LEFT, padx=5)
        
        self.min_entry = tk.Entry(self.range_frame, width=5)
        self.min_entry.pack(side=tk.LEFT, padx=5)
        
        self.max_label = tk.Label(self.range_frame, text="Max:")
        self.max_label.pack(side=tk.LEFT, padx=5)
        
        self.max_entry = tk.Entry(self.range_frame, width=5)
        self.max_entry.pack(side=tk.LEFT, padx=5)
        
        self.set_range_button = tk.Button(self.root, text="Set Range", command=self.set_range)
        self.set_range_button.pack(pady=10)
    
    def set_range(self):
        try:
            self.min_value = int(self.min_entry.get())
            self.max_value = int(self.max_entry.get())
            if self.min_value >= self.max_value:
                raise ValueError("Min should be less than Max.")
        except ValueError as e:
            messagebox.showerror("Invalid input", f"Please enter a valid range.\nError: {e}")
            return
        
        self.target_number = random.randint(self.min_value, self.max_value)
        self.current_player = 1
        self.guess_count = 0
        self.guess_history = {1: [], 2: []}
        
        self.range_frame.pack_forget()
        self.set_range_button.pack_forget()
        
        if self.num_players == 1:
            self.label.config(text="Enter your guess:")
        else:
            self.label.config(text="Player 1, enter your guess:")
        
        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=5)
        
        self.guess_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.history_frame)
        self.scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.player1_label = tk.Label(self.scrollable_frame, text="Player 1 guesses:")
        self.player1_label.grid(row=0, column=0, padx=10, pady=5)

        if self.num_players == 2:
            self.player2_label = tk.Label(self.scrollable_frame, text="Player 2 guesses:")
            self.player2_label.grid(row=0, column=1, padx=10, pady=5)
            self.scrollable_frame.grid_columnconfigure(1, weight=1)

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.center_labels()

    def center_labels(self):
        self.player1_label.grid(row=0, column=0, sticky="ew")
        if self.num_players == 2:
            self.player2_label.grid(row=0, column=1, sticky="ew")
    
    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number.")
            return
        
        self.guess_entry.delete(0, tk.END)
        self.guess_count += 1
        
        if guess == self.target_number:
            result = "Correct"
            self.result_label.config(text=f"Player {self.current_player}: {result}!")
            messagebox.showinfo("Congratulations", f"Player {self.current_player} wins! The number was {self.target_number}. It took {self.guess_count} guesses.")
            self.reset_game()
            return
        elif guess < self.target_number:
            result = "Too low"
            self.result_label.config(text=f"Player {self.current_player}: {result}!")
        else:
            result = "Too high"
            self.result_label.config(text=f"Player {self.current_player}: {result}!")
        
        self.guess_history[self.current_player].append((guess, result))
        self.update_history()
        
        if self.num_players == 2:
            self.switch_player()
    
    def update_history(self):
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget not in [self.player1_label] and (self.num_players == 1 or widget not in [self.player2_label]):
                widget.destroy()
                
        for index, (guess, result) in enumerate(self.guess_history[1]):
            tk.Label(self.scrollable_frame, text=f"{guess} ({result})").grid(row=index+1, column=0, padx=10, pady=2, sticky="ew")
        
        if self.num_players == 2:
            for index, (guess, result) in enumerate(self.guess_history[2]):
                tk.Label(self.scrollable_frame, text=f"{guess} ({result})").grid(row=index+1, column=1, padx=10, pady=2, sticky="ew")
    
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        self.label.config(text=f"Player {self.current_player}, enter your guess:")
    
    def reset_game(self):
        self.history_frame.pack_forget()
        self.result_label.pack_forget()
        self.guess_button.pack_forget()
        self.guess_entry.pack_forget()
        self.label.pack_forget()
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.init_start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
