from logging import root
import xml.etree.ElementTree as ET

class xml_parser:

    namespaces = {
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    # Construct the exact attribute key Python will see

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

    def merge_xml(self, new_root: ET.Element, parent_path=".", type_list=""):
        
        merge_path = "."

        if parent_path != ".":
            merge_path = f"{parent_path}/{type_list}"
        target_parent = self.root.find(merge_path)

        if target_parent is not None:
            
            parent_dir = self.get_gen_dir(parent_path)
            new_root_config = new_root.find('Configuration')

            if new_root_config:
                new_root_dir = new_root_config.find('dir')

                if new_root_dir is not None:
                    print(parent_dir)
                    new_root_dir.text = str(parent_dir)

            target_parent.append(new_root)
            print("XML merged successfully!")
            self.write_xml()
        else:
            print(f"Parent node not found, parent path is {merge_path}")

    def get_gen_dir(self, node_path: str = "."):
        config_path = f"{node_path}/Configuration"
        node_config_raw = self.root.find(config_path)
        if node_config_raw:
            gen_dir = node_config_raw.find('dir')
            print("gen dir")
            for child in node_config_raw:
                print(f"Tag: {child.tag} | Attributes: {child.attrib} | Text: {child.text}")
            print("gen dir ends")
            return gen_dir.text if gen_dir.text else ""
        else:
            return ""

    def write_xml(self):
        ET.indent(self.tree, space="    ", level=0)
        self.tree.write(self.file_path, xml_declaration=True, short_empty_elements=False)  # Save changes to the file

    def set_name(self, new_name):
        self.root.set("name", new_name)

    def get_node_config(self, node_path):
        config_path = f"{node_path}/Configuration"
        node_config_raw = self.root.find(config_path)
        if not node_config_raw:
            raise ValueError(f"Configuration path {config_path} does not exist")
        config_list = []
        for config in node_config_raw:
            config_list.append(self.get_node_config_value(config))
        return config_list
    
    def get_node_config_value(self, config):
        node_value = config.text.strip() if config.text else ""
        data_type = config.attrib['type']
        # Cast to Python boolean if the type is xsd:boolean

        if data_type == "boolean":
            # XML booleans are standard lowercase 'true' or 'false'
            actual_value = node_value.lower() == "true"
        else:
            # Fallback for other types or default strings
            actual_value = node_value

        config_dict = {
            'tag': config.tag,
            'type': data_type,
            'value': actual_value
        }

        return config_dict
         
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

    def update_node_config(self, node_path: str, new_config: dict)->None:
        config_path = f"{node_path}/Configuration"
        node_config = self.root.find(config_path)
        for new_config_tag, new_config_value in new_config.items():
            #print(config_tag)
            update_config = node_config.find(new_config_tag)

            if update_config is None:
                raise ValueError(f"config {new_config_tag} does not exits in path:\n{node_path}")
            
            update_config.text = str(new_config_value)

        self.write_xml()

