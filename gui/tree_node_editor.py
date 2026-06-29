#start page of the uvm generator
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from InputPopup import InputPopup
from uvm_tree_node import uvm_tree_node
from xml_parser.xml_parser import xml_parser
from tkinter import filedialog
from pathlib import Path

class tree_node_editor(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.xml_tree = self.controller.xml_tree
        self.setup_ui()
        self.setup_config_by_type = {
            'string': self.setup_textbox,
            'boolean': self.setup_checkbox,
            'dir': self.setup_path
        }

    def setup_ui(self):
        pass

    def check_config_vld(self, config):
        config_value = config.get('value', None)
        config_tag = config.get('tag', None)
        config_type = config.get('type', None)

        if config_value is None or config_tag is None or config_type is None:
            raise ValueError("value or tag is not found in config")
        
        return config_tag, config_type, config_value

    def setup_checkbox(self, idx, config_value, config_tag):
        # 1. Create a tracking variable for this specific checkbox
        var = tk.BooleanVar(value=config_value)
        self.variables[config_tag] = var

        # 2. Create the Checkbutton widget
        # We use grid layout to stack them neatly on top of each other
        cb = ttk.Checkbutton(self, text=f"{config_tag}", variable=var)
        cb.grid(row=idx, column=0, sticky="w", pady=2)

    def setup_textbox(self, idx, config_value, config_tag):
        entry_var = tk.StringVar(value = config_value)
        self.variables[config_tag] = entry_var

        entry_frame = tk.Frame(self)
        entry_frame.grid(row=idx, column=0, columnspan=2, sticky="w", pady=2)

        config_label = tk.Label(entry_frame, text=config_tag)
        config_label.pack(side="left")

        answer_entry = tk.Entry(entry_frame, textvariable=entry_var)
        answer_entry.pack(side="left", padx=(5, 0))
        #self.answer_entry.insert(0, config_value)

    def setup_path(self, idx, config_value, config_tag):
        
        def get_path(entry_var):
            if entry_var.get():
                initialdir = entry_var.get()
            else:
                initialdir=Path.cwd() 
            selected_dir = filedialog.askdirectory(
                initialdir=initialdir, 
                title="Select a Directory"
            )
            if selected_dir:
                # StringVar CAN update even if the Entry widget is disabled!
                entry_var.set(selected_dir)

        entry_var = tk.StringVar(value = config_value)
        self.variables[config_tag] = entry_var

        entry_frame = tk.Frame(self)
        entry_frame.grid(row=idx, column=0, columnspan=2, sticky="w", pady=2)

        config_label = tk.Label(entry_frame, text=config_tag)
        config_label.pack(side="left")

        answer_entry = tk.Entry(entry_frame, textvariable=entry_var)
        answer_entry.pack(side="left", padx=(5, 0))
        answer_entry.config(state="disabled")

        btn_open = tk.Button(entry_frame, text="Browse Folder", command=lambda: get_path(entry_var=entry_var))
        btn_open.pack(side="left", padx=(5, 0))
        #self.answer_entry.insert(0, config_value)

    def setup_menu(self, uvm_tree_node):
        self.uvm_tree_node = uvm_tree_node
        self.variables = {}
        self.reset_menu()

        if self.uvm_tree_node:
            tree_node_path = self.uvm_tree_node.get_node_xml_path()
            configs = self.xml_tree.get_node_config(tree_node_path)
            idx = 0
    
            for config in configs:
                config_tag, confgi_type, config_value = self.check_config_vld(config=config)
                self.setup_config_by_type[confgi_type](idx=idx, config_value=config_value, config_tag=config_tag)
                idx += 1

            # 3. Configure the row/column weights so sticky="se" actually moves it to the corner
            self.grid_rowconfigure(idx + 1, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            # 4. Place the button at the very next row below the checkboxes
            btn = tk.Button(self, text='Update node', command= self.update_node)  
            btn.grid(row=idx + 1, column=1, sticky="se", padx=10, pady=10)

    def update_node(self):
        node_xml_path = self.uvm_tree_node.get_node_xml_path()
        deocde_variables = {key: value.get() for key, value in self.variables.items()} #extract data from tk variables
        self.controller.xml_tree.update_node_config(node_path = node_xml_path, new_config =deocde_variables)

    def reset_menu(self):
        for widget in self.winfo_children():
            widget.destroy() 
    
