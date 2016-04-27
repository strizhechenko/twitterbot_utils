# coding: utf-8
import unittest
from twitterbot_utils import TwiUtils

TEST_STRINGS = (
    'тестовая строка',
    u'тестовая строка',
)


class TestUtils(unittest.TestCase):
    """ Тесты вспомогательных функций """
    @staticmethod
    def test_any_to_unicode():
        """ tweepy.Status, str и unicode должны стать unicode """
        for string in TEST_STRINGS:
            assert TwiUtils.any_to_unicode(string) == u'тестовая строка'

    @staticmethod
    def test_remove_mention():
        mention = u"@botname Алла Пугачёва"
        need = u"Алла Пугачёва"
        assert TwiUtils.remove_mentions(mention) == need
