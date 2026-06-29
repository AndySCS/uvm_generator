#start page of the uvm generator
from dataclasses import dataclass
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom
from sys_consts import uvm_gen_config_table

@dataclass
class uvm_tree_node():

    name: str
    type: str
    xml_path: str
    gen_path: str
    
    def __init__(self, name = "", type = "", parent_xml_path = ""):
        self.name = name
        self.type = type
        self.parent_xml_path = parent_xml_path

    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type

    def get_parent_xml_path(self):
        return self.parent_xml_path 
    
    def get_type_list(self):
        return uvm_gen_config_table.get(self.type).TYPE_LIST
    
    def get_merge_xml_path(self):
        merge_xml_path = f"{self.parent_xml_path}"
        if merge_xml_path != '.':
            merge_list = uvm_gen_config_table.get(self.type).TYPE_LIST
            merge_xml_path = f"{merge_xml_path}/{merge_list}"
        return merge_xml_path
    
    def get_xml_name(self):
        return f"{self.type}[@name='{self.name}']"
    
    def get_node_xml_path(self):
        node_xml_path = self.get_xml_name() 
        merge_path = self.get_merge_xml_path()
        if merge_path:
            node_xml_path = f"{merge_path}/{node_xml_path}"
        return node_xml_path