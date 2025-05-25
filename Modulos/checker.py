import re

def verify_number(numero):
    regex = re.compile(r"^\+?\d{0,3}\d{10}$") #^matches the start of the line, with \ we scape the special + and whe put a ? to say it's optional that tell us it should begin with 0 to three characters and then the 10 digits with $ to end the string
    result = regex.match(numero)
    return result


def verify_date(fecha):
    regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
    result = regex.match(fecha)
    return result


"""
Checks if the user input in the menu is a valid option. It asumes the options in
    the menu are in a number range, that means, the options will be [1, 2, 3, 4, 5], 
    not [10, 32, 86, 102]. And in case the input is a valid option, in will return
    the selected option.

Arguments:
    user_input(str): is the value the user typed
    starting_range(int): is the start of the range, inclusive
    ending_range(int): is the end of the range, inclusive

Returns:
    bool: if the option is false
    int: the selected option
"""
def check_valid_option(user_input: str, starting_range: int, ending_range: int) -> int | bool:
    if not user_input.isdecimal():
        return False
    
    user_input_int = int(user_input)
    if user_input_int > ending_range or user_input_int < starting_range:
        return False
    
    return user_input_int
