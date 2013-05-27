# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from sse_wrapper.views import EventStreamView


urlpatterns = patterns(
    '',

    # index page.
    url(r'^$', TemplateView.as_view(
        template_name='example/index.html'), name='index'),

    # sample views that sends events in the channel course-state.
    url(r'^start-course/(?P<course_id>\d+)/$',
        'example.views.start_course', name='start_course'),
    url(r'^stop-course/(?P<course_id>\d+)/$',
        'example.views.stop_course', name='stop_course'),
    url(r'^course-state/(?P<course_id>\d+)/$',
        'example.views.course_state', name='course_state'),

    # event stream - course-state.
    url(r'^course-state-stream/(?P<channel_extension>[\w]+)/$',
        EventStreamView.as_view(channel='course-state'),
        name='course_state_stream'),
)
