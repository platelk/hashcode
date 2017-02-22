"""
Basic testing of the app
"""
import unittest

class TestSimpleCase(unittest.TestCase):
    """
    TestSimpleCase will assert that most simple test work
    """
    def empty_test(self):
        """
        Verify that the Environment working
        """
        self.assertEqual("toto", "toto")

if __name__ == '__main__':
    unittest.main()
