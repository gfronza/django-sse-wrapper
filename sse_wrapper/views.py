# -*- coding: utf-8 -*-
from sse import Sse

from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

try:
    from django.http import StreamingHttpResponse as HttpResponse
except ImportError:
    from django.http import HttpResponse

from django.utils.decorators import method_decorator

from utils import class_from_str

DEFAULT_CHANNEL = getattr(settings, 'SSE_CHANNEL_NAME', 'sse')
SSE_BACKEND_CLASS = getattr(settings, 'SSE_BACKEND_CLASS')


class EventStreamView(View):
    """
    This is the view you must use in your urls.py to expose an event stream.
    """
    channel = DEFAULT_CHANNEL

    def _generate_content(self):
        for subiterator in self.iterator():
            for bufferitem in self.sse:
                yield bufferitem

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.sse = Sse()

        # Check if there is a channel extension in kwargs.
        # This may be used to separate events of the same kind
        # by some identifier (some object id, for example)
        channel_extension = kwargs.get('channel_extension', '')
        if channel_extension:
            self.channel = '%s/%s' % (self.channel, channel_extension)

        response = HttpResponse(self._generate_content(),
                                content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        response['Software'] = 'django-sse-wrapper'
        return response

    def iterator(self):
        # get the class object from settings (or default if not specified).
        Backend = class_from_str(SSE_BACKEND_CLASS)

        # create a backend instance and subscribe the channel.
        backend = Backend()
        backend.subscribe(self.channel)

        for event, data in backend.listen():
            self.sse.add_message(event, data)
            yield
