import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sys_consts import uvm_gen_config_table

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
        type = self.combo_priority.get().split(' ')[0]
        print(f"{type}1")
        
        # --- Data Validation ---
        if not name:
            messagebox.showwarning("Validation Error", "Name cannot be empty!", parent=self)
            return
        
        name_vld = self.check_format_name(name, type)
        if not name_vld:
            #messagebox.showwarning("Validation Error", "Name cannot be empty!", parent=self)
            return

        # Save results into a dictionary if validation passes
        self.result = {
            "name": name,
            "type": type
        }
        
        # Close the popup
        self.destroy()

    def check_format_name(self, name: str, type: str) -> bool:
        correct_suffix = uvm_gen_config_table.get(type).NAME_SUFFIX
        if not name.endswith(correct_suffix):
            msg = (f"{name} with type {type} does not end with expected suffix({correct_suffix})\n"
                   "Do you want to continue with current name?")
            response = messagebox.askyesno("Warning", msg)
            if response:
                return True
            else:
                return False
        return True