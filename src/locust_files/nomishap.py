from locust import HttpLocust, TaskSet, task, events, web
from datetime import datetime
import time
import sys
import requests
from urllib.parse import urlencode


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("Starting user session")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("Stopping user session")

    @task(1)
    def index(self):
        self.client.get("/x/pdfToText")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 100


stats_host = "http://88.147.126.145:8011/"
global_stats = {
    "current": 0,
    "stats_list": list()
}


def init_stats():
    stats = {
        "start": {
            "time": 0.0,
            "utc": None
        },
        "end": {
            "time": 0.0,
            "utc": None
        },
        "diff": 0.0,
        "started": False
    }
    global_stats["stats_list"].append(stats)


init_stats()


def starting():
    stats = global_stats["stats_list"][global_stats["current"]]
    if stats["started"] is False:
        stats["started"] = True
        stats["start"]["time"] = time.time()
        stats["start"]["utc"] = datetime.utcnow()


def stopping():
    stats = global_stats["stats_list"][global_stats["current"]]
    stats["end"]["time"] = time.time()
    stats["end"]["utc"] = datetime.utcnow()
    stats["diff"] = stats["end"]["time"] - stats["start"]["time"]

    write_process_time_on_file(global_stats_to_string())

    global_stats["current"] += 1

    init_stats()


def send_stats_to_host(data):
    query_string = urlencode(data)
    req = requests.post(stats_host + query_string)


def on_request_success(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    starting()
    send_stats_to_host({
        "responseTime": str(round(response_time, 3)),
        "name": "locust",
        "responseCode": 200
    })


def on_request_failure(request_type, name, response_time, exception):
    """
    Event handler that get triggered on every fiailure request
    """
    send_stats_to_host({
        "responseTime": str(round(response_time, 3)),
        "name": "locust",
        "responseCode": 200
    })


def on_master_start_hatching():
    """
    Event handler that get triggered on initiate the hatching process on the master.
    """
    starting()


def on_stop_hatching():
    stopping()


# Hook up the event listeners
events.request_success += on_request_success
events.master_start_hatching += on_master_start_hatching
events.master_stop_hatching += on_stop_hatching
events.locust_stop_hatching += on_stop_hatching


def global_stats_to_string():
    content = ""

    for index, stats in enumerate(global_stats["stats_list"]):
        content += "PROCESS TIME: execution " + str(index + 1) + "<br><br>"
        content += "Process started at: " + str(stats["start"]["utc"]) + " (utc date) <br>"
        content += "Process ended at: " + str(stats["end"]["utc"]) + " (utc date) <br><br>"
        if stats["end"]["utc"] is None and stats["start"]["utc"] is not None:
            diff = time.time() - stats["start"]["time"]
            content += "Process in execution from: " + str(round(diff, 2)) + " seconds<br>"
        else:
            diff = stats["diff"]
            content += "Process execution time was: " + str(round(diff, 2)) + " seconds<br>"

        content += "------------------------------------------------------------------------<br><br>"

    return content


def write_process_time_on_file(content):
    argv = sys.argv[1:]
    output_name = ""
    for arg in argv:
        if "--csv=" in arg:
            output_name += arg.replace("--csv=", "")

    output_name += "_process_time.txt"
    file = open(output_name, "w")
    file.write(content.replace("<br>", "\n"))

    file.close()


@web.app.route("/process_time")
def process_time():
    """
    Add a route to the Locust web app, where we can see the total content-length
    """

    return global_stats_to_string()
