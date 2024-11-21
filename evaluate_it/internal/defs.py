"""
   Contains the definitions for the entire module
"""

import enum

class TokenType(enum.IntEnum):
    TOK_INT = 0
    TOK_FLOAT = 1
    TOK_PLUS = 2
    TOK_MINUS = 3
    TOK_DIV = 4
    TOK_MUL = 5
    TOK_MOD = 6
    TOK_ERROR = 255
    TOK_EOF = 256

class NodeKind(enum.Enum):
    pass

# We will use Dictionaries to easily map tokens to their types
value_to_token_map = {
    "+": TokenType.TOK_PLUS,
    "-": TokenType.TOK_MINUS,
    "*": TokenType.TOK_MUL,
    "/": TokenType.TOK_DIV,
    "%": TokenType.TOK_MOD,
}

def get_token_type_from_value(value: str) -> TokenType:
    if not value_to_token_map.__contains__(value):
        return TokenType.TOK_ERROR
    return value_to_token_map[value]