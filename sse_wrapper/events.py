# -*- coding: utf-8 -*-
from django.conf import settings
from utils import class_from_str


# create a reference to the backend class.
SseBackendClass = class_from_str(getattr(settings, 'SSE_BACKEND_CLASS'))


def send_event(event, data, channel):
    '''
    A handy function to send an event to a particular channel.

    Arguments:
      event     -- the name of the event to be sent.
      data      -- data (dict) to be sent along with the event.
      channel   -- the name of the channel to send event to.
    '''
    SseBackendClass().send_event(event, data, channel)
