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
    
class ASTVisualizer:
    @staticmethod
    def visualize(node: TreeNode, level: int = 0, prefix: str = "") -> None:
        """
        Recursively visualizes the AST.
        
        :param node: The current TreeNode to visualize.
        :param level: The current depth level of the node in the tree.
        :param prefix: The prefix string for indentation and formatting.
        """
        if node is None:
            return
        
        # Print the current node
        token_str = str(node.token) if node.token else "Empty Node"
        print(f"{' ' * (level * 4)}{prefix}{token_str}")
        
        # Recurse for left and right children
        # if node.token.type == defs.TokenType.TOK_SUB_EXPR:
        #     node.token = node.token.tree
        if node.left or node.right:
            ASTVisualizer.visualize(node.left, level + 1, "L-- ")
            ASTVisualizer.visualize(node.right, level + 1, "R-- ")
    
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
        return self.tokens[original_index+1:ind-1]
        
    def handle_error(self) -> None:
        config.log("Error while Parsing....")
        config.log(f"Terminating Parsing{"(STRICT CRASH HAS NO EFFECT)" if config.global_config.strict_crash else ""}....")
        exit(-1)
    
    def evaluate_sub_expressions(self) -> bool:
        current_sub_expr = self.find_token_kind(defs.TokenType.TOK_OPAREN)
        while current_sub_expr < self.tokens.__len__():
            # We now need to resolve this sub expression by finding a matching closing parenthesis
            sub_expr = self.gen_sub_expression(current_sub_expr)

            # We parse the sub_expr now!
            child_parser = Parser()
            child_parser.populate_token_list_by_sub_expr(sub_expr)
            child_parser.lexer = self.lexer # We need this for the expression string
            if not child_parser.parse():
                return False
            result: list[lexer.Token] = self.tokens[:current_sub_expr+1]
            result[current_sub_expr].type = defs.TokenType.TOK_SUB_EXPR
            result[current_sub_expr].make_token_sub_expr(child_parser.ast)
            result.extend(self.tokens[current_sub_expr+sub_expr.__len__()+2:])
            self.tokens = result
            current_sub_expr = self.find_token_kind(defs.TokenType.TOK_OPAREN)
        return True
    
    def find_the_next_node(self) -> int:
        """
        Finds the index of the next relevant token within the specified range [st, ed),
        processing tokens of one type (e.g., TOK_PLUS) fully before moving to the next type.
        """
        token_priority = [
            defs.TokenType.TOK_PLUS, defs.TokenType.TOK_MINUS,
            defs.TokenType.TOK_MUL, defs.TokenType.TOK_DIV, defs.TokenType.TOK_MOD,
            defs.TokenType.TOK_INT, defs.TokenType.TOK_FLOAT, defs.TokenType.TOK_SUB_EXPR
        ]

        for toktype in token_priority:
            for ind in range(0, len(self.tokens)):
                if self.tokens[ind].type == toktype:
                    return ind

        return len(self.tokens)
    
    def create_next_node(self) -> TreeNode:
        """
        Create the next node for the AST based on the token at start_index.
        Handles numbers, sub-expressions, and operators recursively.
        """
        start_index = self.find_the_next_node()
        if start_index >= len(self.tokens):
            report.log_err("Unexpected end of tokens while creating a node.", self.lexer.input_expr)
            self.handle_error()

        token = self.tokens[start_index]
        
        if token.type in [defs.TokenType.TOK_INT, defs.TokenType.TOK_FLOAT]:
            return TreeNode(token)
        
        if token.type == defs.TokenType.TOK_SUB_EXPR:
            return TreeNode(token.tree.root.token, token.tree.root.left, token.tree.root.right)
        
        if token.type in [defs.TokenType.TOK_PLUS, defs.TokenType.TOK_MINUS,
                          defs.TokenType.TOK_MUL, defs.TokenType.TOK_DIV, defs.TokenType.TOK_MOD]:
            temp_tokens = self.tokens
            self.tokens = self.tokens[:start_index]
            left = self.create_next_node()
            self.tokens = temp_tokens[start_index+1:]
            right = self.create_next_node()
            self.tokens = temp_tokens
            return TreeNode(token, left=left, right=right)
        
        report.log_err(f"Unexpected token: {token}", self.lexer.input_expr)
        self.handle_error()
    
    def parse(self) -> bool:
        if len(self.tokens) == 0:
            if not self.lexer.lex_all_tokens():
                return False
            self.tokens = self.lexer.get_tokens_list()

        if not self.evaluate_sub_expressions():
            return False
        
        self.ast.root = self.create_next_node()
        return True
