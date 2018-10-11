from locust import events
from datetime import datetime
import time
import sys
import requests
import os


def write_process_time_on_file(content, file_prefix):
    output_name = file_prefix + "_process_time.txt"
    file = open(output_name, "w")
    file.write(content.replace("<br>", "\n"))

    file.close()


def send_stats_to_host(data, host):
    raw_data = ""
    for key in data.keys():
        raw_data += key + "=" + str(data[key]) + " "
    requests.post(host, data=raw_data)


def send_stats_to_local(data, file_prefix):
    output_name = file_prefix + "_stats.log"
    content = "code " + str(data["responseCode"]) + " | " + "time " + data["responseTime"] + "\n"
    file = open(output_name, "a")
    file.write(content)

    file.close()


def send_stats(data, host, file_name_prefix):
    logger = os.environ["LOGGER"]
    if logger == "http":
        send_stats_to_host(data, host)
    elif logger == "local":
        send_stats_to_local(data, file_name_prefix)


class EventHandler:

    def __init__(self):
        self.stats_host = "http://88.147.126.145:8011"
        self.current = 0
        self.stats_list = list()
        self.stats_list.append({
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
        })
        self.output_file_prefix = ""
        self.set_output_file_prefix()

    def add_callback_to_event(self):
        events.request_success += self.on_request_success
        events.master_start_hatching += self.on_master_start_hatching
        events.master_stop_hatching += self.on_stop_hatching
        events.locust_stop_hatching += self.on_stop_hatching

    def reinit(self):
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
        self.stats_list.append(stats)

    def stats_to_string(self):
        content = ""

        for index, stats in enumerate(self.stats_list):
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

    def starting(self):
        stats = self.stats_list[self.current]
        if stats["started"] is False:
            stats["started"] = True
            stats["start"]["time"] = time.time()
            stats["start"]["utc"] = datetime.utcnow()

        self.stats_list[self.current] = stats

    def stopping(self):
        stats = self.stats_list[self.current]
        stats["end"]["time"] = time.time()
        stats["end"]["utc"] = datetime.utcnow()
        stats["diff"] = stats["end"]["time"] - stats["start"]["time"]

        self.stats_list[self.current] = stats

        write_process_time_on_file(self.stats_to_string(), self.output_file_prefix)

        self.current += 1

        self.reinit()

    def on_request_success(self, request_type, name, response_time, response_length):
        """
        Event handler that get triggered on every successful request
        """
        self.starting()
        send_stats({
            "responseTime": str(round(response_time, 1)),
            "name": "locust",
            "responseCode": 200
        }, self.stats_host, self.output_file_prefix)

    def on_request_failure(self, request_type, name, response_time, exception):
        """
        Event handler that get triggered on every fiailure request
        """
        send_stats({
            "responseTime": str(round(response_time, 1)),
            "name": "locust",
            "responseCode": 200
        }, self.stats_host, self.output_file_prefix)

    def on_master_start_hatching(self):
        """
        Event handler that get triggered on initiate the hatching process on the master.
        """
        self.starting()

    def on_stop_hatching(self):
        self.stopping()

    def set_output_file_prefix(self):
        argv = sys.argv[1:]
        for arg in argv:
            if "--csv=" in arg:
                self.output_file_prefix = arg.replace("--csv=", "")
