# -*- coding: utf-8 -*-
from django.http import HttpResponse

from sse_wrapper.events import send_event


def start_course(request, course_id):
    send_event('state', 'started', 'course-state/%s' % course_id)
    return HttpResponse('Course started!')


def stop_course(request, course_id):
    send_event('state', 'stopped', 'course-state/%s' % course_id)
    return HttpResponse('Course stopped!')


def course_state(request, course_id):
    # this would bring the info from database, for example.
    return HttpResponse('stopped')
