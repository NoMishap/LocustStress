import sys
from src.locust_caller import call_locust_slave
from src.utils import check_argv

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


def main(argv):
    if check_argv(argv, 1, options, print_help):
        call_locust_slave(options)


if __name__ == "__main__":
    main(sys.argv[1:])
