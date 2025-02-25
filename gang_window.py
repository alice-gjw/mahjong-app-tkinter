import tkinter as tk
from tkinter import ttk, messagebox


class GangWindow:
    def __init__(self, gang_window, game_setup, total_scores, player_names):
        self.gang_window = gang_window
        self.game_setup = game_setup
        self.total_scores = total_scores
        self.player_names = player_names

    def who_gang(self):
        label = tk.Label(self.gang_window, text="Who 杠?")
        label.pack(pady=5)

        self.gang_player_var = tk.StringVar()
        self.gang_dropdown = ttk.Combobox(
            self.gang_window, textvariable=self.gang_player_var
        )
        self.gang_dropdown["values"] = self.player_names
        self.gang_dropdown.pack(pady=(0, 10))

    def gang_or_angang(self):
        gang_frame = ttk.Frame(self.gang_window)
        gang_frame.pack(pady=0)

        self.gang_type_var = tk.IntVar(value=1)

        normal_check = ttk.Radiobutton(
            gang_frame, text="杠", variable=self.gang_type_var, value=1
        )
        normal_check.pack(side=tk.LEFT, padx=(0, 5))

        an_check = ttk.Radiobutton(
            gang_frame, text="暗杠", variable=self.gang_type_var, value=0
        )
        an_check.pack(side=tk.LEFT)

    def submit_gang_window(self):
        messagebox.showinfo("Success", "Entry Recorded")
