#start page of the uvm generator
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from blocks import blocks
from InputPopup import InputPopup
from uvm_tree_node import uvm_tree_node
from xml_parser.xml_parser import xml_parser

class tree_node_editor(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.xml_tree = self.controller.xml_tree

    def setup_menu(self, uvm_tree_node):
        self.uvm_tree_node = uvm_tree_node
        self.variables = {}
        if self.uvm_tree_node:
            tree_node_path = self.uvm_tree_node.get_node_xml_path()
            configs = self.xml_tree.get_node_config(tree_node_path)
            for idx, config in enumerate(configs):
                # 1. Create a tracking variable for this specific checkbox
                var = tk.BooleanVar(value=False)
                self.variables[config] = var

                # 2. Create the Checkbutton widget
                # We use grid layout to stack them neatly on top of each other
                cb = ttk.Checkbutton(self, text=f"{config.tag}", variable=var)
                cb.grid(row=idx, column=0, sticky="w", pady=2)
    
    
