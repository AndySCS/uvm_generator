import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class InputPopup(tk.Toplevel):
    def __init__(self, parent, types):
        super().__init__(parent)
        
        self.title("Enter Details")
        self.geometry("300x250")
        
        # Make this popup "modal" (blocks interaction with main window)
        self.grab_set()
        
        # Variable placeholders to store the final data
        self.result = None
        
        # --- Form Fields ---
        
        # 1. Text Input (String)
        tk.Label(self, text="Item Name :").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.entry_name = tk.Entry(self)
        self.entry_name.pack(fill=tk.X, padx=10, pady=2)
        
        # 2. Dropdown/Combobox Input (Selection)
        tk.Label(self, text="Component Type:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.combo_priority = ttk.Combobox(self, values=types, state="readonly")
        self.combo_priority.pack(fill=tk.X, padx=10, pady=2)
        self.combo_priority.set(types[0] if types else "") # Default value
        
        # --- Submit Button ---
        btn_submit = tk.Button(self, text="Submit", command=self.submit, bg="#4CAF50", fg="white")
        btn_submit.pack(pady=20)

    def submit(self):
        name = self.entry_name.get().strip()
        priority = self.combo_priority.get()
        
        # --- Data Validation ---
        if not name:
            messagebox.showwarning("Validation Error", "Name cannot be empty!", parent=self)
            return

        # Save results into a dictionary if validation passes
        self.result = {
            "name": name,
            "type": priority
        }
        
        # Close the popup
        self.destroy()