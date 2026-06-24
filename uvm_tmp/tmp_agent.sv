class {tmp_root}_agent extends uvm_agent;
    
    {f"{tmp_root}_driver    {tmp};" if driver_define else "pass"}
    {f"{tmp_root}_sequencer {tmp};" if sequencer_define else "pass"}
    {f"{tmp_root}_monitor   {tmp};" if monitor_define else "pass"}
    {f"uvm_analysis_port #({tmp}) ap;" if uvm_analysis_port_define else "pass"} 

    function new(string name = "{tmp_root}_agent", uvm_component parent);
        super.new(name, parent);
    endfunction

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);

    `uvm_component_utils({tmp}_agent)

endclass //className extends superClass

function void {tmp_root}_agent::build_phase(uvm_phase phase);

    super.build_phase(phase);
    {f"{tmp} = {tmp}_driver::type_id::create(\"{tmp}\", this);" if driver_define else "pass"}
    {f"{tmp} = {tmp}_monitor::type_id::create(\"{tmp}\", this);" if monitor_define else "pass"}
    {f"{tmp} = {tmp}_sequencer::type_id::create(\"{tmp}\", this);" if sequencer_define else "pass"} 
    
endfunction

function void {tmp}_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase); 
    {f"ap = {tmp}.ap;" if uvm_analysis_port_define else "pass"} 
    {f"ap = {tmp}.seq_item_port.connect({tmp}_sqr.seq_item_export);" if driver_define and sequencer_define else "pass"}  
endfunction
