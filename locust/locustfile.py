import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get("reservation_unit/")
        self.client.get("resource/")
        self.client.get("application_round/")
        self.client.get("parameters/district/")
        self.client.get("allocation_request/")
        self.client.get("allocation_results/")
        self.client.get("parameters/purpose/")
        self.client.get("parameters/age_group/")
        self.client.get("parameters/ability_group/")
        self.client.get("parameters/reservation_unit_type/")
        self.client.get("parameters/equipment_category/")
        self.client.get("parameters/equipment/")
        self.client.get("parameters/city/")

