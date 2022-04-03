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

from cProfile import label
from data import random_currency, random_card, random_product, random_quantity
from locust import HttpUser, LoadTestShape, task, between
import math
import random
import datetime
import pandas as pd
import numpy as np
import os
import prometheus_client as pc
import time

registry = pc.CollectorRegistry()
page_request = pc.Counter('page_request_count', 'Count of page visits.', labelnames=['page', 'status', 'instance'], registry=registry)
page_request_duration_sum = pc.Counter('page_request_duration_sum', 'Sum of page visit duration(ms).', labelnames=['page', 'status', 'instance'], registry=registry)
gateway_url = 'testbed-master-1:9091'
job = 'business-kpi monitoring'
hostname = str(os.getenv('HOSTNAME'))
page_request.labels(page='none', status='-1', instance=hostname)
page_request_duration_sum.labels(page='none', status='-1', instance=hostname)

class Hipster(HttpUser):
    wait_time = between(1, 10)

    def on_start(self):
        self.index()
    
    @task(50)
    def index(self):
        t0 = time.time()
        res = self.client.get('/')
        page_request.labels(
            page='home',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='home',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

    @task(50)
    def browse_product(self):
        t0 = time.time()
        res = self.client.get("/product/" + random_product())
        page_request.labels(
            page='product',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='product',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

    @task(10)
    def add_to_cart(self):
        t0 = time.time()
        product = random_product()
        res = self.client.get("/product/" + product)
        page_request.labels(
            page='product',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='product',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

        t0 = time.time()
        res = self.client.post(
            "/cart", {"product_id": product, "quantity": random_quantity()}
        )
        page_request.labels(
            page='add_cart',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='add_cart',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

    @task(10)
    def view_cart(self):
        t0 = time.time()
        res = self.client.get("/cart")
        page_request.labels(
            page='view_cart',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='view_cart',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

    @task(20)
    def checkout(self):
        t0 = time.time()
        self.add_to_cart()
        res = self.client.post("/cart/checkout", random_card(bad=random.random() < 0.01))
        page_request.labels(
            page='checkout',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='checkout',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

    @task(1)
    def set_currency(self):
        t0 = time.time()
        res = self.client.post("/setCurrency", {"currency_code": random_currency()})
        page_request.labels(
            page='currency',
            status=str(res.status_code),
            instance=hostname
        ).inc()
        page_request_duration_sum.labels(
            page='currency',
            status=str(res.status_code),
            instance=hostname
        ).inc(int((time.time() - t0) * 1000))

class SimulateWave(LoadTestShape):
    cache = None
    # 现实时间的多少小时等于模拟的一天
    hourly_scale = float(os.environ['HOURLY_SCALE'])
    origin_timestamp = 1648656000

    sim_scale = 10
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

        # 每秒向gateway报告一次
        pc.push_to_gateway(gateway=gateway_url, job=job, registry=registry, grouping_key={'instance': hostname})
        return user_count, 1

if __name__ == '__main__':
    print(f'Hourly_scale: {SimulateWave.hourly_scale}')