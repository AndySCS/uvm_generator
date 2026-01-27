import configparser
import os

class uvm_comp_setting:

    uvm_file_hash = {
        "uvm_agent"     : "tmp_agent.sv", 
        "uvm_driver"    : "tmp_driver.sv", 
        "uvm_monitor"   : "tmp_monitor.sv", 
        "uvm_sequencer" : "tmp_sequencer.sv", 
        "uvm_interface" : "tmp_interface.sv"
    }
    
    def __init__(self):
        self.name                     = '' 
        self.path                     = './'
        self.type                     = ''
        self.driver_define            = False
        self.interface_define         = False
        self.sequencer_define         = False
        self.monitor_define           = False
        self.uvm_analysis_port_define = False

    def get_setting(self, setting: configparser.SectionProxy, type: str, proj_path: str) -> None:
        self.name                     = setting.get('NAME', fallback=False)
        self.path                     = os.path.join(proj_path, setting.get('PATH', fallback=False))
        self.type                     = type
        self.driver_define            = setting.getboolean('DRIVER', fallback=False)
        self.interface_define         = setting.getboolean('INTERFACE', fallback=False)
        self.sequencer_define         = setting.getboolean('SEQUENCER', fallback=False)
        self.monitor_define           = setting.getboolean('MONITOR', fallback=False)
        self.uvm_analysis_port_define = setting.getboolean('UVM_ANALYSIS_PORT', fallback=False)

    def write_uvm_files(self, uvm_comp: str, script_path: str) -> None:
        tmp                      = self.name
        driver_define            = self.driver_define            
        interface_define         = self.interface_define         
        sequencer_define         = self.sequencer_define         
        monitor_define           = self.monitor_define           
        uvm_analysis_port_define = self.uvm_analysis_port_define

        uvm_template_folder_path = os.path.join(script_path, 'uvm_tmp') 
        uvm_template = open(f"{os.path.join(uvm_template_folder_path, uvm_comp_setting.uvm_file_hash[uvm_comp])}", "r")
        output_uvm = open(f"{os.path.join(self.path, uvm_comp_setting.uvm_file_hash[uvm_comp].replace('tmp', self.name))}", "w")

        for line in uvm_template:
            line = line.rstrip('\n')
            format_str = eval(f"f'{line}'")
            if format_str == 'pass':
                continue
            else:
                output_uvm.write(f"{format_str}\n")
        
        uvm_template.close()
        output_uvm.close()

    def create_agent(self, script_path: str) -> None:
        self.write_uvm_files(uvm_comp='uvm_agent', script_path=script_path)
        if self.driver_define:
            self.write_uvm_files(uvm_comp='uvm_driver', script_path=script_path)
        if self.interface_define:
            self.write_uvm_files(uvm_comp='uvm_interface', script_path=script_path)
        if self.sequencer_define:
            self.write_uvm_files(uvm_comp='uvm_sequencer', script_path=script_path)
        if self.monitor_define:
            self.write_uvm_files(uvm_comp='uvm_monitor', script_path=script_path)
    
    def create_driver(self, script_path: str) -> None:
        self.write_uvm_files(uvm_comp='uvm_driver', script_path=script_path)

    def create_sequencer(self, script_path: str) -> None:
        self.write_uvm_files(uvm_comp='uvm_sequencer', script_path=script_path)
    
    def create_monitor(self, script_path: str) -> None:
        self.write_uvm_files(uvm_comp='uvm_monitor', script_path=script_path)
    
    def create_inteface(self, script_path: str) -> None:
        self.write_uvm_files(uvm_comp='uvm_interface', script_path=script_path)

    def create_uvm_component(self, script_path: str) -> None:
        create_uvm_component_hash = {
            'AGENT'         : self.create_agent,
            'DRIVER'        : self.create_driver,
            'MONITOR'       : self.create_monitor,
            'INTERFACE'     : self.create_inteface,
            'SEQUENCER'     : self.create_sequencer,
        }

        return create_uvm_component_hash[self.type](script_path=script_path)