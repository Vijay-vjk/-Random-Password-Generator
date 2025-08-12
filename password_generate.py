
import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string

SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
AMBIGUOUS = "Il1O0"

def build_charset(lower, upper, digits, symbols, exclude_ambiguous):
    charset = ""
    if lower: charset += string.ascii_lowercase
    if upper: charset += string.ascii_uppercase
    if digits: charset += string.digits
    if symbols: charset += SYMBOLS
    if exclude_ambiguous:
        charset = "".join(ch for ch in charset if ch not in AMBIGUOUS)
    return charset

def ensure_inclusion(chars_list, required_sets):
    for req in required_sets:
        if not any(c in req for c in chars_list):
            idx = secrets.randbelow(len(chars_list))
            chars_list[idx] = secrets.choice(req)

def generate(length, lower, upper, digits, symbols, exclude_ambiguous):
    required_sets = []
    if lower: required_sets.append(string.ascii_lowercase)
    if upper: required_sets.append(string.ascii_uppercase)
    if digits: required_sets.append(string.digits)
    if symbols: required_sets.append(SYMBOLS)

    charset = build_charset(lower, upper, digits, symbols, exclude_ambiguous)
    if not charset:
        raise ValueError("Choose at least one character type.")

    if length < len(required_sets):
        raise ValueError(f"Length must be at least {len(required_sets)} to include each selected type.")

    chars = [secrets.choice(charset) for _ in range(length)]
    if required_sets:
        ensure_inclusion(chars, required_sets)
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

def estimate_strength(pwd):
    score = 0
    if len(pwd) >= 8: score += 1
    if len(pwd) >= 12: score += 1
    types = 0
    if any(c.islower() for c in pwd): types += 1
    if any(c.isupper() for c in pwd): types += 1
    if any(c.isdigit() for c in pwd): types += 1
    if any(c in SYMBOLS for c in pwd): types += 1
    score += (types - 1)
    if score <= 1: return "Weak"
    if score == 2: return "Moderate"
    if score >= 3: return "Strong"
    return "Unknown"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Password Generator")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        pad = 8
        frm = ttk.Frame(self, padding=pad)
        frm.grid(row=0, column=0, sticky="nsew")

        # Length
        ttk.Label(frm, text="Length:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        length_spin = ttk.Spinbox(frm, from_=4, to=128, textvariable=self.length_var, width=6)
        length_spin.grid(row=0, column=1, sticky="w")

        # Options
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(frm, text="Lowercase", variable=self.lower_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(frm, text="Uppercase", variable=self.upper_var).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(frm, text="Digits", variable=self.digits_var).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(frm, text="Symbols", variable=self.symbols_var).grid(row=2, column=1, sticky="w")
        ttk.Checkbutton(frm, text="Exclude ambiguous (Il1O0)", variable=self.exclude_var).grid(row=3, column=0, columnspan=2, sticky="w")

        # Generate button
        gen_btn = ttk.Button(frm, text="Generate", command=self.on_generate)
        gen_btn.grid(row=4, column=0, pady=(pad,0), sticky="w")

        # Copy button
        copy_btn = ttk.Button(frm, text="Copy to Clipboard", command=self.on_copy)
        copy_btn.grid(row=4, column=1, pady=(pad,0), sticky="e")

        # Output
        ttk.Label(frm, text="Password:").grid(row=5, column=0, sticky="w", pady=(pad,0))
        self.pwd_var = tk.StringVar()
        self.pwd_entry = ttk.Entry(frm, textvariable=self.pwd_var, width=40, font=("Consolas", 10))
        self.pwd_entry.grid(row=6, column=0, columnspan=2, sticky="w")

        # Strength
        ttk.Label(frm, text="Strength:").grid(row=7, column=0, sticky="w", pady=(6,0))
        self.str_var = tk.StringVar(value="N/A")
        ttk.Label(frm, textvariable=self.str_var).grid(row=7, column=1, sticky="w", pady=(6,0))

        # Fill a default password on start
        self.on_generate()

    def on_generate(self):
        length = self.length_var.get()
        try:
            pwd = generate(
                length,
                lower=self.lower_var.get(),
                upper=self.upper_var.get(),
                digits=self.digits_var.get(),
                symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_var.get()
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.pwd_var.set(pwd)
        self.str_var.set(estimate_strength(pwd))

    def on_copy(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        # Use Tkinter clipboard
        self.clipboard_clear()
        self.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
