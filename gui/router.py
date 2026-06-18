from logging import root
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from start_page import start_page
from uvm_tree import uvm_tree
from toolbar import toolbar
from tree_node_editor import tree_node_editor
from xml_parser.xml_parser import xml_parser
from pathlib import Path


class XMLGuiApp(tk.Tk):
    SCRIPT_DIR = Path(__file__).resolve().parent
    XML_DIR = SCRIPT_DIR / ".." / "uvm_xml_tmp"
    XML_TMP_DIR = SCRIPT_DIR / "xml_tmp.xml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("XML Creator & Reader")
        self.geometry("600x500")
        #self.root.minsize(500, 400)
        
        # Instantiate the separated Menu class and pass 'self' (this app) into it
        self.main_menu = toolbar(self)
        
        # Configure the app window to use this menu object
        self.config(menu=self.main_menu)
        self.xml_tree = xml_parser(self.XML_TMP_DIR, create_if_not_exists=True)  # Load or create the XML file for the root node

        # Create a central container to hold all page frames
        tree_container = tk.Frame(self)
        tree_container.pack(side="left", fill="both", expand=True)
        
        # Configure the grid to expand equally
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Create a central container to hold all page frames
        config_container = tk.Frame(self)
        config_container.pack(side="left", fill="both", expand=True)
        
        # Configure the grid to expand equally
        config_container.grid_rowconfigure(0, weight=1)
        config_container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store and reference the initialized frames
        self.frames = {}
        
        # Initialize and stack all pages in the exact same grid slot
        frame_classes = [uvm_tree, tree_node_editor]
        frame_containers = [tree_container, config_container]
        for PageClass, frame_container in zip(frame_classes, frame_containers):
            frame = PageClass(parent=frame_container, controller=self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Display the initial page
        self.show_frame(uvm_tree)
        self.show_frame(tree_node_editor)
        
    def show_frame(self, page_class):
        """Brings the requested frame class to the top view."""
        frame = self.frames[page_class]
        frame.tkraise()

    def on_closing(self):
        os.remove(uvm_tree.XML_TMP_DIR)  # Clean up the temporary XML file when closing the app
        self.destroy()

if __name__ == "__main__":
    app = XMLGuiApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()