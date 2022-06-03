from locust import HttpUser, task, between
# locust: an open source load-testing tool 

class UserBehavior(HttpUser):
# Put your stress tests here 
    wait_time = between(0.5, 1)
    @task(2)
    def index_locus(self):
        self.client.get('/')  
   
    @task(5)
    def predict_locus(self):
        image_test = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        
        self.client.post("/predict", files=image_test)
        
    
#class APIUser(HttpUser):
 #   task_set = UserBehavior
  #  min_wait = 5000
  #  max_wait = 9000
    