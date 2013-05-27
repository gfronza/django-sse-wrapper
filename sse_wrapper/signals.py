# -*- coding: utf-8 -*-
from django.dispatch import Signal


sse_message_sent = Signal(providing_args=['event', 'data', 'channel'])
