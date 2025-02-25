import tkinter as tk
from tkinter import ttk


class TotalScores:
    def __init__(self, scores_tab, game_setup, round_window, gang_window):
        self.scores_frame = scores_tab
        self.game_setup = game_setup
        self.round_window = round_window
        self.gang_window = gang_window
        self.current_round = 0
        self.rounds_data = []  # Store round data
        self.total_labels = []  # Store references to total labels

        self.player_names = self.game_setup.get_player_names()

        # Fill in player names automatically if none are entered
        if not self.player_names:
            self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
            print("Using default player names")

        self.create_table()

    def create_headers(self):
        # Create "Rounds" header in the tab
        rounds_label = tk.Label(
            self.scores_frame,
            text="Rounds",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black",  # Light theme colors
        )
        rounds_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Create player name headers in the tab
        for col, name in enumerate(self.player_names, start=1):
            header_label = tk.Label(
                self.scores_frame,
                text=name,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="black",  # Light theme colors
            )
            header_label.grid(row=0, column=col, padx=5, pady=5)

    def add_new_round(self):
        self.current_round += 1

        # Create round label
        round_label = tk.Label(
            self.scores_frame,
            text=f"Round {self.current_round}",
            bg="white",
            fg="black",  # Light theme colors
        )
        round_label.grid(row=self.current_round, column=0, padx=5, pady=2, sticky="w")

        # Get player names
        self.player_names = self.game_setup.get_player_names()
        if not self.player_names:
            self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

        round_entries = []

        # Create entry boxes for each player's score
        for col, _ in enumerate(self.player_names, start=1):
            score_entry = tk.Entry(self.scores_frame, width=10, bg="white", fg="black")
            score_entry.grid(row=self.current_round, column=col, padx=5, pady=2)
            round_entries.append(score_entry)

        # Store entries for later access
        self.rounds_data.append(round_entries)

        # Update total row position
        self.update_total_row()

        return round_entries

    def add_gang_row(self):
        # Add a row for Gang (special scoring in MahJong)
        gang_row = self.current_round + 1

        # Create gang label
        gang_label = tk.Label(
            self.scores_frame,
            text=f"Gang {self.current_round}",
            bg="white",
            fg="black",  # Light theme colors
        )
        gang_label.grid(row=gang_row, column=0, padx=5, pady=2, sticky="w")

        # Get player names
        self.player_names = self.game_setup.get_player_names()
        if not self.player_names:
            self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

        gang_entries = []

        # Create entry boxes for each player's gang score
        for col, _ in enumerate(self.player_names, start=1):
            gang_entry = tk.Entry(self.scores_frame, width=10, bg="white", fg="black")
            gang_entry.grid(row=gang_row, column=col, padx=5, pady=2)
            gang_entries.append(gang_entry)

        # Update total row position after adding gang
        self.update_total_row()

        return gang_entries

    def update_total_row(self):
        # Remove existing total labels
        for label in self.total_labels:
            if label.winfo_exists():
                label.destroy()
        self.total_labels = []

        # Calculate the row for total (after all rounds and gangs)
        total_row = self.current_round + 2

        # Create a new total row
        total_label = tk.Label(
            self.scores_frame,
            text="Total",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black",  # Light theme colors
        )
        total_label.grid(row=total_row, column=0, padx=5, pady=5, sticky="w")
        self.total_labels.append(total_label)

        self.player_names = self.game_setup.get_player_names()
        if not self.player_names:
            self.player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]

        # Add total score labels for each player
        for col, _ in enumerate(self.player_names, start=1):
            total_score = self.calculate_player_total(col - 1)  # 0-based index
            total_label = tk.Label(
                self.scores_frame,
                text=str(total_score),
                font=("Arial", 10, "bold"),
                bg="white",
                fg="black",  # Light theme colors
            )
            total_label.grid(row=total_row, column=col, padx=5, pady=5)
            self.total_labels.append(total_label)

    def calculate_player_total(self, player_idx):
        # Start with 0 total
        total = 0

        # Sum all round entries for this player
        for round_entries in self.rounds_data:
            if player_idx < len(round_entries):  # Ensure index is valid
                entry = round_entries[player_idx]
                try:
                    score = int(entry.get())
                    total += score
                except (ValueError, AttributeError):
                    # Skip if entry is empty or not a number
                    pass

        return total

    def create_table(self):
        # Configure the frame to match the light theme
        style = ttk.Style()
        style.configure("ScoresFrame.TFrame", background="white")
        style.configure(
            "Spreadsheet.TLabel",
            background="white",
            foreground="black",
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "Header.TLabel",
            background="white",
            foreground="black",
            font=("Arial", 10, "bold"),
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "Cell.TLabel",
            background="white",
            foreground="black",
            relief="solid",
            borderwidth=1,
            padding=5,
        )

        # Apply the style to the frame
        self.scores_frame.configure(style="ScoresFrame.TFrame")

        # Create table headers
        header_row = 0
        rounds_header = ttk.Label(
            self.scores_frame, text="Rounds", style="Header.TLabel"
        )
        rounds_header.grid(row=header_row, column=0, sticky="nsew", padx=1, pady=1)

        for i, name in enumerate(self.player_names):
            player_header = ttk.Label(
                self.scores_frame, text=name, style="Header.TLabel"
            )
            player_header.grid(
                row=header_row, column=i + 1, sticky="nsew", padx=1, pady=1
            )

        # Create total row
        total_row = 1  # Start with one row (you can add more as rounds are played)
        total_label = ttk.Label(self.scores_frame, text="Total", style="Header.TLabel")
        total_label.grid(row=total_row, column=0, sticky="nsew", padx=1, pady=1)

        for i in range(len(self.player_names)):
            total_value = ttk.Label(self.scores_frame, text="0", style="Cell.TLabel")
            total_value.grid(row=total_row, column=i + 1, sticky="nsew", padx=1, pady=1)

        # Configure all rows and columns to expand uniformly
        for i in range(10):  # Prepare for multiple rows
            self.scores_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):  # Columns: Round + 4 players
            self.scores_frame.grid_columnconfigure(i, weight=1)

        self.create_headers()
        self.add_new_round()  # Start with one round
        self.update_total_row()

    def get_round_data(self):
        # Return all round data as a list of lists
        result = []
        for round_entries in self.rounds_data:
            round_scores = []
            for entry in round_entries:
                try:
                    score = int(entry.get())
                    round_scores.append(score)
                except (ValueError, AttributeError):
                    round_scores.append(0)  # Default to 0 if empty or invalid
            result.append(round_scores)
        return result
