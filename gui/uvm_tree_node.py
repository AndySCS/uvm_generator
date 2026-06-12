#start page of the uvm generator
from dataclasses import dataclass
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom

@dataclass
class uvm_tree_node():

    name: str
    type: str
    xml_path: str
    
    def __init__(self, name, type, parent_xml_path):
        self.name = name
        self.type = type
        self.parent_xml_path = parent_xml_path

    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_parent_xml_path(self):
        return self.parent_xml_path
    
    def get_node_xml_path(self):
        node_xml_path = f"{self.type}@name={self.name}"
        if self.parent_xml_path:
            node_xml_path = f"{self.parent_xml_path}/{node_xml_path}"
        return node_xml_path