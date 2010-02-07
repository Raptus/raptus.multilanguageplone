import unittest
import doctest

from Testing import ZopeTestCase
from zope.testing import doctestunit
from zope.component import testing, eventtesting

from collective.testcaselayer import ptc as ptc_tcl
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import ptc

from raptus.multilanguageplone.tests import base

class InstallLayer(ptc_tcl.BasePTCLayer):
    """Install raptus.multilanguageplone"""

    def afterSetUp(self):
        ZopeTestCase.installPackage('raptus.multilanguageplone')
        self.addProfile('raptus.multilanguageplone:default')

install_layer = InstallLayer([ptc_tcl.ptc_layer])

def test_suite():
    suite = unittest.TestSuite()

    suite.addTest(
        ztc.FunctionalDocFileSuite(
            'README.txt', 
            package='raptus.multilanguageplone',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        )
    )

    install_suite = ztc.FunctionalDocFileSuite(
        'install.txt',
        'browser.txt',
        test_class=ptc.PloneTestCase)
    install_suite.layer = install_layer
    suite.addTest(install_suite)

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
