import argparse
import os
import inquirer
from inquirer.themes import GreenPassion
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

# Path to the current script
script_dir = Path(__file__).parent
uvm_tmp_dir = os.path.join(script_dir, 'uvm_tmp')

uvm_types = ["uvm_agent", "uvm_driver", "uvm_monitor", "uvm_sequencer", "uvm_interface"]#, "uvm_env", "uvm_sequence", "uvm_test"]
uvm_agent_comp = ["uvm_driver", "uvm_monitor", "uvm_sequencer", "uvm_interface"]

uvm_parent_hash = {
    "uvm_agent" : uvm_agent_comp
}

uvm_file_hash = {
    "uvm_agent"     : "tmp_agent.sv", 
    "uvm_driver"    : "tmp_driver.sv", 
    "uvm_monitor"   : "tmp_monitor.sv", 
    "uvm_sequencer" : "tmp_sequencer.sv", 
    "uvm_interface" : "tmp_intf.sv"
}

inquirer_choice_type = {
    'list'      : inquirer.List,
    'checkbox'  : inquirer.Checkbox
}

def get_path(msg: str) -> str:
    session = PromptSession()
    completer = PathCompleter(expanduser=True, only_directories=True)
    path = session.prompt(f"{msg}: ", completer=completer)
    return path

def get_choice(opts: list[str], msg: str, question_type: str) -> str | list[str]:
    question = [inquirer_choice_type[question_type]("choice", message=msg, choices=opts)]
    answer = inquirer.prompt(question)
    return answer['choice']

def get_txt(msg: str) -> str:
    question = [inquirer.Text("ans", message=msg)]
    answer = inquirer.prompt(question)
    return answer['ans']

def get_confrim(msg: str) -> bool:
    question = [inquirer.Confirm("ans", message=msg, default = False)]
    answer = inquirer.prompt(question)
    return answer['ans']

def get_files(uvm_type: str) -> list[str]:
    uvm_type_list = [uvm_type]
    if uvm_type in uvm_parent_hash:
        msg = f'select uvm component under {uvm_type}'
        uvm_type_list += get_choice(uvm_parent_hash[uvm_type], msg, 'checkbox')
    uvm_file_list = [uvm_file_hash[uvm_key] for uvm_key in uvm_type_list]
    return uvm_file_list

def read_uvm_tmp(uvm_file_type: str) -> list[str]:
    tmp_file = []
    with open(uvm_file_type) as f:
        for line in f:
            tmp_file.append(line)
    return tmp_file

def write_uvm_tmp(tmp_file: list[str], gen_name: str, write_file_path: str) -> None:
    with open(write_file_path, 'w') as f:
        for line in tmp_file:
            f.write(line.format(tmp = gen_name))

def write_files(uvm_file_list: list[str], gen_name: str, write_file_dir: str) -> None:
    for uvm_file in uvm_file_list:
        tmp_file = read_uvm_tmp(os.path.join(uvm_tmp_dir, uvm_file))
        write_file_path = os.path.join(write_file_dir, uvm_file.replace('tmp', gen_name))
        write_uvm_tmp(tmp_file, gen_name, write_file_path)

if __name__ == '__main__':
    dest_dir = get_path('gen file dir')
    gen_name = get_txt('gen file name')
    uvm_type = get_choice(uvm_types, 'select uvm component', 'list')
    uvm_file_list = get_files(uvm_type)
    write_files(uvm_file_list, gen_name, dest_dir)

