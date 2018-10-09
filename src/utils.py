

def check_argv(argv, min_length, options, print_help):
    """
    :param argv: arguments
    :param min_length: min length of the argv array
    :param options: options dictionary with argument to search
    :param print_help: callable function with help message
    :return:
    """
    if any("-h" == arg for arg in argv) or any("--help" == arg for arg in argv):
        print_help()

    if len(argv) > min_length:
        for arg in argv:
            for key in options.keys():
                arg_key = options[key]['arg']
                if arg_key in arg:
                    options[key]['value'] = arg.replace(arg_key, '')
        return True
    else:
        print_help()
