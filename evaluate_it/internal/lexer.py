from report import log_err, log_msg, format_string_for_highlight

class Lexer:
    def __init__(self, input_expr):
        self.col = 0
        self.input_expr = input_expr
        