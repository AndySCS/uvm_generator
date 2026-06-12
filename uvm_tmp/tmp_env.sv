class env extends uvm_env;

    {tmp}_agent {tmp}_agt;
    reference_model rm;
    scoreboard sc;

    function new(string name = "env", uvm_component parent);
        super.new(name, parent);
    endfunction

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task main_phase(uvm_phase phase);

    `uvm_component_utils(env)

endclass //env extends superClass

function void env::build_phase(uvm_phase phase);
    super.build_phase(phase);
    {f"{tmp}_agt = {tmp}_agent::type_id::create(\"{tmp}_agt\", this);n" if agent_define else "pass"} 
    {f"rm        = reference_model::type_id::create(\"rm\", this);n" if reference_model_define else "pass"} 
    {f"sc        = scoreboard::type_id::create(\"sc\", this);n" if scoreboard_define else "pass"} 
endfunction

function void env::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
endfunction

task env::main_phase(uvm_phase phase);
    super.main_phase(phase);
endtask
