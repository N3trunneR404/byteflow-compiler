from copy import deepcopy
from .Exceptions import BFSemanticError

functions = dict()  # Global dictionary to store function_name --> FunctionCompiler objects


def insert_function_object(function):
    # Add a function object to the global dictionary
    functions[function.name] = function


def get_function_object(name):
    """
    Return a copy of the function object from the global dictionary.
    We return a copy because we might need to compile the function recursively.
    If we don't use different copies, we could mess up the current token pointer and other states.

    Example:
        int increase(int n) { return n+1;}
        int main() {int x = increase(increase(1));}

    When compiling the first call to 'increase', we start compiling the same function object again for the second call.
    """
    return deepcopy(functions[name])


def check_function_exists(function_token, parameters_amount):
    # Check if a function with the given name exists in the global dictionary
    function_name = function_token.data
    if function_name not in functions:
        raise BFSemanticError("Function '%s' is undefined" % str(function_token))

    # Check if the function has the correct number of parameters
    function = functions[function_name]
    if len(function.parameters) != parameters_amount:
        raise BFSemanticError("Function '%s' has %s parameters (called it with %s parameters)" % (str(function_token), len(function.parameters), parameters_amount))
