import sys
sys.path.append("../src/owlbrain")
from owlbrainV1 import *

from unittest import TestCase


class TestOwlbrainScheduler(TestCase):
    def test_OwlbrainScheduler_easy_input01(self):
        assignmentDeadline = '2017-03-17 23:59:59'
        initialHoursSet = 3
        calendarEvents = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00',
                          u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00',
                          u'2017-03-15T08:15:00EB2017-03-15T16:00:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00',
                          u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00',
                          u'2017-03-16T17:15:00EB2017-03-16T19:00:00']
        daysPriorToDeadline = 5

        correctOutput = [['15:00:00', '16:00:00', '2017-03-14'], ['18:00:00', '20:00:00', '2017-03-14']]
        self.assertEqual(OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents, daysPriorToDeadline), correctOutput)


    def test_OwlbrainScheduler_easy_input02(self):
        assignmentDeadline = '2017-03-17 23:59:59'
        initialHoursSet = 3
        calendarEvents = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00',
                          u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00',
                          u'2017-03-15T08:15:00EB2017-03-15T17:15:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00',
                          u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00',
                          u'2017-03-16T17:15:00EB2017-03-16T19:00:00']
        daysPriorToDeadline = 5

        correctOutput = [['15:00:00', '16:00:00', '2017-03-14'], ['18:00:00', '20:00:00', '2017-03-14']]
        self.assertEqual(OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents, daysPriorToDeadline), correctOutput)

    def test_OwlbrainScheduler_double_posting_input01(self):
        assignmentDeadline = '2017-06-16 17:00:00'
        initialHoursSet = 4
        calendarEvents = [u'2017-06-12T08:15:00EB2017-06-12T10:00:00', u'2017-06-12T10:15:00EB2017-06-12T12:00:00',
                          u'2017-06-12T12:00:00EB2017-06-12T14:00:00', u'2017-06-12T14:30:00EB2017-06-12T15:45:00',
                          u'2017-06-12T17:15:00EB2017-06-12T19:00:00', u'2017-06-13T08:15:00EB2017-06-13T10:00:00',
                          u'2017-06-13T10:30:00EB2017-06-13T13:00:00', u'2017-06-13T13:30:00EB2017-06-13T15:30:00',
                          u'2017-06-13T16:15:00EB2017-06-13T18:00:00', u'2017-06-13T18:00:00EB2017-06-13T20:00:00',
                          u'2017-06-14T08:30:00EB2017-06-14T10:15:00', u'2017-06-14T13:00:00EB2017-06-14T14:30:00',
                          u'2017-06-15T12:15:00EB2017-06-15T15:00:00']
        daysPriorToDeadline = 4

        correctOutput = [['10:15:00', '12:45:00', '2017-06-14'], ['14:30:00', '16:00:00', '2017-06-14']]
        self.assertEqual(OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents, daysPriorToDeadline), correctOutput)