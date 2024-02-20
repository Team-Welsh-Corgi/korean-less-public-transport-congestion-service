import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    x_auth_token = ""

    @task
    def view_items(self):
        self.client.headers = {
            "Content-Type": "application/json",
            "X-AUTH-TOKEN": self.x_auth_token
        }
        self.client.get(url="http://localhost:524/getCongestion")
        time.sleep(1)

    def on_start(self):
        for name_index in range(10):
            self.client.get(f"http://localhost:524/getCongestion?BusID=10000&StationID1=10000&StationID2=10000", name="/getCongestion")