from unittest.case import TestCase
from 漢羅文本整理 import 轉


class 試驗(TestCase):
    def test_分詞(self):
        句 = '阮｜goan2 過｜ke3  著｜tioh8 孤-孤-單-單｜kou-kou-toann-toann'
        self.assertEqual(len(list(轉()._提出一句(句))), 1)

    def test_分詞對袂濟(self):
        句 = '阮｜goan2 過｜ke3  著｜÷tioh8 孤-孤-單-單｜kou-kou-toann-toann'
        self.assertEqual(len(list(轉()._提出一句(句))), 0)
