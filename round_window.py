import tkinter as tk
from tkinter import ttk, messagebox


class RoundWindow:
    def __init__(self, round_window, game_setup, total_scores, player_names):
        self.round_window = round_window
        self.game_setup = game_setup
        self.total_scores = total_scores
        self.player_names = player_names

    def who_won(self):
        # Create a dropdown with player names for winner selection
        winner_label = tk.Label(self.round_window, text="Who won this round?")
        winner_label.pack(pady=(20, 0))

        # Storing UI elements as instance variables
        self.winner_var = tk.StringVar()
        self.winner_dropdown = ttk.Combobox(
            self.round_window, textvariable=self.winner_var
        )
        self.winner_dropdown["values"] = self.player_names
        self.winner_dropdown.pack(pady=10)

    def tai_number(self):
        label = ttk.Label(self.round_window, text="How many 台?")
        label.pack(pady=0)

        self.tai_entry = ttk.Entry(self.round_window)
        self.tai_entry.pack(pady=10)

    def shooter_pay(self):
        # Create a frame to hold the checkbuttons side by side
        shooter_frame = ttk.Frame(self.round_window)
        shooter_frame.pack(pady=20)

        # Create label
        shooter_label = ttk.Label(shooter_frame, text="Shooter pay?")
        shooter_label.pack(side=tk.LEFT, padx=(0, 10))

        # Create a variable to track selection (0 for No, 1 for Yes)
        self.shooter_var = tk.IntVar(value=0)  # Default to No (0)

        # Create Yes checkbutton
        yes_check = ttk.Radiobutton(
            shooter_frame, text="Yes", variable=self.shooter_var, value=1
        )
        yes_check.pack(side=tk.LEFT, padx=(0, 5))

        # Create No checkbutton
        no_check = ttk.Radiobutton(
            shooter_frame, text="No", variable=self.shooter_var, value=0
        )
        no_check.pack(side=tk.LEFT)

    def who_threw(self):
        player_names = self.game_setup.get_player_names()
        all_options = player_names + ["自摸"]

        threw_label = tk.Label(self.round_window, text="Who threw?")
        threw_label.pack(pady=0)

        self.threw_var = tk.StringVar()
        self.threw_dropdown = ttk.Combobox(
            self.round_window, textvariable=self.threw_var
        )
        self.threw_dropdown["values"] = all_options
        self.threw_dropdown.pack(pady=10)

    def submit_round(self):
        self.total_scores.add_new_round()
        messagebox.showinfo("Success", "Round Submitted")
