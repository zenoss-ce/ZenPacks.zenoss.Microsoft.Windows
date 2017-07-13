#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import Globals
from mock import Mock, sentinel
import pprint

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.Microsoft.Windows.datasources.EventLogDataSource import EventLogPlugin
from ZenPacks.zenoss.Microsoft.Windows.tests.utils import load_pickle_file

EXPECTED = {
    'component': u'Microsoft-Windows-Winlogon',
    'computername': u'SQLSRV02.solutions-dev.local',
    'device': 'machine',
    'eventClassKey': u'Microsoft-Windows-Winlogon_6000',
    'eventGroup': sentinel.eventlog,
    'eventidentifier': u'6000',
    'message': u'The winlogon notification subscriber <AUInstallAgent> was unavailable to handle a notification event.',
    'ntevid': u'6000',
    'originaltime': u'07/13/2017 14:19:50',
    'severity': 2,
    'summary': u'The winlogon notification subscriber <AUInstallAgent> was unavailable to handle a notification event',
    'user': u''}


class TestDataSourcePlugin(BaseTestCase):
    def test_onSuccess(self):
        plugin = EventLogPlugin()

        results = load_pickle_file(self, 'EventLogPlugin_onSuccess_092940')[0]
        res = plugin.onSuccess(results, Mock(
            id="machine",
            datasources=[Mock(params={'eventlog': sentinel.eventlog},
                              datasource='DataSource')],
        ))

        self.assertEquals(len(res['events']), 5, msg='Received {}'.format(pprint.pformat(res)))
        self.assertEquals(res['events'][0], EXPECTED)
        self.assertEquals(res['events'][2]['summary'], 'Windows EventLog: No PowerShell errors during event collection')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDataSourcePlugin))
    return suite


if __name__ == "__main__":
    from zope.testrunner.runner import Runner
    runner = Runner(found_suites=[test_suite()])
    runner.run()
