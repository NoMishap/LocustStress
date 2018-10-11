from locust import HttpLocust, TaskSet, task, web
from event.event_handler import EventHandler


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


event_handler = EventHandler()

# Hook up the event listeners
event_handler.add_callback_to_event()


@web.app.route("/process_time")
def process_time():
    """
    Add a route to the Locust web app, where we can see the total content-length
    """

    return event_handler.stats_to_string()
