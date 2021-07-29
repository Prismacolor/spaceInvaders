import unittest


class StartMenu(unittest.TestCase):
    def test_startup(self):
        events = ['pygame.MOUSEBUTTONDOWN', 'pygame.MOUSEBUTTONDOWN', 'pygame.QUIT']
        run = True
        counter = 0

        while run:
            print('game is running')

            for event in events:
                if event == 'pygame.QUIT':
                    run = False
                if event == 'pygame.MOUSEBUTTONDOWN':
                    print('Game continues.')
                    counter += 1

        self.assertEqual(counter, 2)
        self.assertEqual(run, False)


if __name__ == '__main__':

    with open('items_test.log', 'w') as f:
        trunner = unittest.TextTestRunner(f)
        unittest.main(testRunner=trunner)