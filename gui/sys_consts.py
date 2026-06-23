from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
XML_DIR = SCRIPT_DIR / ".." / "uvm_xml_tmp"
XML_TMP_DIR = SCRIPT_DIR / "xml_tmp.xml"

@dataclass
class uvm_gen_config():
    UVM_XML_FILE: str | None
    UVM_TREE_NODES_NXT: list[str | None]
    TYPE_LIST: str | None
    NAME_SUFFIX: str | None

uvm_gen_config_table = {
    "": uvm_gen_config(UVM_XML_FILE=None, 
                       UVM_TREE_NODES_NXT=["UVM_ENV"], 
                       TYPE_LIST=None,
                       NAME_SUFFIX=None),
    "UVM_ENV": uvm_gen_config(UVM_XML_FILE=XML_DIR / "tmp_env.xml",
                              UVM_TREE_NODES_NXT=["UVM_AGENT", "UVM_DRIVER", "UVM_MONITOR"],
                              TYPE_LIST="",
                              NAME_SUFFIX="_env"),
    "UVM_AGENT": uvm_gen_config(UVM_XML_FILE=XML_DIR / "tmp_agent.xml",
                              UVM_TREE_NODES_NXT=["UVM_DRIVER", "UVM_MONITOR", "UVM_SEQUENCER"],
                              TYPE_LIST="Agent_list",
                              NAME_SUFFIX="_agt"),
    "UVM_DRIVER": uvm_gen_config(UVM_XML_FILE=XML_DIR / "tmp_driver.xml",
                              UVM_TREE_NODES_NXT=[],
                              TYPE_LIST="Driver_list",
                              NAME_SUFFIX="_drv"),
    "UVM_MONITOR": uvm_gen_config(UVM_XML_FILE=XML_DIR / "tmp_monitor.xml",
                              UVM_TREE_NODES_NXT=[],
                              TYPE_LIST="Monitor_list",
                              NAME_SUFFIX="_mon"),
}