import internal.config as config
import internal.report as report
import internal.defs as defs
import internal.lexer as lexer
from colorama import Fore

# we need to build a tree
class TreeNode:
    
    # left and right are actually TreeNode types
    def __init__(self, token: lexer.Token=None, left= None, right=None) -> None:
        self.token = token
        self.right = right
        self.left = left
        
    def get_node(self) -> lexer.Token:
        return self.token
    
    def get_left_node(self):
        return self.left 
    
    def get_right_node(self):
        return self.right

class AST:
    def __init__(self) -> None:
        self.root: TreeNode = TreeNode()
    
class Parser:
    def __init__(self, input_expr: str="") -> None:
        self.lexer = lexer.Lexer(input_expr)
        self.ast = AST()
        self.tokens: list[lexer.Token] = []
    
    def populate_token_list_by_lexing(self) -> None:
        if not self.lexer.lex_all_tokens():
            self.handle_error()
        self.tokens = self.lexer.get_tokens_list()
    
    def populate_token_list_by_sub_expr(self, sub_expr: list[lexer.Token]) -> None:
        self.tokens = sub_expr
    
    # we return an index to the requested token
    def find_token_kind(self, kind: defs.TokenType) -> int:
        ind = 0
        for tok in self.tokens:
            if tok.type == kind:
                return ind
            ind+=1
        return ind
    
    def gen_sub_expression(self, ind: int) -> list[lexer.Token]:
        config.log("Generating SUB EXPRESSION...")
        opening_paren_count = 1
        original_index = ind
        ind += 1
        while opening_paren_count != 0:
            if ind >= self.tokens.__len__():
                report.log_err("Invalid expression- No closing parenthesis found.",report.format_string_for_highlight(self.lexer.input_expr, self.tokens[ind-1].col_st, self.tokens[ind-1].col_ed, Fore.RED))
                self.handle_error()
            if self.tokens[ind].type == defs.TokenType.TOK_OPAREN:
                opening_paren_count += 1
            elif self.tokens[ind].type == defs.TokenType.TOK_CPAREN:
                opening_paren_count -= 1
            ind += 1
        
        # If we are out then ind should be the index of the closing parenthesis
        return self.tokens[original_index:ind]
        
    def handle_error(self) -> None:
        config.log("Error while Parsing....")
        config.log(f"Terminating Parsing{"(STRICT CRASH HAS NO EFFECT)" if config.global_config.strict_crash else ""}....")
        exit(-1)
    
    def evaluate_sub_expressions(self) -> bool:
        current_sub_expr = self.find_token_kind(defs.TokenType.TOK_OPAREN)
        if current_sub_expr >= self.tokens.__len__():
            return True # we are done with sub expressions
        
        # We now need to resolve this sub expression by finding a matching closing parenthesis
        sub_expr = self.gen_sub_expression(current_sub_expr + 1)
        
        # We parse the sub_expr now!
        child_parser = Parser()
        child_parser.populate_token_list_by_sub_expr(sub_expr)
        child_parser.lexer = self.lexer # We need this for the expression string
        if not child_parser.parse():
            return False
        result: list[lexer.Token] = self.tokens[:current_sub_expr+1]
        result[current_sub_expr].type = defs.TokenType.TOK_SUB_EXPR
        result[current_sub_expr].make_token_sub_expr(child_parser.ast)
        result.extend(self.tokens[current_sub_expr+sub_expr.__len__()+1:])
        self.tokens = result
        return True
    
    def find_the_next_node(self) -> int:
        tokens_length = len(self.tokens)
        # if self.find_token_kind(defs.TokenType.TOK_MOD)
    
    def parse(self) -> bool:
        if len(self.tokens) == 0:
            if not self.lexer.lex_all_tokens():
                return False
            self.tokens = self.lexer.get_tokens_list()
        # Start parsing the expression:
        # 1) Find the parenthesis and build the expression of them first
        # 2) Finally move on to the rest of the expression
        if not self.evaluate_sub_expressions():
            return False
        
        # We now have basic NUMBERS, OPERATORS and SUB EXPRESSIONS to evaluate
        
        
        return True