"""
  Define logging functions
"""
from colorama import Fore, Style, ansi
import internal.config as config

def log_msg(msg: str) -> None:
    print(f"{Fore.BLUE}LOG:{Style.RESET_ALL} {msg}")
    
def format_string_for_highlight(line:str, col_st: int, col_ed: int, color:ansi.AnsiFore=Fore.WHITE) ->str:
    # There are no checks here because we trust ourselves and the lexer
    result = line[:col_st]              
    result += color                
    result += line[col_st:col_ed]       
    result += Style.RESET_ALL           
    result += line[col_ed:]             
    return result

def log_err(err_msg: str, input_line: str='') -> None:
    print(f"\n{Fore.RED}ERROR:{Style.RESET_ALL} {err_msg}{"\n\t" + input_line if len(input_line) > 0 else ""}\n")
    if config.global_config.strict_crash:
        exit()

def useless_log(msg: str) -> None:
    pass
    
