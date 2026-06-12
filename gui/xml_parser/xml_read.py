from logging import root
import xml.etree.ElementTree as ET

class xml_reader:
    def __init__(self, file_path):
        self.file_path = file_path
        # 1. Load and parse the XML file
        self.tree = None
        self.root = None
        self.load_xml()
        # 2. Access elements and attributes
        print(f"Root tag: {self.root.tag}\n")

    def load_xml(self):
        """Loads and parses the XML file."""
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            print(f"XML file '{self.file_path}' loaded successfully!")
        except Exception as e:
            print(f"Error loading XML file: {e}")
