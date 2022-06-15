
from urllib.parse import MAX_CACHE_SIZE
from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    # Put your stress tests here
    # TODO
    @task
    def index(self):
        self.client.get("http://localhost/")

    @task(3)
    def predict(self):
        files = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        headers = {}
        payload = {}
        self.client.post(
            "http://localhost/predict",
            headers=headers,
            data=payload,
            files=files,
        )

        

class APIUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 5000