from locust import HttpLocust, TaskSet, task, events, web
from datetime import datetime
import time


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print("Starting user session")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print("Stopping user session")

    @task(1)
    def index(self):
        self.client.get("/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 100


stats = {
    "start": {
        "time": time.time(),
        "utc": datetime.utcnow()
    },
    "end": {
        "time": None,
        "utc": None
    },
    "diff": 0.0
}
print(stats)


def on_master_stop_hatching():
    stats["end"]["time"] = time.time()
    stats["end"]["utc"] = datetime.utcnow()
    stats["diff"] = stats["end"]["time"] - stats["start"]["time"]
    print(stats)


# Hook up the event listeners
events.master_stop_hatching += on_master_stop_hatching


@web.app.route("/process_time")
def process_time():
    """
    Add a route to the Locust web app, where we can see the total content-length
    """
    return "Process time was: \n" + str(stats)
