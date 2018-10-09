import sys, time
from datetime import datetime
from src.locust_caller import call_locust

options = {
    "file": {
        "arg": "-f=",
        "value": "locustfile.py"
    },
    "host": {
        "arg": "--host=",
        "value": None
    },
    "no_web": {
        "arg": "--no-web",
        "value": False
    },
    "num_call": {
        "arg": "-c=",
        "value": 0
    },
    "users_for_second": {
        "arg": "-r=",
        "value": 0
    },
    "time": {
        "arg": "-t=",
        "value": None
    },
    "output": {
        "arg": "-o=",
        "value": "test"
    }
}


def print_help():
    print(
        "locust_standalone.py -f=[file] --host=[host] --no-web -c=[num_call] -r=[users_for_second] -t=[time] -o=[output",
        end="\n\n")
    print("Required:")
    print("-f=[file]: set file name, default locustfiles.py optional param, this file must be "
          "located in src/locust_files folder")
    print("--host=[host]: set the host value")
    print("Optional:")
    print("--no-web: with this options you can run locust without web gui")
    print("-c=[num_call]: number of user to simulate")
    print("-r=[users_for_second]: number of user spawn for second")
    print("-t=[time]: execute for time example: 1m execute for 1 minute or 1h30m execute for 1 hour and 30 minutes. "
          "This param is optional default is 1m")
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
        start = time.time()
        print(datetime.utcnow())
        call_locust(options)
        end = time.time()
        print(datetime.utcnow())
        print("Execution done by: " + str(end-start))


if __name__ == "__main__":
    main(sys.argv[1:])
