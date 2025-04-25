import tkinter as tk
from tkinter import ttk
import math
from tkinter.font import Font
from PIL import Image, ImageDraw
import io

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.resizable(True, True)
        self.root.minsize(250, 350)
        
        # Define color themes
        self.themes = {
            'Tokyo Night': {
                'bg': '#1A1B26',
                'display_bg': '#24283B',
                'display_fg': '#7AA2F7',
                'numbers': '#414868',
                'operations': '#BB9AF7',
                'special': '#7AA2F7',
                'equals': '#9ECE6A',
                'clear': '#F7768E'
            },
            'Dracula': {
                'bg': '#282A36',
                'display_bg': '#44475A',
                'display_fg': '#BD93F9',
                'numbers': '#6272A4',
                'operations': '#FF79C6',
                'special': '#8BE9FD',
                'equals': '#50FA7B',
                'clear': '#FF5555'
            },
            'Nord': {
                'bg': '#2E3440',
                'display_bg': '#3B4252',
                'display_fg': '#88C0D0',
                'numbers': '#4C566A',
                'operations': '#81A1C1',
                'special': '#8FBCBB',
                'equals': '#A3BE8C',
                'clear': '#BF616A'
            }
        }
        
        self.current_theme = 'Tokyo Night'
        theme = self.themes[self.current_theme]
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg=theme['bg'])
        self.main_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Create and set the calculator icon
        self.create_icon()
        
        # History for calculations
        self.history = []
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', 
                           font=('Segoe UI', 10, 'bold'),
                           padding=5)
        self.style.configure('TEntry', 
                           font=('Segoe UI', 12),
                           padding=5)
        
        # Create theme switcher button
        self.theme_button = tk.Button(self.main_frame, 
                                    text="🎨", 
                                    font=('Segoe UI', 12),
                                    bg=theme['special'],
                                    fg='white',
                                    relief=tk.FLAT,
                                    command=self.switch_theme)
        self.theme_button.grid(row=0, column=0, padx=2, pady=2, sticky="nw")
        
        # Create history display
        self.history_display = tk.Text(self.main_frame, height=2, width=25, 
                                     font=('Segoe UI', 9), 
                                     bg=theme['display_bg'],
                                     fg=theme['display_fg'], 
                                     relief=tk.FLAT)
        self.history_display.grid(row=0, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")
        self.history_display.config(state=tk.DISABLED)
        
        # Create main display
        self.display = ttk.Entry(self.main_frame, width=20, justify="right", 
                               font=('Segoe UI', 16))
        self.display.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
        
        # Create buttons with custom colors and hover effects
        self.create_button("√", 2, 0, theme['special'], "sqrt")
        self.create_button("x²", 2, 1, theme['special'], "square")
        self.create_button("π", 2, 2, theme['special'], "pi")
        self.create_button("C", 2, 3, theme['clear'], "clear")
        
        self.create_button("7", 3, 0, theme['numbers'])
        self.create_button("8", 3, 1, theme['numbers'])
        self.create_button("9", 3, 2, theme['numbers'])
        self.create_button("/", 3, 3, theme['operations'])
        
        self.create_button("4", 4, 0, theme['numbers'])
        self.create_button("5", 4, 1, theme['numbers'])
        self.create_button("6", 4, 2, theme['numbers'])
        self.create_button("*", 4, 3, theme['operations'])
        
        self.create_button("1", 5, 0, theme['numbers'])
        self.create_button("2", 5, 1, theme['numbers'])
        self.create_button("3", 5, 2, theme['numbers'])
        self.create_button("-", 5, 3, theme['operations'])
        
        self.create_button("0", 6, 0, theme['numbers'])
        self.create_button(".", 6, 1, theme['numbers'])
        self.create_button("=", 6, 2, theme['equals'])
        self.create_button("+", 6, 3, theme['operations'])

    def switch_theme(self):
        themes = list(self.themes.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name):
        theme = self.themes[theme_name]
        self.root.configure(bg=theme['bg'])
        self.main_frame.configure(bg=theme['bg'])
        self.history_display.configure(bg=theme['display_bg'], fg=theme['display_fg'])
        self.theme_button.configure(bg=theme['special'])
        
        # Update all buttons
        for child in self.main_frame.winfo_children():
            if isinstance(child, tk.Button):
                if child['text'] in ['√', 'x²', 'π']:
                    child.configure(bg=theme['special'])
                elif child['text'] in ['+', '-', '*', '/']:
                    child.configure(bg=theme['operations'])
                elif child['text'] == '=':
                    child.configure(bg=theme['equals'])
                elif child['text'] == 'C':
                    child.configure(bg=theme['clear'])
                else:
                    child.configure(bg=theme['numbers'])

    def create_icon(self):
        # Create a new image with a white background
        img = Image.new('RGB', (64, 64), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw calculator body
        draw.rectangle([10, 10, 54, 54], fill='#7AA2F7', outline='#7AA2F7')
        draw.rectangle([15, 15, 49, 49], fill='#1A1B26', outline='#7AA2F7')
        
        # Draw calculator buttons
        for i in range(3):
            for j in range(3):
                draw.rectangle([20 + i*10, 20 + j*10, 25 + i*10, 25 + j*10], 
                             fill='#BB9AF7', outline='#BB9AF7')
        
        # Convert to PhotoImage
        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        img_data.seek(0)
        
        # Create PhotoImage and set as icon
        icon = tk.PhotoImage(data=img_data.getvalue())
        self.root.iconphoto(True, icon)

    def create_button(self, text, row, column, color, command=None):
        button = tk.Button(self.main_frame, 
                          text=text,
                          font=('Segoe UI', 10, 'bold'),
                          bg=color,
                          fg='white',
                          relief=tk.FLAT,
                          borderwidth=0,
                          command=lambda: self.button_click(text, command))
        button.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")
        
        # Add hover effect
        button.bind("<Enter>", lambda e: button.configure(bg=self.lighten_color(color)))
        button.bind("<Leave>", lambda e: button.configure(bg=color))

    def lighten_color(self, color):
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Lighten the color
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_history(self, expression, result):
        self.history.append(f"{expression} = {result}")
        if len(self.history) > 2:
            self.history.pop(0)
        
        self.history_display.config(state=tk.NORMAL)
        self.history_display.delete(1.0, tk.END)
        for item in self.history:
            self.history_display.insert(tk.END, item + "\n")
        self.history_display.config(state=tk.DISABLED)

    def button_click(self, text, command=None):
        if command == "clear":
            self.display.delete(0, tk.END)
        elif command == "sqrt":
            try:
                result = math.sqrt(float(self.display.get()))
                self.update_history(f"√({self.display.get()})", result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif command == "square":
            try:
                result = float(self.display.get()) ** 2
                self.update_history(f"({self.display.get()})²", result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif command == "pi":
            self.display.insert(tk.END, str(math.pi))
        elif text == "=":
            try:
                expression = self.display.get()
                result = eval(expression)
                self.update_history(expression, result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    
    # Configure grid weights to make buttons expand
    for i in range(7):
        calculator.main_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        calculator.main_frame.grid_columnconfigure(i, weight=1)
        
    root.mainloop() 