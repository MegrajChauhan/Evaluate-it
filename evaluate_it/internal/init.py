from colorama import init
import internal.config as config
import internal.report as report
import internal.lexer as lexer
import os

"""
This is where the entire module may be configured for things such as:
1) Taking input from STDIO or a file.
2) Run in an event loop or run just once etc
"""
def evaluate_it_init(_in_debug_mode: bool, _be_verbose: bool, strictly_crash: bool) -> None:
    init()
    config.global_config.in_debug_state = _in_debug_mode
    config.global_config.strict_crash = strictly_crash
    config.global_config.verbose = _be_verbose
    report.report_init()
    
def print_terminal_io_start_info() -> None:
    print("Welcome to Evaluate It!")
    print("You are using version-0.0.0")

def evaluate_it() -> None:
    # For now, our only way to get input is via the terminal
    print_terminal_io_start_info()
    while True:
        expr: str = input(">>> ")
        if len(expr) > 0:
            if expr in ["exit", "quit", "q"]:
                return
            elif expr == "clear":
                os.system("clear")
                continue
            evaluate_it_lexer = lexer.Lexer(expr) 
            if not evaluate_it_lexer.lex_all_tokens():
                exit(-1)
            # Move on to the next step
            all_tokens = evaluate_it_lexer.get_tokens_list()
            for token in all_tokens:
                print(token)