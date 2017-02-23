"""
Basic testing of the app
"""
import unittest


class TestSimpleCase(unittest.TestCase):
    """
    TestSimpleCase will assert that most simple test work
    """
    def test_empty(self):
        """
        Verify that the Environment working
        """
        print("Basic test")
        self.assertEqual("toto", "toto")
