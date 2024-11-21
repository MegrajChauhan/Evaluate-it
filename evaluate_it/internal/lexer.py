from internal.report import log_err, log, format_string_for_highlight
from colorama import Fore, Style
from internal.defs import *
import internal.config as config

class Token:
    def __init__(self, col_st: int = 0, col_ed:int = 0, tok_type: TokenType = TokenType.TOK_ERROR, token_value: str="") -> None:
        self.type = tok_type
        self.col_st = col_st
        self.col_ed = col_ed
        self.token_value = token_value
    
    def __str__(self) -> str:
        if self.type >= TokenType.TOK_PLUS and self.type <= TokenType.TOK_MOD:
            return f"Token Identified Operator"
        return f"Token Identified: {self.token_value}"

"""
No matter how we take inputs, the Lexer will just take a single line each time and pass a list of lexed tokens as result
"""
class Lexer:
    def __init__(self, input_expr: str) -> None:
        self.col: int = 0
        self.input_expr = input_expr
        self.token_list: list[Token] = []
        self.expr_len = len(self.input_expr)
        self.curr: str = self.input_expr[0]
    
    def update(self) -> None:
        if (self.col+1) >= self.expr_len:
            self.col+=1
            return
        self.col+=1
        self.curr = self.input_expr[self.col]
    
    def obtain_digit(self) -> bool:
        log("Found a NUMBER TOKEN")
        number_token: Token = Token()
        number_token.col_st = self.col
        
        # if we want to support hexadecimal, octal or binary inputs, we may modify the logic here

        dot_count = 0
        while self.col < self.expr_len and (self.curr.isdigit() or self.curr == '.'):
            if self.curr == '.':
                dot_count+=1
            if dot_count > 1:
                log_err("Invalid floating-point value", format_string_for_highlight(self.input_expr, number_token.col_st, self.col, Fore.RED))
                if config.global_config.strict_crash:
                    log("Terminating Lexing....")
                    exit(-1)
                else:
                    return False
            number_token.token_value += self.curr
            self.update()
        
        if dot_count > 0:
            number_token.type = TokenType.TOK_FLOAT
        else:
            number_token.type = TokenType.TOK_INT
        number_token.col_ed = self.col
        self.token_list.append(number_token)
        log(f"Found NUMBER TOKEN with VALUE: {number_token.token_value}")
        return True
    
    def handle_error(self) -> None:
        log("Error while Lexing....")
        if config.global_config.strict_crash:
            log("Terminating Lexing....")
            exit(-1)
        elif not config.global_config.found_error_already:
            config.global_config.found_error_already = True
            log("LEXING ERROR DETECTED(Parsing Aborted)")
    
    def lex_all_tokens(self) -> bool:
        while True:
            current_token: Token = Token()
            if self.col >= self.expr_len:
                current_token.type = TokenType.TOK_EOF
                self.token_list.append(current_token)
                break
            if self.curr.isdigit():
                if (not self.obtain_digit()) and (not config.global_config.found_error_already):
                    config.global_config.found_error_already = True
                    log("LEXING ERROR DETECTED(Parsing Aborted)")
            else:
                # For now, we will use match cases to identify the operators
                current_token.col_st = self.col # we don't really need this info for operators
                match self.curr:
                    case '+':
                        current_token.type = TokenType.TOK_PLUS      
                    case '-':
                        current_token.type = TokenType.TOK_MINUS
                    case '*':
                        current_token.type = TokenType.TOK_MUL
                    case '/':
                        current_token.type = TokenType.TOK_DIV
                    case '%':
                        current_token.type = TokenType.TOK_MOD
                    case _:
                        log_err(f"Invalid Token '{self.curr}' found", self.input_expr)
                        self.handle_error()
                self.token_list.append(current_token)
                self.update()
        return not config.global_config.found_error_already
    
    def get_tokens_list(self) -> list[Token]:
        return self.token_list
        