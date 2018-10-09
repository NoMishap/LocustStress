from locust import HttpLocust, TaskSet, task, events, web
from datetime import datetime
import time, sys


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("Starting user session")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("Stopping user session")

    @task(1)
    def index(self):
        self.client.get("/pdfservice/pdfToText")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 100


stats = {
    "start": {
        "time": None,
        "utc": None
    },
    "end": {
        "time": None,
        "utc": None
    },
    "diff": 0.0,
    "started": False
}


def starting():
    if stats["started"] is False:
        stats["started"] = True
        stats["start"]["time"] = time.time()
        stats["start"]["utc"] = datetime.utcnow()


def on_request_success(request_type, name, response_time, response_length):
    """
    Event handler that get triggered on every successful request
    """
    starting()


def on_master_start_hatching():
    """
    Event handler that get triggered on initiate the hatching process on the master.
    """
    starting()


def on_stop_hatching():
    stats["end"]["time"] = time.time()
    stats["end"]["utc"] = datetime.utcnow()
    stats["diff"] = stats["end"]["time"] - stats["start"]["time"]

    content = "PROCESS TIME<br><br>"
    content += "Process started at: " + str(stats["start"]["utc"]) + " (utc date) <br>"
    content += "Process ended at: " + str(stats["end"]["utc"]) + " (utc date) <br><br>"
    content += "Porcess execution time was: " + str(round(stats["diff"], 2)) + " seconds"

    write_process_time_on_file(content)


# Hook up the event listeners
events.request_success += on_request_success
events.master_start_hatching += on_master_start_hatching
events.master_stop_hatching += on_stop_hatching
events.locust_stop_hatching += on_stop_hatching


def write_process_time_on_file(content):
    argv = sys.argv[1:]
    output_name = ""
    for arg in argv:
        print(arg)
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
    content = "PROCESS TIME<br><br>"
    content += "Process started at: " + str(stats["start"]["utc"]) + " (utc date) <br>"
    content += "Process ended at: " + str(stats["end"]["utc"]) + " (utc date) <br><br>"
    content += "Porcess execution time was: " + str(round(stats["diff"], 2)) + " seconds"

    return content
