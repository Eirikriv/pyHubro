import sys
sys.path.append("../src/owlbrain")
from owlbrainV1 import *

from unittest import TestCase
from datetime import datetime


class TestOwlbrainScheduler(TestCase):
    def test_OwlbrainScheduler_easy_input01(self):
        assignmentDeadline = '2017-03-16 23:59:59'
        initialHoursSet = 3
        calendarEvents = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00',
                          u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00',
                          u'2017-03-15T08:15:00EB2017-03-15T16:00:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00',
                          u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00',
                          u'2017-03-16T17:15:00EB2017-03-16T19:00:00']

        correctOutput = [['15:00:00', '16:00:00', '2017-03-14'], ['18:00:00', '20:00:00', '2017-03-14']]
        self.assertEqual(OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents), correctOutput)


    def test_OwlbrainScheduler_easy_input02(self):
        assignmentDeadline = datetime.strptime('2017-03-17 23:59:59', '%Y-%m-%d %H:%M:%S')
        initialHoursSet = 3
        calendarEvents = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00',
                          u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00',
                          u'2017-03-15T08:15:00EB2017-03-15T17:15:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00',
                          u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00',
                          u'2017-03-16T17:15:00EB2017-03-16T19:00:00']

        correctOutput = [['17:15:00', '20:00:00', '2017-03-15'], ['15:00:00', '15:15:00', '2017-03-14']]
        self.assertEqual(OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents), correctOutput)