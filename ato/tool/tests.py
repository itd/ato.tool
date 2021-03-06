import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import ato.tool

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['ato.tool'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              ato.tool)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='ato.tool',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='ato.tool.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='ato.tool',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for ATOEvent
        ztc.ZopeDocFileSuite(
            'ReviewEvent.txt',
            package='ato.tool',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ComplianceControl
        ztc.ZopeDocFileSuite(
            'ComplianceControl.txt',
            package='ato.tool',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ComplianceFamily
        ztc.ZopeDocFileSuite(
            'ComplianceFamily.txt',
            package='ato.tool',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ComplianceTracker
        ztc.ZopeDocFileSuite(
            'ComplianceTracker.txt',
            package='ato.tool',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
