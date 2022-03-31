#!/usr/bin/python
#
# Copyright 2021 Lightstep
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from data import random_currency, random_card, random_product, random_quantity
from locust import HttpUser, LoadTestShape, task, between
import math
import random
import datetime
import pandas as pd
import numpy as np
import os


class Hipster(HttpUser):
    wait_time = between(1, 10)

    def on_start(self):
        self.index()
    
    @task(50)
    def index(self):
        self.client.get('/')

    @task(50)
    def browse_product(self):
        self.client.get("/product/" + random_product())

    @task(10)
    def add_to_cart(self):
        product = random_product()
        self.client.get("/product/" + product)
        self.client.post(
            "/cart", {"product_id": product, "quantity": random_quantity()}
        )

    @task(10)
    def view_cart(self):
        self.client.get("/cart")

    @task(20)
    def checkout(self):
        self.add_to_cart()
        self.client.post("/cart/checkout", random_card(bad=random.random() < 0.01))

    @task(1)
    def set_currency(self):
        self.client.post("/setCurrency", {"currency_code": random_currency()})

class SimulateWave(LoadTestShape):
    cache = None
    # 现实时间的多少小时等于模拟的一天
    hourly_scale = float(os.environ['HOURLY_SCALE'])
    origin_timestamp = 1648656000

    sim_scale = 20
    weekend_sim_scale = sim_scale * 0.5

    def load_period_csv(self):
        if not self.cache is None:
            return
        df = pd.read_csv('period.csv')
        self.cache = np.array(df['value'])

    def tick(self):
        self.load_period_csv()
        now_timestamp = datetime.datetime.now().timestamp()
        # 当前相当于一天之中的什么时候
        relative_time = math.modf((now_timestamp - self.origin_timestamp) / (3600 * self.hourly_scale))[0]
        weekday = int(7 * math.modf((now_timestamp - self.origin_timestamp) / (3600 * self.hourly_scale * 7))[0])
        cache_idx = min(int(relative_time * len(self.cache)), len(self.cache) - 1)

        periodicity_base_value = self.cache[cache_idx]
        noise = np.random.normal(0, 0.1 * periodicity_base_value)
        scale = self.sim_scale if weekday < 5 else self.weekend_sim_scale
        user_count = int(max(0, noise + periodicity_base_value) * scale)

        return user_count, 1

if __name__ == '__main__':
    print(f'Hourly_scale: {SimulateWave.hourly_scale}')