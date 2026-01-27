import configparser
from pathlib import Path
from uvm_comp_setting import uvm_comp_setting

# Path to the current script
cfg = configparser.ConfigParser()
cfg.read('cfg.ini', encoding='utf-8')

script_dir = Path(__file__).parent

uvm_tree_comp_list = ["AGENT"]

def get_path(cfg: configparser.ConfigParser) -> str:
    path = cfg['PROJECT_SETTING']['PATH']
    return path

def collect_uvm_comp_setting_list_by_module(cfg: configparser.ConfigParser, uvm_comp: str, proj_path: str) -> list[uvm_comp_setting]:
    module_cnt = 0
    uvm_comp_list = []
    while True:
        if not cfg.has_section(f'{uvm_comp}{module_cnt}'):
            break
        uvm_comp_tmp = uvm_comp_setting()
        uvm_comp_tmp.get_setting(setting=cfg[f'{uvm_comp}{module_cnt}'], type=uvm_comp, proj_path=proj_path)
        module_cnt += 1
        uvm_comp_list.append(uvm_comp_tmp)
    return uvm_comp_list

def collect_uvm_comp_setting_list(cfg: configparser.ConfigParser, proj_path: str) -> list[uvm_comp_setting]:
    uvm_comp_setting_list = []
    for uvm_tree_comp in uvm_tree_comp_list:
        uvm_comp_setting_list += collect_uvm_comp_setting_list_by_module(cfg=cfg, uvm_comp=uvm_tree_comp, proj_path=proj_path)
    return uvm_comp_setting_list

def create_uvm_files(uvm_comp_list: list[uvm_comp_setting]) -> None:
    for uvm_comp in uvm_comp_list:
        uvm_comp.create_uvm_component(script_dir)

if __name__ == '__main__':
    dest_dir = get_path(cfg)
    uvm_comp_list = collect_uvm_comp_setting_list(cfg=cfg, proj_path=dest_dir)
    create_uvm_files(uvm_comp_list)

