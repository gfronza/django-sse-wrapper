# -*- coding: utf-8 -*-
import time

from sse_wrapper.signals import sse_message_sent


class MemoryBasedBackend:
    '''
    Represents a very simple in-memory broker backend.
    Should only be used for testing purpose.
    '''
    def __init__(self, *args, **kwargs):
        self.reset_state()

    def reset_state(self):
        self.last_event = None
        self.last_data = None

    def send_event(self, event, data, channel):
        sse_message_sent.send(sender=self, event=event,
                              data=data, channel=channel)

    def subscribe(self, channel):
        def handle_message_sent(sender, event, data, **kwargs):
            self.last_event = event
            self.last_data = data

        sse_message_sent.connect(handle_message_sent,
                                 weak=False,
                                 dispatch_uid='memory_based_backend')

    def listen(self):
        while True:
            while self.last_event is None:
                time.sleep(1)

            yield self.last_event, self.last_data
            self.reset_state()
