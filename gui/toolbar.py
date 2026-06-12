import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class toolbar(tk.Menu):
    def __init__(self, app_instance):
        super().__init__(app_instance)

        # --- 1. Top Menu Bar (Standard Software Practice) ---
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        self.add_cascade(label="File", menu=filemenu)

#        # --- 2. The Toolbar Container ---
#        # bd=1 and relief=tk.RAISED give it a slight professional border if desired, 
#        # but a flat frame with a separator line looks cleaner and more modern.
#        toolbar = tk.Frame(self.root, bg="#f0f0f0", height=30)
#        # Pack at the very top, stretching horizontally
#        toolbar.pack(side=tk.TOP, fill=tk.X)
#
#        # --- 3. Adding Elements to the Toolbar ---
#        
#        # Note: In a real app, use tk.PhotoImage(file="icon.png") for actual graphics.
#        # We will use text symbols like "💾", "➕", "❌" here as lightweight mock icons.
#        
#        # Button 1: New File
#        btn_new = tk.Button(toolbar, text="➕", font=("Arial", 10), command=self.on_new,
#                            bg="#f0f0f0", relief=tk.FLAT, overrelief=tk.RAISED, padx=5, pady=2)
#        btn_new.pack(side=tk.LEFT, padx=2, pady=2)
#        self.add_tooltip(btn_new, "Create New File")
#
#        # Button 2: Save File
#        btn_save = tk.Button(toolbar, text="💾", font=("Arial", 10), command=self.on_save,
#                             bg="#f0f0f0", relief=tk.FLAT, overrelief=tk.RAISED, padx=5, pady=2)
#        btn_save.pack(side=tk.LEFT, padx=2, pady=2)
#        self.add_tooltip(btn_save, "Save Document")
#
#        # --- Toolbar Separator / Divider Line ---
#        # Separates different button groups (like file actions vs editing actions)
#        sep = ttk.Separator(toolbar, orient=tk.VERTICAL)
#        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=3)
#
#        # Button 3: Delete Item
#        btn_delete = tk.Button(toolbar, text="❌", font=("Arial", 10), command=self.on_delete,
#                               bg="#f0f0f0", relief=tk.FLAT, overrelief=tk.RAISED, padx=5, pady=2)
#        btn_delete.pack(side=tk.LEFT, padx=2, pady=2)
#        self.add_tooltip(btn_delete, "Delete Selected Item")
#
#        # --- 4. Bottom Divider Line ---
#        # Visually cuts off the toolbar from the rest of the application workspace
#        divider = ttk.Separator(self.root, orient=tk.HORIZONTAL)
#        divider.pack(side=tk.TOP, fill=tk.X)
#
#        # --- 5. Main Workspace Area ---
#        self.workspace = tk.Text(self.root, wrap=tk.WORD, bd=0, font=("Consolas", 11))
#        self.workspace.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
#
#    # --- Button Functions ---
#    def on_new(self):
#        self.workspace.delete("1.0", tk.END)
#        
#    def on_save(self):
#        messagebox.showinfo("Toolbar Action", "File Saved successfully!")
#        
#    def on_delete(self):
#        messagebox.showwarning("Toolbar Action", "Delete requested.")
#
#    # --- Quick Helper Function for Hover Tooltips ---
#    def add_tooltip(self, widget, text):
#        def enter(event):
#            self.tooltip = tk.Toplevel(widget)
#            self.tooltip.wm_overrideredirect(True) # Remove window borders
#            
#            # Position the tooltip directly beneath the hovered mouse cursor
#            x = widget.winfo_rootx() + 10
#            y = widget.winfo_rooty() + widget.winfo_height() + 5
#            self.tooltip.wm_geometry(f"+{x}+{y}")
#            
#            lbl = tk.Label(self.tooltip, text=text, bg="#ffffe0", relief=tk.SOLID, bd=1, font=("Arial", 9))
#            lbl.pack()
#            
#        def leave(event):
#            if hasattr(self, 'tooltip'):
#                self.tooltip.destroy()
#                
#        widget.bind("<Enter>", enter)
#        widget.bind("<Leave>", leave)
#
## Run the app
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = AppWithToolbar(root)
#    root.mainloop()