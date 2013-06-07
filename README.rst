Django SSE Wrapper
==================

Django SSE wrapper is an easy way to implement Server-Sent Events (http://www.html5rocks.com/en/tutorials/eventsource/basics/) in a Django application.


Installation
------------

    $ pip install django-sse-wrapper


Usage
-----

Django SSE Wrapper exposes a view called ``EventStreamView`` that implements the SSE logic.
In your ``urls.py`` you will specify a pattern like:

.. code-block:: python

    from django.conf.urls import patterns, url

    from sse_wrapper.views import EventStreamView


    urlpatterns = patterns(
        '',
        url(r'^an-event-stream/$',
            EventStreamView.as_view(channel='some-channel-name'),
            name='an_event_stream'),
    )

You can also specify a channel extension. This may be useful, for example, when you have an event stream called course_state_stream, but that needs to differ from one course to another (by course_id, for example). The url pattern would look like:

.. code-block:: python

    from django.conf.urls import patterns, url

    from sse_wrapper.views import EventStreamView


    urlpatterns = patterns(
        '',
        url(r'^course-state-stream/(?P<channel_extension>[\w]+)/$',
            EventStreamView.as_view(channel='course-state'),
            name='course_state_stream'),
    )


Brokers
-------

For now, I only support two backend brokers: Memory (testing purpose only) and Redis. Soon I'll be adding support to RabbitMQ, ZeroMQ, and others.

In your settings.py you must specify the broker and its properties:

.. code-block:: python

    SSE_BACKEND_CLASS = 'sse_wrapper.backends.redis_based.RedisBasedBackend'
    SSE_BACKEND_CONNECTION_SETTINGS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }


Production Environment Notes
----------------------------

Because Server-Sent Events are streams of data, they require long-lived connections. You’ll want to use a server can handle large numbers of simultaneous connections. I strongly recomend you to use some gevent WSGI server.


Contributing
------------

Install `Vagrant <http://www.vagrantup.com/>`_ in order to run the example app and test the code.
