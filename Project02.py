# Simple Calculator using Tkinter



import tkinter as tk
from tkinter import font

def button_click(number):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))

def button_clear():
    entry.delete(0, tk.END)

def button_equal():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Create main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")
root.resizable(False, False)

# Custom font
custom_font = font.Font(size=14)

# Entry widget
entry = tk.Entry(root, width=15, borderwidth=5, font=custom_font)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# Define buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# Create and place buttons
for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(root, text=text, padx=20, pady=20, font=custom_font, 
                       command=button_equal, bg='#4CAF50', fg='white')
    elif text == 'C':
        btn = tk.Button(root, text=text, padx=20, pady=20, font=custom_font, 
                       command=button_clear, bg='#f44336', fg='white')
    else:
        btn = tk.Button(root, text=text, padx=20, pady=20, font=custom_font, 
                       command=lambda t=text: button_click(t))
    btn.grid(row=row, column=col, sticky="nsew")

# Configure row/column weights
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()