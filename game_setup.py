import tkinter as tk
from tkinter import ttk, messagebox
from total_scores import TotalScores
from round_window import RoundWindow
from gang_window import GangWindow


class GameSetup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mahjong Calculator")

        self.player_entries = []
        self.player_names = []
        self.round_manager = None
        self.tai_entry = None
        self.gang_entry = None
        self.angang_entry = None
        self.setup_theme()  # Calling theme setup before creating widgets
        self.create_notebook()

    def create_notebook(self):
        # Configure root window grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.setup_tab = ttk.Frame(self.notebook)
        self.scores_tab = ttk.Frame(self.notebook)

        # Configure the scores_tab to expand properly
        self.scores_tab.pack_propagate(
            False
        )  # Prevent the frame from shrinking to fit its children

        # Configure grid weights for the scores_tab
        for i in range(5):  # For 5 columns (Rounds + 4 players)
            self.scores_tab.grid_columnconfigure(i, weight=1)
        for i in range(10):  # Allow for up to 10 rows (adjust as needed)
            self.scores_tab.grid_rowconfigure(i, weight=1)

        # Add a canvas with scrollbar for the scores table
        scores_canvas = tk.Canvas(self.scores_tab, background="white")
        scrollbar = ttk.Scrollbar(
            self.scores_tab, orient="vertical", command=scores_canvas.yview
        )
        scores_canvas.configure(yscrollcommand=scrollbar.set)

        # Layout the canvas and scrollbar
        scrollbar.pack(side="right", fill="y")
        scores_canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas for the table
        self.scores_frame = ttk.Frame(scores_canvas)
        scores_canvas.create_window((0, 0), window=self.scores_frame, anchor="nw")

        # Configure the frame to update the canvas scroll region
        self.scores_frame.bind(
            "<Configure>",
            lambda e: scores_canvas.configure(scrollregion=scores_canvas.bbox("all")),
        )

        self.notebook.add(self.setup_tab, text="Game Setup")
        self.notebook.add(self.scores_tab, text="Total Scores")

    def setup_theme(self):
        # Set the light theme
        self.root.configure(bg="white")

        # Set default colors for common widgets
        self.root.option_add("*Label.Background", "white")
        self.root.option_add("*Label.Foreground", "black")
        self.root.option_add("*Entry.Background", "white")
        self.root.option_add("*Entry.Foreground", "black")
        self.root.option_add("*Button.Background", "#f0f0f0")
        self.root.option_add("*Button.Foreground", "black")

        # If using ttk
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")  # A theme that works well with customization

        # Configure ttk styles
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TButton", background="#f0f0f0", foreground="black")

    def set_round_manager(self, round_manager):
        self.round_manager = round_manager

    def input_box(self):
        text_label = tk.Label(self.setup_tab, text="Type Players Names Here")
        text_label.pack(pady=(10, 0))

        for i in range(4):
            entry = tk.Entry(self.setup_tab)
            entry.pack(pady=10)
            self.player_entries.append(entry)

    def get_player_names(self):
        # Return a list of player names
        names = []
        for entry in self.player_entries:
            name = entry.get().strip()
            if name:
                names.append(name)
            else:
                names.append(f"Player {len(names)+1}")
        return names

    def tai_amount(self):
        label = ttk.Label(
            self.setup_tab, text="How much is 1 台 ($)? (e.g 0.2, 0.5, 1)"
        )
        label.pack(pady=10)

        self.tai_entry = ttk.Entry(self.setup_tab)
        self.tai_entry.pack(pady=10)

    def get_tai_amount(self):
        try:
            return float(self.tai_entry.get())
        except (ValueError, TypeError):
            return 0.0

    def gang_amount(self):
        label = ttk.Label(self.setup_tab, text="How much is 杠 ($)? (e.g 0.2, 0.5, 1)")
        label.pack(pady=10)

        self.gang_entry = ttk.Entry(self.setup_tab)
        self.gang_entry.pack(pady=10)

    def get_gang_amount(self):
        try:
            return float(self.gang_entry.get())
        except (ValueError, TypeError):
            return 0.0

    def angang_amount(self):
        label = ttk.Label(
            self.setup_tab, text="How much is 暗杠 ($)? (e.g 0.2, 0.5, 1)"
        )
        label.pack(pady=10)

        self.angang_entry = ttk.Entry(self.setup_tab)
        self.angang_entry.pack(pady=10)

    def get_angang_amount(self):
        try:
            return float(self.angang_entry.get())
        except (ValueError, TypeError):
            return 0.0

    def validate_inputs(self):
        # Validate player names
        player_names = self.get_player_names()
        if len(set(player_names)) != 4 or "" in player_names:
            messagebox.showerror("Error", "Please enter 4 unique player names")
            return False

        # Validate numerical inputs
        try:
            tai = self.get_tai_amount()
            gang = self.get_gang_amount()
            angang = self.get_angang_amount()

            if any(x <= 0 for x in [tai, gang, angang]):
                messagebox.showerror("Error", "All amounts must be positive numbers")
                return False

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all amounts")
            return False

        return True

    def save_info(self):
        save_button = ttk.Button(
            self.setup_tab, text="Submit", command=self.handle_submit
        )
        save_button.pack(pady=10)

    def handle_submit(self):
        if self.validate_inputs():
            messagebox.showinfo("Success", "Game setup completed!")

    def open_round_window(self, total_scores):
        round_window_root = tk.Toplevel(self.root)
        round_window_root.title("Round Information")
        round_window_root.transient(self.root)
        round_window_root.grab_set()
        round_window_root.geometry("300x400")

        self.player_names = self.get_player_names()
        round_window = RoundWindow(
            round_window_root, self, total_scores, self.player_names
        )

        # Call UI methods to display elements
        round_window.who_won()
        round_window.tai_number()
        round_window.shooter_pay()
        round_window.who_threw()

        # Add submit button
        submit_button = ttk.Button(
            round_window_root,
            text="Submit Round",
            command=lambda: [round_window.submit_round(), round_window_root.destroy()],
        )
        submit_button.pack(pady=10)

    def open_gang_window(self):
        gang_window_root = tk.Toplevel(self.root)
        gang_window_root.title("杠 Info")
        gang_window_root.geometry("300x400")

        self.player_names = self.get_player_names()
        gang_handler = GangWindow(
            gang_window_root, self, total_scores, self.player_names
        )

        gang_handler.who_gang()
        gang_handler.gang_or_angang()

        submit_button = ttk.Button(
            gang_window_root,
            text="Submit",
            command=lambda: gang_handler.submit_gang_window(),
        )
        submit_button.pack(pady=10)

    def reset_inputs(self):
        for entry in self.player_entries:
            entry.delete(0, tk.END)

        self.tai_entry.delete(0, tk.END)
        self.gang_entry.delete(0, tk.END)
        self.angang_entry.delete(0, tk.END)

        button_frame = ttk.Frame(self.setup_tab)
        button_frame.pack(pady=10)

        reset_button = ttk.Button(
            button_frame, text="Reset All", command=self.reset_inputs
        )

        reset_button.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    game = GameSetup()
    total_scores = TotalScores(game.scores_tab, game, None, None)

    game.input_box()
    game.tai_amount()
    game.gang_amount()
    game.angang_amount()
    game.save_info()

    gang_button = ttk.Button(
        game.setup_tab, text="Click for 杠 / 暗杠", command=game.open_gang_window
    )
    gang_button.pack(pady=10)

    new_round_button = ttk.Button(
        game.setup_tab,
        text="New Round",
        command=lambda: game.open_round_window(total_scores),
    )
    new_round_button.pack(pady=10)

    game.root.mainloop()
