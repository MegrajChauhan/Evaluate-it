import internal.parser as parser
import internal.config as config
import internal.report as report
import internal.defs as defs

class Evaluator:
    def __init__(self, ast_tree: parser.AST) -> None:
        self.tree = ast_tree
    
    def handle_error(self) -> None:
        config.log("Error while Evaluation....")
        config.log(f"Terminating{"(STRICT CRASH HAS NO EFFECT)" if config.global_config.strict_crash else ""}....")
        exit(-1)
    
    def evaluate_node(self, node: parser.TreeNode) -> float:
        """
        Recursively evaluates the given TreeNode.
        - Leaf nodes (TOK_INT, TOK_FLOAT): return their value.
        - Operator nodes: evaluate left and right children and apply the operation.
        """
        if node is None or node.token is None:
            return 0

        if node.token.type == defs.TokenType.TOK_INT:
            return int(node.token.token_value)
        elif node.token.type == defs.TokenType.TOK_FLOAT:
            return float(node.token.token_value)

        if node.token.type == defs.TokenType.TOK_SUB_EXPR:
            return self.evaluate_node(node.left)

        if node.token.type in [defs.TokenType.TOK_PLUS, defs.TokenType.TOK_MINUS,
                               defs.TokenType.TOK_MUL, defs.TokenType.TOK_DIV,
                               defs.TokenType.TOK_MOD]:
            left_value = self.evaluate_node(node.left)
            right_value = self.evaluate_node(node.right)

            if node.token.type == defs.TokenType.TOK_PLUS:
                return left_value + right_value
            elif node.token.type == defs.TokenType.TOK_MINUS:
                return left_value - right_value
            elif node.token.type == defs.TokenType.TOK_MUL:
                return left_value * right_value
            elif node.token.type == defs.TokenType.TOK_DIV:
                if right_value == 0:
                    report.log_err("Divide by zero")
                    self.handle_error()
                return left_value / right_value
            elif node.token.type == defs.TokenType.TOK_MOD:
                if right_value == 0:
                    report.log_err("Divide by zero")
                    self.handle_error()
                return left_value % right_value

        # If no valid token type is matched, raise an error
        report.log_err("Unexpected token during evaluation...")

    def evaluate(self) -> float:
        """
        Starts the evaluation of the AST from its root.
        """
        self.result = self.evaluate_node(self.tree.root)
        return self.result
