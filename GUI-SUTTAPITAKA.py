import tkinter as tk
from tkinter import ttk
import threading

from suttapitaka_model import suttapitaka_answer


def on_run():
    """
    Start processing user input in a background thread.
    """
    text = entry.get()

    # Show waiting message immediately
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Waiting.......")
    output_text.config(state="disabled")

    # Run long task in a separate thread
    thread = threading.Thread(
        target=run_long_task,
        args=(text,),
        daemon=True
    )
    thread.start()


def run_long_task(text):
    """
    Execute the long-running function and update the UI when done.
    """
    result = suttapitaka_answer(text)

    # Update UI safely from the main thread
    root.after(0, update_output, result)


def update_output(result):
    """
    Replace waiting message with the actual result.
    """
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state="disabled")


# ---------- GUI ----------

root = tk.Tk()
root.title("Simple Python GUI")
root.geometry("500x300")


def on_esc(event=None):
    """
    Clear input and output fields and return focus to input.
    """
    entry.delete(0, tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

    entry.focus_set()


ESC_FOR_CLEAR = 1

if ESC_FOR_CLEAR:
    # Clear fields on Esc
    root.bind("<Escape>", on_esc)
else:
    # Close application on Esc
    root.bind("<Escape>", lambda e: root.destroy())


# Run processing on Enter key
root.bind("<Return>", lambda e: on_run())

# Input label and field
ttk.Label(root, text="Input:").pack(anchor="w", padx=10, pady=(10, 0))
entry = ttk.Entry(root)
entry.pack(fill="x", padx=10)

# Run button
run_button = ttk.Button(root, text="Run", command=on_run)
run_button.pack(pady=10)

# Output label and text area
ttk.Label(root, text="Output:").pack(anchor="w", padx=10)
output_text = tk.Text(root, height=10, state="disabled")
output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Set focus to input field on startup
entry.focus_set()

root.mainloop()
