import bot_selenium
import unittest

class Test_seleniumの起動確認(unittest.TestCase):
    def test_起動確認(self):
        b = bot_selenium.BotSelenium()
        expected = "http://milk0824.sakura.ne.jp/doukana/"
        b.run_chrome(expected, False)
        actual = b.current_url()
        self.assertEqual(expected, actual)
        b.close()


    

