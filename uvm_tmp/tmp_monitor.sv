class {tmp}_monitor extends uvm_monitor;

    virtual {tmp}_intf {tmp}_if;
    uvm_analysis_port #({tmp}_tr) ap;

    `uvm_component_utils({tmp}_input_monitor)
    function new(string name = "{tmp}_input_monitor", uvm_component parent = null);
       super.new(name, parent);
    endfunction //new()
    
    extern function void build_phase(uvm_phase phase);
    extern virtual task main_phase(uvm_phase phase);
    
endclass //{tmp}_input_monitor extends superClass

function void {tmp}_monitor::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!uvm_config_db#(virtual {tmp}_intf)::get(this, "", "{tmp}_if", {tmp}_if))begin
        `uvm_fatal("{tmp}_input_monitor", "{tmp} input_monitor fail to get {tmp} if")
    end
    ap = new("ap", this);
endfunction

task {tmp}_monitor::main_phase(uvm_phase phase);
    super.main_phase(phase);    
endtask
