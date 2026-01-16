class {tmp}_agent extends uvm_agent;
    
    {tmp}_driver {tmp}_drv;
    {tmp}_sequencer {tmp}_sqr;
    {tmp}_output_monitor {tmp}_mon; //output monitor
    uvm_analysis_port #({tmp}_tr) ap;

    function new(string name = "{tmp}_agent", uvm_component parent);
        super.new(name, parent);
    endfunction

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);

    `uvm_component_utils({tmp}_agent)

endclass //className extends superClass

function void {tmp}_agent::build_phase(uvm_phase phase);
    super.build_phase(phase);
    {tmp}_drv = {tmp}_driver::type_id::create("{tmp}_drv", this);
    {tmp}_mon = {tmp}_output_monitor::type_id::create("{tmp}_omon", this);
    {tmp}_sqr = {tmp}_sequencer::type_id::create("{tmp}_sqr", this);
endfunction

function void {tmp}_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    ap = {tmp}_mon.ap;
    {tmp}_drv.seq_item_port.connect({tmp}_sqr.seq_item_export);
endfunction
