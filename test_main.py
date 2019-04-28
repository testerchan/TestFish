import bot_main
import unittest

class Test_起動(unittest.TestCase):
    def test_起動テスト(self):
        m = bot_main.bot_main()
        m.main()


    

