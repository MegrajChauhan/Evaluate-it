# Variable names
1. Use lowercase words separated by underscores.
2. Write meaningful names that are easily understood.
3. Avoid the declaration of unnecessary global variables.

# Function names
1. Same rules as Variable names.
2. Follow the rule with the parameter names as well.
3. Provide types for the paramters.
4. Write descriptive names.
5. No need for docstrings if the names are enough.
6. Use comments if needed to describe the implementation.

# Class Names
1. Use camelcase
2. Descriptive method names and member names.
3. Mention the return type of the function

# Examples:
```python
class TestClass:
    pass

def this_does_nothing(type_of_tok: TestClass, value: str) -> int:
    pass

testing = TestClass()
```