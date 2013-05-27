# -*- coding: utf-8 -*-
from django.conf import settings

import redis
import json


CONNECTION_SETTINGS = getattr(settings, 'SSE_BACKEND_CONNECTION_SETTINGS', {})


class ConnectionPoolManager(object):
    pool = {}

    @classmethod
    def connection_pool(cls, **kwargs):
        if cls.pool:
            return cls.pool

        cls.pool = redis.ConnectionPool(
            db=kwargs.get('db', 0),
            password=kwargs.get('password', None),
            host=kwargs.get('host', 'localhost'),
            port=kwargs.get('port', 6379)
        )

        return cls.pool


class RedisBasedBackend:
    def __init__(self, *args, **kwargs):
        pool = ConnectionPoolManager.connection_pool(**CONNECTION_SETTINGS)
        self.connection = redis.Redis(connection_pool=pool)
        self.pubsub = self.connection.pubsub()

    def send_event(self, event, data, channel):
        self.connection.publish(channel, json.dumps([event, data]))

    def subscribe(self, channel):
        self.pubsub.subscribe(channel)

    def listen(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event, data = json.loads(message['data'].decode('utf-8'))
                yield event, data
