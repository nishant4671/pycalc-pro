import tkinter as tk
from calculator import PyCalc

class CalculatorApp:
    def __init__(self, root):
        self.calc = PyCalc()
        self.root = root
        self.root.title("PyCalc Pro")
        self.root.geometry("400x500")
        
        # Expression entry
        self.entry = tk.Entry(root, font=("Arial", 20), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.entry.insert(0, "2+3*4")
        
        # Result display
        self.result_var = tk.StringVar()
        tk.Label(root, textvariable=self.result_var, font=("Arial", 16), 
                anchor="e", bg="#f0f0f0").grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10)
        
        # Buttons
        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('^', 5, 2), ('+', 5, 3),
            ('(', 6, 0), (')', 6, 1), ('C', 6, 2), ('⌫', 6, 3),
            ('sqrt', 7, 0), ('sin', 7, 1), ('cos', 7, 2), ('tan', 7, 3)
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            btn = tk.Button(root, text=text, font=("Arial", 14),
                           command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Equal button (span all columns)
        equal_btn = tk.Button(root, text="=", font=("Arial", 14),
                            command=lambda: self.button_click("="))
        equal_btn.grid(row=8, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        
        # History display
        tk.Label(root, text="History:", font=("Arial", 12)).grid(row=9, column=0, sticky="w", padx=10)
        self.history_list = tk.Listbox(root, height=5, font=("Arial", 10))
        self.history_list.grid(row=10, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        
        # Configure grid weights
        for i in range(11):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
    
    def button_click(self, value):
        if value == "=":
            expr = self.entry.get()
            result = self.calc.calculate(expr)
            self.result_var.set(f"Result: {result}")
            self.update_history()
        elif value == "C":
            self.entry.delete(0, tk.END)
            self.result_var.set("")
        elif value == "⌫":  # Backspace functionality
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])
        else:
            self.entry.insert(tk.END, value)
    
    def update_history(self):
        self.history_list.delete(0, tk.END)
        for item in self.calc.history[-5:]:
            self.history_list.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
    