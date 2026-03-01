import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator - Dark Mode")
        self.root.geometry("400x600")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)
        
        # Dark mode color scheme
        self.bg_color = '#1e1e1e'
        self.button_bg = '#2d2d2d'
        self.button_hover = '#3d3d3d'
        self.text_color = '#ffffff'
        self.accent_color = '#0078d4'
        self.operator_color = '#ff6b35'
        self.display_bg = '#000000'
        
        self.setup_ui()
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.display_bg, relief=tk.RAISED, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Display label
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 24, 'bold'),
            fg=self.text_color,
            bg=self.display_bg,
            anchor='e',
            padx=20,
            pady=20
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button configuration
        button_config = {
            'font': ('Arial', 16, 'bold'),
            'relief': tk.RAISED,
            'bd': 2,
            'cursor': 'hand2'
        }
        
        # Button grid
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text in ['C', '⌫', '%', '/', '*', '-', '+', '=']:
                    if text == '=':
                        bg_color = self.accent_color
                        fg_color = self.text_color
                    elif text in ['/', '*', '-', '+']:
                        bg_color = self.operator_color
                        fg_color = self.text_color
                    else:
                        bg_color = self.button_bg
                        fg_color = self.text_color
                else:
                    bg_color = self.button_bg
                    fg_color = self.text_color
                
                btn = tk.Button(
                    button_frame,
                    text=text,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground=self.button_hover,
                    activeforeground=self.text_color,
                    command=lambda t=text: self.button_click(t),
                    **button_config
                )
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
                
                # Bind hover effects
                btn.bind('<Enter>', lambda e, b=btn: self.on_hover_enter(b))
                btn.bind('<Leave>', lambda e, b=btn: self.on_hover_leave(b, text))
        
        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def on_hover_enter(self, button):
        # Store original color if not already stored
        if not hasattr(button, 'original_bg'):
            button.original_bg = button['bg']
        button.configure(bg=self.button_hover)
    
    def on_hover_leave(self, button, text):
        # Restore to original color
        if hasattr(button, 'original_bg'):
            button.configure(bg=button.original_bg)
    
    def button_click(self, value):
        if value.isdigit():
            self.number_click(value)
        elif value == '.':
            self.decimal_click()
        elif value in ['+', '-', '*', '/', '%']:
            self.operator_click(value)
        elif value == '=':
            self.equals_click()
        elif value == 'C':
            self.clear_click()
        elif value == '⌫':
            self.backspace_click()
        elif value == '±':
            self.plus_minus_click()
    
    def number_click(self, number):
        if self.new_number:
            self.current = number
            self.new_number = False
        else:
            if self.current == "0":
                self.current = number
            else:
                self.current += number
        self.update_display()
    
    def decimal_click(self):
        if self.new_number:
            self.current = "0."
            self.new_number = False
        elif '.' not in self.current:
            self.current += '.'
        self.update_display()
    
    def operator_click(self, op):
        if self.operator and not self.new_number:
            self.equals_click()
        
        self.previous = self.current
        self.operator = op
        self.new_number = True
    
    def equals_click(self):
        if self.operator and self.previous:
            try:
                if self.operator == '+':
                    result = float(self.previous) + float(self.current)
                elif self.operator == '-':
                    result = float(self.previous) - float(self.current)
                elif self.operator == '*':
                    result = float(self.previous) * float(self.current)
                elif self.operator == '/':
                    if float(self.current) == 0:
                        self.current = "Error: Division by zero"
                        self.update_display()
                        return
                    result = float(self.previous) / float(self.current)
                elif self.operator == '%':
                    if float(self.current) == 0:
                        self.current = "Error: Division by zero"
                        self.update_display()
                        return
                    result = float(self.previous) % float(self.current)
                
                # Format result
                if result == int(result):
                    self.current = str(int(result))
                else:
                    self.current = str(result)
                
                self.previous = ""
                self.operator = ""
                self.new_number = True
                self.update_display()
                
            except Exception as e:
                self.current = "Error"
                self.update_display()
    
    def clear_click(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        self.update_display()
    
    def backspace_click(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def plus_minus_click(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
        self.update_display()
    
    def update_display(self):
        # Limit display length
        if len(self.current) > 12:
            if '.' in self.current:
                self.current = f"{float(self.current):.6g}"
            else:
                self.current = self.current[:12]
        
        self.display_var.set(self.current)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
