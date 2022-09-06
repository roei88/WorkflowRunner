import os

variable_dictionary = dict()
output = ""

# will always be the first node
def start_action():
    return

# logs the value of the input, which is either a variable (print(varname)) or plain text (print("string"))
def print_action(args):
    global output
    output = output + args['input']
    print(args['input'])
    return output

# puts the provided value in a variable with the provided name
def set_variable_action(args):
    global variable_dictionary
    variable_dictionary[args['name']] = args['value']
    return variable_dictionary

# condition node, continues execution with one path if the file exists and with another path otherwise
def file_exists_action(args):
    if os.path.exists(args['name']):
        return True
    return False

# reads the contents of the file, as a string, into a variable
def read_file_into_variable_action(args):
    global variable_dictionary
    with open(args['filename'], "r") as f:
        variable_dictionary[args['varname']] = f.read()
    return variable_dictionary

# ends the workflow
def end_action(args):
    global output
    result_dictionary = dict()
    result_dictionary[args['result']] = True
    result_dictionary["output"] = output
    print(str(result_dictionary))
