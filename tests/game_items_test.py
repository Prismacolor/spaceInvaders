import unittest


if __name__ == '__main__':

    with open('items_test.log', 'w') as f:
        trunner = unittest.TextTestRunner(f)
        unittest.main(testRunner=trunner)