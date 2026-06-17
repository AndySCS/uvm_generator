#start page of the uvm generator
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from blocks import blocks
from InputPopup import InputPopup
from uvm_tree_node import uvm_tree_node
from pathlib import Path
from xml_parser.xml_parser import xml_parser

class uvm_tree(tk.Frame):

    #constants for tree structure
    SCRIPT_DIR = Path(__file__).resolve().parent
    XML_DIR = SCRIPT_DIR / ".." / "uvm_xml_tmp"
    XML_TMP_DIR = SCRIPT_DIR / "xml_tmp.xml"
    UVM_XML_FILE = {
        "UVM_ENV": XML_DIR / "tmp_env.xml",
        "UVM_AGENT": XML_DIR / "tmp_agent.xml",
        "UVM_DRIVER": XML_DIR / "tmp_driver.xml",
        "UVM_MONITOR": XML_DIR / "tmp_monitor.xml",
        #"UVM_SCOREBOARD": XML_DIR / "tmp_scoreboard.xml",
        "UVM_SEQUENCER": XML_DIR / "tmp_sequencer.xml"
    }
    UVM_TREE_NODES_NXT = {
        "":["UVM_ENV"],
        "UVM_ENV":["UVM_AGENT", "UVM_DRIVER", "UVM_MONITOR"],
        "UVM_AGENT":["UVM_DRIVER", "UVM_MONITOR", "UVM_SEQUENCER"],
        "UVM_DRIVER":[],
        "UVM_MONITOR":[],
        "UVM_SCOREBOARD":[]
    }

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.context_menu = tk.Menu(self, tearoff=False)
        self.block_menu = tk.Menu(self, tearoff=0)
        self.tree_nodes = {}  # Dictionary to keep track of nodes by their unique IDs
        self.setup_ui()
        self.xml_tree = xml_parser(self.XML_TMP_DIR, create_if_not_exists=True)  # Load or create the XML file for the root node

    def setup_empty_menu(self):
            self.context_menu.add_command(label="Create Node", command= lambda: self.create_node())  # Placeholder for clear canvas functionality

    def get_clicked_node_id(self, clicked_item):
        clicked_item_id = self.tree.selection()[0]  # Get the node instance from the value
        return clicked_item_id
    
    def get_clicked_node_type(self, clicked_item):
        clicked_item_id = self.get_clicked_node_id(clicked_item)
        clicked_node = self.get_node_by_id(clicked_item_id)
        return clicked_node.get_type()  # Add a tag for styling if needed

    def setup_node_menu(self, clicked_item):
        # User clicked on an actual node
        item_type = self.get_clicked_node_type(clicked_item)
        if self.UVM_TREE_NODES_NXT.get(item_type, []):  # Check if there are allowed child types
            self.context_menu.add_command(label="Create Block", command= lambda: self.create_node(clicked_item=clicked_item))  # Placeholder for clear canvas functionality
        self.context_menu.add_command(label="Delete Node", command= lambda: self.delete_node(item=clicked_item))  # Placeholder for clear canvas functionality
        # Show your "Edit / Delete" context menu here

    def setup_menu(self, event):
        # 1. Clear any old commands so they don't pile up
        self.context_menu.delete(0, "end")
        """Sets up the context menu with options for the canvas."""
        #self.context_menu.add_separator()
        clicked_item = self.tree.identify_row(event.y) 
        if not clicked_item: # clicked on empty space, not a node
            self.setup_empty_menu()  # Show the "Create Node" option for empty space
        else:
            self.tree.selection_set(clicked_item)
            self.setup_node_menu(clicked_item)  # Show the "Edit / Delete" options for the clicked node

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
        self.tree.heading("#0", text="UVM Testbench Structure", anchor=tk.W)  # Set the heading for the tree
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar for when the list gets long
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 2. Bind Mouse Events to the Treeview
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind('<<TreeviewSelect>>', self.on_node_click)

    def insert_new_node(self, parent="", new_node=None):
        """Helper to insert a new node into the tree."""
        if new_node is not None:
            node_id = self.tree.insert(parent, 'end', 
                                       text=f"{new_node.get_name()}({new_node.get_type()})", 
                                       values=(new_node.get_name(), new_node.get_type()))
            self.tree_nodes[node_id] = new_node  # Store the node instance in the dictionary for later reference

    def insert_xml_node(self, parent="", new_node=None):
        tmp_xml_file_path = self.UVM_XML_FILE.get(new_node.get_type(), None)
        if tmp_xml_file_path:
            # Ensure the directory exists
            tmp_xml_file_path.parent.mkdir(parents=True, exist_ok=True)
            # Create an empty XML file for this node type
            xml_read = xml_parser(tmp_xml_file_path)  # This will create the file if it doesn't exist and load it
            xml_read.set_name(new_node.get_name())
            parent_xml_path = new_node.get_merge_xml_path() if new_node.get_parent_xml_path() else "."
            self.xml_tree.merge_xml(xml_read.root, parent_path=parent_xml_path)  # Merge the new node's XML into the main XML tree
        else:
            print(f"Warning: No XML file path defined for type '{new_node.get_type()}'")

    def create_node(self, clicked_item=""):
        """Helper to create a tree node."""
        # Create a tag so we can move both the rectangle and text together
        parent_type = self.get_clicked_node_type(clicked_item) if clicked_item else ""
        create_result = self.open_popup(parent_type=parent_type)
        if create_result is not None:
            parent_xml_path = self.get_node_by_id(clicked_item).get_node_xml_path() if clicked_item else ""
            new_node = uvm_tree_node(
                name=create_result['name'], 
                type=create_result['type'], 
                parent_xml_path=parent_xml_path
            )
            self.insert_new_node(parent=clicked_item, new_node=new_node)
            self.insert_xml_node(parent=clicked_item, new_node=new_node)

    def on_node_click(self, event):
        # 1. Get the ID of the selected item
        selected_item = self.tree.selection()

        if selected_item:
            node_id = self.get_clicked_node_id(selected_item)
            clicked_node = self.get_node_by_id(node_id)
            xml_path = clicked_node.get_node_xml_path()
            self.xml_tree.get_node_config(xml_path)
            ## 2. Get the unique ID (Tkinter uses strings like 'I001')
            #node_id = selected_item[0]
            ## 3. Retrieve the item's details (like its text)
            #node_text = self.tree.item(node_id, "text")
        
            ## Print or use the data
            #print(f"Clicked Node ID: {node_id} | Text: {node_text}")

    def delete_node(self, item):
        node_id = self.get_clicked_node_id(item)
        clicked_node = self.get_node_by_id(node_id)

        merge_path = clicked_node.get_merge_xml_path()
        xml_name = clicked_node.get_xml_name()
        self.xml_tree.del_node_by_path(merge_path = merge_path, node_name = xml_name)

        self.tree_nodes.pop(node_id)

        self.tree.selection_clear()  # Clear selection to avoid issues with deleted item
        self.tree.delete(item) 


    def open_popup(self, parent_type=""):
        """Opens a popup window to collect user input for creating a new block."""
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
    
    def get_node_by_id(self, node_id):
        """Helper to retrieve a node instance by its tree ID."""
        return self.tree_nodes.get(node_id, None)
    
