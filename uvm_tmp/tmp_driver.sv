class {tmp}_driver extends uvm_driver #({tmp}_tr); 

    virtual {tmp}_intf {tmp}_if;

    `uvm_component_utils({tmp}_driver)
    
    function new(string name = "{tmp}_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction //new()
    
    extern function void build_phase(uvm_phase phase);
    extern virtual task main_phase(uvm_phase phase);

endclass //className extends superClass

function void {tmp}_driver::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!uvm_config_db#(virtual {tmp}_intf)::get(this, "", "{tmp}_if", {tmp}_if))begin
        `uvm_fatal("{tmp}_driver", "{tmp} driver fail to get {tmp} if")
    end
endfunction

task {tmp}_driver::main_phase(uvm_phase phase); 
    super.main_phase(phase);
endtask