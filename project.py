import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time
import ttkbootstrap as tb  # Modern themes for Tkinter

# Word categories for Wordle and Anagram Solver
CATEGORIES = {
    "fruits": ["apple", "grape", "mango", "peach", "berry"],
    "animals": ["tiger", "zebra", "horse", "panda", "snake"],
    "countries": ["india", "china", "egypt", "japan", "brazil"]
}

class GameApp:


    def __init__(self, root):
        self.root = root
        self.root.title("Word Game Hub")
        self.root.geometry("500x500")
        self.root.configure(bg="#2E3440")  # Dark background color

        # Use ttkbootstrap theme
        self.style = tb.Style("cosmo")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        ttk.Label(self.root, text="🎮 Word Game Hub", font=("Arial", 18, "bold"), background="#2E3440", foreground="white").pack(pady=20)

        # Buttons for different games
        self.create_button("Wordle", self.play_wordle)
        self.create_button("Typing Speed Test", self.typing_speed_test)
        self.create_button("Anagram Solver", self.play_anagram_solver)  # New game
        self.create_button("Exit", self.root.quit)

    def create_button(self, text, command):
        """Create a stylish button with hover effect"""
        btn = ttk.Button(self.root, text=text, command=command, style="success.TButton")
        btn.pack(pady=10, ipadx=10, ipady=5, fill="x")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def play_wordle(self):
        self.clear_window()
        category = simpledialog.askstring("Wordle", "Choose a category: Fruits, Animals, Countries")

        if not category:
            self.create_main_menu()
            return

        category = category.strip().lower()

        if category not in CATEGORIES:
            messagebox.showerror("Error", "Invalid Category!")
            self.create_main_menu()
            return

        word_to_guess = random.choice(CATEGORIES[category]).upper()
        attempts = 6
        word_length = len(word_to_guess)

        # UI Elements
        ttk.Label(self.root, text=f"Category: {category.capitalize()} | Guess a {word_length}-letter word",
                  font=("Arial", 12), background="#2E3440", foreground="white").pack(pady=5)

        grid_frame = ttk.Frame(self.root)
        grid_frame.pack(pady=10)

        # Creating the 6x5 grid for guesses
        self.grid_labels = [[tk.Label(grid_frame, text=" ", font=("Arial", 18, "bold"), width=4, height=2, relief="ridge",
                                      anchor="center", bg="#3B4252", fg="white")
                            for _ in range(word_length)] for _ in range(attempts)]

        for row in range(attempts):
            for col in range(word_length):
                self.grid_labels[row][col].grid(row=row, column=col, padx=2, pady=2)

        self.current_attempt = 0
        self.word_to_guess = word_to_guess
        self.word_length = word_length
        self.attempts_left = attempts

        # Entry field
        self.entry = ttk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.check_guess)  # Bind Enter key

        # Submit button
        ttk.Button(self.root, text="Submit", command=self.check_guess, style="info.TButton").pack(pady=5)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_main_menu, style="secondary.TButton").pack(pady=5)

    def check_guess(self, event=None):  # `event=None` allows Enter key binding
        guess = self.entry.get().strip().upper()

        if len(guess) != self.word_length or not guess.isalpha():
            messagebox.showerror("Error", "Invalid word length or characters!")
            return

        if self.current_attempt >= 6:
            return  # No more attempts allowed

        # Update grid with guessed letters
        for i in range(self.word_length):
            letter = guess[i]
            label = self.grid_labels[self.current_attempt][i]
            label.config(text=letter)

            if letter == self.word_to_guess[i]:  # Correct letter & position
                label.config(bg="#4CAF50")  # Green
            elif letter in self.word_to_guess:  # Letter exists but wrong position
                label.config(bg="#FFC107")  # Yellow
            else:  # Letter not in the word
                label.config(bg="#757575")  # Gray

        self.current_attempt += 1
        self.entry.delete(0, tk.END)

        if guess == self.word_to_guess:
            messagebox.showinfo("Wordle", "🎉 Congratulations! You guessed the word.")
            self.create_main_menu()
        elif self.current_attempt == 6:
            messagebox.showinfo("Wordle", f"😢 Game Over! The correct word was: {self.word_to_guess}")
            self.create_main_menu()

    def typing_speed_test(self):
        self.clear_window()
        sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Python programming is fun and powerful.",
            "Speed and accuracy matter in typing tests.",
            "Artificial intelligence is shaping the future."
        ]
        sentence = random.choice(sentences)
        start_time = time.time()

        ttk.Label(self.root, text="Type this sentence:", font=("Arial", 12), background="#2E3440", foreground="white").pack(pady=5)
        ttk.Label(self.root, text=sentence, font=("Arial", 14), background="#2E3440", foreground="#88C0D0", wraplength=400).pack(pady=10)
        entry = ttk.Entry(self.root, font=("Arial", 14), width=50)
        entry.pack(pady=5)

        def check_typing():
            user_input = entry.get().strip()
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            words_per_minute = round((len(sentence.split()) / time_taken) * 60, 2)

            if user_input == sentence:
                messagebox.showinfo("Typing Test", f"🎉 Great job! You took {time_taken} seconds and typed at {words_per_minute} WPM.")
            else:
                messagebox.showinfo("Typing Test", "❌ Incorrect typing. Try again next time!")

            self.create_main_menu()

        ttk.Button(self.root, text="Submit", command=check_typing, style="info.TButton").pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.create_main_menu, style="secondary.TButton").pack(pady=5)

    def play_anagram_solver(self):
        """Anagram Solver game"""
        self.clear_window()

        category = random.choice(list(CATEGORIES.keys()))  # Choose a random category
        original_word = random.choice(CATEGORIES[category]).upper()  # Choose a random word
        scrambled_word = ''.join(random.sample(original_word, len(original_word)))  # Shuffle letters

        # UI Elements
        ttk.Label(self.root, text=f"Category: {category.capitalize()}", font=("Arial", 14), background="#2E3440", foreground="white").pack(pady=5)
        ttk.Label(self.root, text="Unscramble the word:", font=("Arial", 12), background="#2E3440", foreground="white").pack(pady=5)
        ttk.Label(self.root, text=scrambled_word, font=("Arial", 20, "bold"), background="#2E3440", foreground="#88C0D0").pack(pady=10)

        # Entry field
        self.entry = ttk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_anagram(original_word))  # Bind Enter key

        # Submit button
        ttk.Button(self.root, text="Submit", command=lambda: self.check_anagram(original_word), style="info.TButton").pack(pady=5)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_main_menu, style="secondary.TButton").pack(pady=5)

    def check_anagram(self, original_word):
        """Check if the entered word is the correct unscrambled word"""
        guess = self.entry.get().strip().upper()

        if guess == original_word:
            messagebox.showinfo("Anagram Solver", "🎉 Correct! Well done!")
        else:
            messagebox.showinfo("Anagram Solver", f"❌ Incorrect! The correct word was: {original_word}")

        self.create_main_menu()  # Return to main menu after showing result

    # Other games remain unchanged (Wordle, Typing Speed Test)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
