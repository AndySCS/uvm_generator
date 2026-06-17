from logging import root
import xml.etree.ElementTree as ET

class xml_parser:
    def __init__(self, file_path, create_if_not_exists=False):
        self.file_path = file_path
        # 1. Load and parse the XML file
        self.tree = None
        self.root = None
        self.init_parser(create_if_not_exists)  # Initialize the parser and load or create the XML file
        # 2. Access elements and attributes
        #print(f"Root tag: {self.root.tag}\n")

    def init_parser(self, create_if_not_exists):  
        if create_if_not_exists and not self.file_path.exists():
            # Create an empty XML file with a root element
            self.root = ET.Element("root")
            self.tree = ET.ElementTree(self.root)
            self.tree.write(self.file_path)
            print(f"Created new XML file at: {self.file_path}")
        else:
            self.load_xml()  # Load the existing XML file

    def load_xml(self):
        """Loads and parses the XML file."""
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            print(f"XML file '{self.file_path}' loaded successfully!")
        except Exception as e:
            print(f"Error loading XML file: {e}")

    def merge_xml(self, new_root: ET.Element, parent_path="."):
        target_parent = self.root.find(parent_path)
        if target_parent is not None:
            target_parent.append(new_root)
            print("XML merged successfully!")
            self.write_xml()
        else:
            print(f"Parent node not found, parent path is {parent_path}")

    def write_xml(self):
        ET.indent(self.tree, space="    ", level=0)
        self.tree.write(self.file_path, xml_declaration=True, short_empty_elements=False)  # Save changes to the file

    def set_name(self, new_name):
        self.root.set("name", new_name)

    def get_node_config(self, node_path):
        config_path = f"{node_path}/Configuration"
        node_config = self.root.find(config_path)
        for config in node_config:
            print(f"{config.tag}: {config.attrib}")
        return node_config
    
    def del_node_by_path(self, merge_path, node_name):
        if merge_path:
            del_dir = self.root.find(merge_path)
        else:
            del_dir = self.root
            
        del_node = del_dir.find(node_name)
        if del_node:
            del_dir.remove(del_node)
        else:
            print(f"path not found\npath: {merge_path}\nnode name: {node_name}")
        self.write_xml()