from logging import root
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from start_page import start_page
from uvm_tree import uvm_tree
from toolbar import toolbar


class XMLGuiApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("XML Creator & Reader")
        self.geometry("600x500")
        #self.root.minsize(500, 400)
        
        # Instantiate the separated Menu class and pass 'self' (this app) into it
        self.main_menu = toolbar(self)
        
        # Configure the app window to use this menu object
        self.config(menu=self.main_menu)

        # Create a central container to hold all page frames
        tree_container = tk.Frame(self)
        tree_container.pack(side="left", fill="both", expand=True)
        
        # Configure the grid to expand equally
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Create a central container to hold all page frames
        xml_container = tk.Frame(self)
        xml_container.pack(side="left", fill="both", expand=True)
        
        # Configure the grid to expand equally
        xml_container.grid_rowconfigure(0, weight=1)
        xml_container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store and reference the initialized frames
        self.frames = {}
        
        # Initialize and stack all pages in the exact same grid slot
        for PageClass in (start_page, uvm_tree, ):
            frame = PageClass(parent=tree_container, controller=self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Display the initial page
        self.show_frame(uvm_tree)
        
    def show_frame(self, page_class):
        """Brings the requested frame class to the top view."""
        frame = self.frames[page_class]
        frame.tkraise()

if __name__ == "__main__":
    app = XMLGuiApp()
    app.mainloop()