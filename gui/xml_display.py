#start page of the uvm generator
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from blocks import blocks
from InputPopup import InputPopup
from uvm_tree_node import uvm_tree_node

class xml_display(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.context_menu = tk.Menu(self, tearoff=False)
        self.block_menu = tk.Menu(self, tearoff=0)
        self.tree_nodes = {}  # Dictionary to keep track of nodes by their unique IDs
        self.setup_ui()

    def setup_menu(self, event):
        # 1. Clear any old commands so they don't pile up
        self.context_menu.delete(0, "end")
        """Sets up the context menu with options for the canvas."""
        #self.context_menu.add_separator()
        clicked_item = self.tree.identify_row(event.y) 
        if not clicked_item: # clicked on empty space, not a node
            self.context_menu.add_command(label="Create Node", command= lambda: self.create_node())  # Placeholder for clear canvas functionality
        else:
            # User clicked on an actual node
            self.tree.selection_set(clicked_item)  # Select it
            item_type = self.tree.item(clicked_item, "values")  # Add a tag for styling if needed
            print(f"Right-clicked node: {self.tree.item(clicked_item, 'text')}")
            if self.UVM_TREE_NODES_NXT.get(item_type[0], []):  # Check if there are allowed child types
                self.context_menu.add_command(label="Create Block", command= lambda: self.create_node(parent=clicked_item))  # Placeholder for clear canvas functionality
            self.context_menu.add_command(label="Delete Node", command= lambda: self.delete_node(item=clicked_item))  # Placeholder for clear canvas functionality
            # Show your "Edit / Delete" context menu here

    def show_context_menu(self, event):
        """Displays the context menu at the mouse cursor location."""
        self.setup_menu(event)  # Ensure the menu is updated with the latest event coordinates
        try:
            # Dynamically display the menu at screen coordinates
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            # Releases the event grab on systems that require it
            self.context_menu.grab_release()

    def setup_ui(self):
        # 1. Create the treeview
        self.tree = ttk.Treeview(self)
        self.tree.heading('#0', text='Project Hierarchy', anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar for when the list gets long
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. Bind Mouse Events to the Treeview
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind('<<TreeviewSelect>>', self.on_node_click)

    def create_node(self, parent=""):
        """Helper to create a tree node."""
        # Create a tag so we can move both the rectangle and text together
        create_result = self.open_popup(parent=parent)
        if create_result is not None:
            self.tree.insert(parent, 'end', 
                             text=f"{create_result['name']}({create_result['type']})", 
                             values=(create_result['type'],)
                            )
            #self.tree_nodes[new_node.get_id()] = new_node  # Store the node instance in the dictionary for later reference

    def on_node_click(self, event):
        # 1. Get the ID of the selected item
        selected_item = self.tree.selection()

        if selected_item:
            # 2. Get the unique ID (Tkinter uses strings like 'I001')
            node_id = selected_item[0]
            # 3. Retrieve the item's details (like its text)
            node_text = self.tree.item(node_id, "text")
        
            # Print or use the data
            print(f"Clicked Node ID: {node_id} | Text: {node_text}")

    def delete_node(self, item):
        self.tree.selection_clear()  # Clear selection to avoid issues with deleted item
        self.tree.delete(item)

    def open_popup(self, parent=""):
        """Opens a popup window to collect user input for creating a new block."""
        parent_type = self.tree.item(parent, "values")[0] if parent else ""
        popup = InputPopup(self, types=list(self.UVM_TREE_NODES_NXT.get(parent_type, [])))  # Pass the allowed types based on parent
        self.wait_window(popup)  # Wait until the popup is closed
        
        # Check if the user filled it out or just closed it
        if popup.result:
            data = popup.result
            # Display the collected data in our main window label
            print(
                f"Data Received:\nName: {data['name']}\nType: {data['type']}"
            )
        return popup.result
    
    

