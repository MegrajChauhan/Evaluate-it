"""
Define some configurable vairables that define the state of the module
"""

class Config:
    in_debug_state = False      # Is the module in Debug state?
    verbose = False             # Should the module be verbose?
    strict_crash = True         # If True, an error will cause a crash with error message otherwise the entire line will be lexed and all errors will be displayed at once
                                # The errors will be displayed for only the active stage i.e if the error was in the Lexing stage, we won't enter the parsing state at all
    found_error_already = False # Has any error been encountered already? Propagate the message to the entire module
    
global_config = Config()