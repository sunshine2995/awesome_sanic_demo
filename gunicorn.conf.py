# -*- coding: utf-8 -*-

import os


bind = "0.0.0.0:18100"
workers = os.cpu_count() * 2 + 1
worker_class = "sanic.worker.GunicornWorker"
