import utility
import unittest

class Test_get_last_word_of_urlが最後の単語を返すか(unittest.TestCase):
    u = utility.utility()

    def test_スラッシュアリの場合に最後の単語を返すか(self):
        actual = self.u.get_last_ward_of_url('http://testerchan.hatenadiary.com/entry/2019/04/18/070634/')
        expected = '070634'
        self.assertEqual(expected, actual)

    def test_スラッシュなしの場合に最後の単語を返すか(self):
        actual = self.u.get_last_ward_of_url('http://testerchan.hatenadiary.com/entry/2019/04/18/070634')
        expected = '070634'
        self.assertEqual(expected, actual)
        
    def test_ドメインの場合に最後の単語を返すか(self):
        actual = self.u.get_last_ward_of_url('http://testerchan.hatenadiary.com')
        expected = 'testerchan.hatenadiary.com'
        self.assertEqual(expected, actual)