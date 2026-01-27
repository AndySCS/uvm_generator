class {tmp}_monitor extends uvm_monitor;

    {f"virtual {tmp}_interface {tmp}_intf;" if interface_define else "pass"}
    {f"uvm_analysis_port #({tmp}_tr) ap;" if uvm_analysis_port_define else "pass"} 

    `uvm_component_utils({tmp}_t_monitor)
    function new(string name = "{tmp}_monitor", uvm_component parent = null);
       super.new(name, parent);
    endfunction
    
    extern function void build_phase(uvm_phase phase);
    extern virtual task main_phase(uvm_phase phase);
    
endclass

function void {tmp}_monitor::build_phase(uvm_phase phase);
    super.build_phase(phase);
    {f"if(!uvm_config_db#(virtual {tmp}_interface)::get(this, \"\", \"{tmp}_inft\", {tmp}_inft))begin" if interface_define else "pass"}
    {f"    `uvm_fatal(get_name(), $sformatf(\"{tmp}_monitor fail to get {tmp}_intf\"))               " if interface_define else "pass"}
    {f"end                                                                                           " if interface_define else "pass"} 
    {f"ap = new(\"ap\", this);" if uvm_analysis_port_define else "pass"} 
endfunction

task {tmp}_monitor::main_phase(uvm_phase phase);
    super.main_phase(phase);    
endtask
