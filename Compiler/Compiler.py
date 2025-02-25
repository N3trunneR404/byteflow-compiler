from .Exceptions import BFSyntaxError, BFSemanticError
from .FunctionCompiler import FunctionCompiler
from .Functions import check_function_exists, get_function_object, insert_function_object
from .General import is_token_literal, get_literal_token_code, unpack_literal_tokens_to_array_dimensions
from .Globals import get_global_variables_size, get_variable_size, get_variable_dimensions, insert_global_variable, create_variable_from_definition
from .Lexical_analyzer import analyze
from .Optimizer import optimize
from .LibraryFunctionCompiler import insert_library_functions
from .Parser import Parser
from .Token import Token

"""
This file handles the compilation process of C-like code into Byteflow code.
It creates FunctionCompiler objects for functions and manages global variables.
Finally, it returns the Byteflow code for the main function.
"""

class Compiler:
    def __init__(self, code, optimize_code=False):
        # Tokenize the input code
        tokens = analyze(code)
        # Optionally optimize the tokens
        if optimize_code:
            optimize(tokens)
        # Initialize the parser with the tokens
        self.parser = Parser(tokens)

    def create_function_object(self):
        # Create a FunctionCompiler object for a function definition
        if self.parser.current_token().type not in [Token.VOID, Token.INT]:
            raise BFSemanticError("Function return type can be either void or int, not '%s'" % str(self.parser.current_token()))

        self.parser.check_next_tokens_are([Token.ID, Token.LPAREN])

        # Get the function name and find the matching parentheses and braces
        function_name = self.parser.next_token(next_amount=1).data
        RPAREN_index = self.parser.find_matching(starting_index=self.parser.current_token_index + 2)
        self.parser.check_next_token_is(Token.LBRACE, starting_index=RPAREN_index)
        RBRACE_index = self.parser.find_matching(starting_index=RPAREN_index + 1)

        # Extract the tokens for the function and create a FunctionCompiler object
        function_tokens = self.parser.tokens[self.parser.current_token_index:RBRACE_index + 1]
        self.parser.advance_to_token_at_index(RBRACE_index + 1)
        function = FunctionCompiler(function_name, function_tokens)
        return function

    def compile_global_variable_definition(self):
        # Compile a global variable definition and return the initialization code
        self.parser.check_current_tokens_are([Token.INT, Token.ID])
        ID_token = self.parser.next_token()
        variable = create_variable_from_definition(self.parser, advance_tokens=True)
        insert_global_variable(variable)

        ZERO_CELLS_BEFORE_USE = False
        code = '[-]' if ZERO_CELLS_BEFORE_USE else ''

        if get_variable_size(variable) > 1:  # It's an array
            if self.parser.current_token().type == Token.SEMICOLON:
                self.parser.advance_token()  # Skip SEMICOLON
                code = (code + '>') * get_variable_size(variable)  # Advance to after this variable
                return code
            elif self.parser.current_token().type == Token.ASSIGN and self.parser.current_token().data == "=":
                self.parser.advance_token()  # Skip ASSIGN

                if self.parser.current_token().type not in [Token.LBRACE, Token.STRING]:
                    raise BFSyntaxError("Expected LBRACE or STRING at '%s'" % self.parser.current_token())

                literal_tokens_list = self.parser.compile_array_initialization_list()
                self.parser.check_current_token_is(Token.SEMICOLON)
                self.parser.advance_token()  # Skip SEMICOLON

                array_dimensions = get_variable_dimensions(variable)
                unpacked_literals_list = unpack_literal_tokens_to_array_dimensions(ID_token, array_dimensions, literal_tokens_list)

                for literal in unpacked_literals_list:
                    code += get_literal_token_code(literal)  # Evaluate this literal and point to next array element
                return code
            else:
                raise BFSyntaxError("Unexpected %s in array definition. Expected SEMICOLON (;) or ASSIGN (=)" % self.parser.current_token())

        elif self.parser.current_token().type == Token.SEMICOLON:  # No need to initialize
            self.parser.advance_token()  # Skip SEMICOLON
            code += '>'  # Advance to after this variable
        else:
            self.parser.check_current_token_is(Token.ASSIGN)
            if self.parser.current_token().data != "=":
                raise BFSyntaxError("Unexpected %s when initializing global variable. Expected ASSIGN (=)" % self.parser.current_token())
            self.parser.advance_token()  # Skip ASSIGN

            if not is_token_literal(self.parser.current_token()):
                raise BFSemanticError("Unexpected '%s'. expected literal (NUM | CHAR | TRUE | FALSE )" % str(self.parser.current_token()))

            code += get_literal_token_code(self.parser.current_token())

            self.parser.check_next_token_is(Token.SEMICOLON)
            self.parser.advance_token(amount=2)  # Skip (NUM|CHAR|TRUE|FALSE) SEMICOLON

        return code

    def process_global_definitions(self):
        """
        Process tokens to handle function and global variable definitions.
        Create FunctionCompiler objects for functions and compile global variables.
        Returns initialization code for global variables.
        """
        code = ''
        token = self.parser.current_token()
        while token is not None and token.type in [Token.VOID, Token.INT, Token.SEMICOLON]:
            if token.type == Token.SEMICOLON:  # Can have random semicolons
                self.parser.advance_token()
                token = self.parser.current_token()
                continue
            self.parser.check_next_token_is(Token.ID)

            if self.parser.next_token(next_amount=2).type == Token.LPAREN:
                function = self.create_function_object()
                insert_function_object(function)
            elif token.type is Token.INT and self.parser.next_token(next_amount=2).type in [Token.SEMICOLON, Token.ASSIGN, Token.LBRACK]:
                code += self.compile_global_variable_definition()
            else:
                raise BFSyntaxError("Unexpected '%s' after '%s'. Expected '(' (function definition) or one of: '=', ';', '[' (global variable definition)" % (str(self.parser.next_token(next_amount=2)), str(self.parser.next_token())))

            token = self.parser.current_token()

        if self.parser.current_token() is not None:  # We have not reached the last token
            untouched_tokens = [str(t) for t in self.parser.tokens[self.parser.current_token_index:]]
            raise BFSyntaxError("Did not reach the end of the code. Untouched tokens:\n%s" % untouched_tokens)

        return code

    def compile(self):
        # Insert library functions and process global definitions
        insert_library_functions()
        code = self.process_global_definitions()  # Code that initializes global variables and advances pointer to after them

        # Ensure the main function exists and get its code
        check_function_exists(Token(Token.ID, 0, 0, "main"), 0)
        code += get_function_object("main").get_code(get_global_variables_size())
        code += "<" * get_global_variables_size()  # Point to the first cell to end the program nicely
        return code


def compile(code, optimize_code=False):
    """
    Compile C-like code into Byteflow code.

    :param code: C-like code (string)
    :param optimize_code: Whether to optimize the code (bool)
    :return: Byteflow code (string)
    """
    compiler = Compiler(code, optimize_code)
    brainfuck_code = compiler.compile()
    return brainfuck_code


if __name__ == '__main__':
    print("This file cannot be directly run")
    print("Please import it and use the 'compile' function")
    print("Which receives a C-like code (string) and returns Brainfuck code (string)")
