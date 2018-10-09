import sys
from src.locust_caller import call_locust_slave

options = {
        "file": {
            "arg": "-f=",
            "value": "locustfile.py"
        },
        "master_host": {
            "arg": "--master-host=",
            "value": None
        },
        "output": {
            "arg": "-o=",
            "value": "test"
        }
    }


def print_help():
    print("locust_slave.py -f=[file] --master-host=[host] -o=[output", end="\n\n")
    print("Required:")
    print("-f=[file]: set file name, default locustfiles.py optional param, this file must be "
          "located in src/locust_files folder")
    print("--master-host=[host]: set the master host value")
    print("Optional:")
    print("-o=[output]: the prefix value of the csv output data ([output]_distribution.csv and [output]_requests.csv). "
          "This param is optional default is 'test'")
    print("-h or --help: to view this message", end="\n\n")
    exit(0)


def check_argv(argv):
    if any("-h" == arg for arg in argv) or any("--help" == arg for arg in argv):
        print_help()

    if len(argv) > 1:
        for arg in argv:
            for key in options.keys():
                arg_key = options[key]['arg']
                if arg_key in arg:
                    options[key]['value'] = arg.replace(arg_key, '')
        return True
    else:
        print_help()


def main(argv):
    if check_argv(argv):
        call_locust_slave(options)


if __name__ == "__main__":
    main(sys.argv[1:])
