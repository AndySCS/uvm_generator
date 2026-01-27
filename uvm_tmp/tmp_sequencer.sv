class {tmp}_sequencer extends uvm_sequencer # ({tmp}_tr);

    function new (string name, uvm_component parent);
        super.new(name, parent);
    endfunction

    `uvm_component_utils({tmp}_sequencer)
    
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual task main_phase(uvm_phase phase);

endclass

function void {tmp}_sequencer::build_phase(uvm_phase phase);
    super.build_phase(phase);
endfunction

task {tmp}_sequencer::main_phase(uvm_phase phase);
    super.main_phase(phase); 
endtask
