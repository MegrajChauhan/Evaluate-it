"""
Define some configurable vairables that define the state of the module
"""

import internal.report as report

class Config:
    in_debug_state = False      # Is the module in Debug state?
    verbose = False             # Should the module be verbose?
    strict_crash = True         # If True, an error will cause a crash with error message otherwise the entire line will be lexed and all errors will be displayed at once
                                # The errors will be displayed for only the active stage i.e if the error was in the Lexing stage, we won't enter the parsing state at all
    found_error_already = False # Has any error been encountered already? Propagate the message to the entire module
    
global_config = Config()

"""
  If verbosity is enabled, we use the default function else the useless function
"""
log = report.log_msg

def report_init() -> None:
    global log
    if not global_config.verbose and not global_config.in_debug_state:
        log = report.useless_log