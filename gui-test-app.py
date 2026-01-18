import tkinter as tk
from tkinter import ttk


def work(user_text: str) -> str:
    result = []
    result.append("Входные данные:")
    result.append(user_text)
    result.append("")
    result.append("Результат обработки:")
    result.append(user_text.upper())
    result.append(f"Длина строки: {len(user_text)} символов")
    return "\n".join(result)


def on_run():
    text = entry.get()

    result = work(text)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state="disabled")


# ---------- GUI ----------

root = tk.Tk()
root.title("Simple Python GUI")
root.geometry("500x300")


# Очистка
def on_esc(event=None):
    entry.delete(0, tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

    entry.focus_set()


ESC_FOR_CLEAR = 0

if ESC_FOR_CLEAR:

    # Очистка по Esc
    root.bind("<Escape>", on_esc)

else:

    # закрытие по Esc
    root.bind("<Escape>", lambda e: root.destroy())



# запуск по Enter
root.bind("<Return>", lambda e: on_run())
    
# поле ввода
ttk.Label(root, text="Input:").pack(anchor="w", padx=10, pady=(10, 0))
entry = ttk.Entry(root)
entry.pack(fill="x", padx=10)

# кнопка
run_button = ttk.Button(root, text="Run", command=on_run)
run_button.pack(pady=10)

# поле вывода
ttk.Label(root, text="Output:").pack(anchor="w", padx=10)
output_text = tk.Text(root, height=10, state="disabled")
output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# фокус в поле ввода при старте
entry.focus_set()

root.mainloop()
