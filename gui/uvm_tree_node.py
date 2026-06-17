#start page of the uvm generator
from dataclasses import dataclass
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from xml.dom import minidom

@dataclass
class uvm_tree_node():

    TYPE_LIST = { 
        "UVM_ENV": "",
        "UVM_AGENT": "Agent_list",
        "UVM_DRIVER": "Driver_list",
        "UVM_MONITOR": "Monitor_list",
        #"UVM_SCOREBOARD": XML_DIR / "tmp_scoreboard.xml",
        "UVM_SEQUENCER": "Sequencer_list"
    }

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
    
    def get_merge_xml_path(self):
        merge_xml_path = f"{self.parent_xml_path}"
        if merge_xml_path:
            merge_list = self.TYPE_LIST.get(self.type)
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