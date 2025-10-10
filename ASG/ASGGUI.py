import tkinter as tk
import os
from tkinter import filedialog, messagebox
from ArknightsSquadGenerator import load_operators_from_file, select_operators

class SquadGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arknights Squad Generator")
        self.operators = []

        self.root.geometry("1980x1080")
        self.root.state('zoomed')

        self.label = tk.Label(self.root, text="Arknights Squad Generator", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.squad_size_label = tk.Label(root, text="Select Squad Size")
        self.squad_size_label.pack()
        self.squad_size_entry = tk.Entry(root)
        self.squad_size_entry.pack()

        self.generate_button = tk.Button(self.root, text="Generate Squad", command=self.generate_squad, state=tk.DISABLED)
        self.generate_button.pack(pady=10)

        self.output_box = tk.Text(self.root, height=12, width=30)
        self.output_box.pack(pady=10)



        self.load_operators()

        
    def load_operators(self):

        base_dir = os.path.dirname(__file__)

        file_path = os.path.join(base_dir, 'data', 'Operators.txt')

        try:
            self.operators = load_operators_from_file(file_path)

            self.generate_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load characters: {e}")
            

    def generate_squad(self):
        try:
            squad_size = int(self.squad_size_entry.get())
            if squad_size <= 0:
                messagebox.showerror("Error", "Please enter a valid squad size greater than 0.")
                return
            if squad_size > 12:
                messagebox.showerror("Error", "Squad size exceeds the maximum capacity")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the squad size.")
            return
        # Generate squad based on your selection logic
        selected_squad = select_operators(self.operators, squad_size)
        # Display the squad in the text area
        self.output_box.delete(1.0, tk.END)
        for operator in selected_squad:
            self.output_box.insert(tk.END, f"{operator.name}\n")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = SquadGeneratorApp(root)
    root.mainloop()
