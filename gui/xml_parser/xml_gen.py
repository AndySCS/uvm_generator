import xml.etree.ElementTree as ET
import xml.dom.minidom

class XMLGenerator:
    def __init__(self):
        self.root = ET.Element("data")

# 1. Create the root element
root = ET.Element("data")

# 2. Create sub-elements
item1 = ET.SubElement(root, "item", id="1")
name1 = ET.SubElement(item1, "name")
name1.text = "Laptop"
price1 = ET.SubElement(item1, "price")
price1.text = "1200"

item2 = ET.SubElement(root, "item", id="2")
name2 = ET.SubElement(item2, "name")
name2.text = "Mouse"
price2 = ET.SubElement(item2, "price")
price2.text = "25"

# 3. Wrap it in an ElementTree object
tree = ET.ElementTree(root)

# 4. Write to a file
# Use encoding='utf-8' and xml_declaration=True for a standard XML header
tree.write("output.xml", encoding="utf-8", xml_declaration=True)

print("XML file 'output.xml' created successfully!")

def pretty_save(element_tree, filename):
    rough_string = ET.tostring(element_tree.getroot(), encoding="utf-8")
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_string = reparsed.toprettyxml(indent="  ")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml_string)

# 1. Load and parse the XML file
tree = ET.parse("items.xml")
root = tree.getroot()

# 2. Access elements and attributes
print(f"Root tag: {root.tag}\n")

# 3. Iterate through elements
for item in root.findall("item"):
    # Get attribute
    item_id = item.get("id")

    # Get child element text (using .findtext() for convenience)
    name = item.findtext("name")
    price = item.findtext("price")

    print(f"Item ID: {item_id}")
    print(f"  Name:  {name}")
    print(f"  Price: ${price}")
    print("-" * 20)