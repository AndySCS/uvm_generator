class {tmp}_agent extends uvm_agent;
    
    {f"{tmp}_driver    {tmp}_drv;" if driver_define else "pass"}
    {f"{tmp}_sequencer {tmp}_sqr;" if sequencer_define else "pass"}
    {f"{tmp}_monitor   {tmp}_mon;" if monitor_define else "pass"}
    {f"uvm_analysis_port #({tmp}_tr) ap;" if uvm_analysis_port_define else "pass"} 

    function new(string name = "{tmp}_agent", uvm_component parent);
        super.new(name, parent);
    endfunction

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);

    `uvm_component_utils({tmp}_agent)

endclass //className extends superClass

function void {tmp}_agent::build_phase(uvm_phase phase);

    super.build_phase(phase);
    {f"{tmp}_drv = {tmp}_driver::type_id::create(\"{tmp}_drv\", this);" if driver_define else "pass"}
    {f"{tmp}_mon = {tmp}_monitor::type_id::create(\"{tmp}_mon\", this);" if monitor_define else "pass"}
    {f"{tmp}_sqr = {tmp}_sequencer::type_id::create(\"{tmp}_sqr\", this);" if sequencer_define else "pass"} 
    
endfunction

function void {tmp}_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase); 
    {f"ap = {tmp}_mon.ap;" if uvm_analysis_port_define else "pass"} 
    {f"ap = {tmp}_drv.seq_item_port.connect({tmp}_sqr.seq_item_export);" if driver_define and sequencer_define else "pass"}  
endfunction
