from os.path import abspath, dirname, join
from posix import listdir
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.基本物件.組 import 組
from 用字.models import 用字表
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.辭典.型音辭典 import 型音辭典
from 臺灣言語工具.語言模型.KenLM語言模型 import KenLM語言模型
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語工具.語言模型.KenLM語言模型訓練 import KenLM語言模型訓練
from 臺灣言語工具.語言模型.安裝KenLM訓練程式 import 安裝KenLM訓練程式
from tempfile import TemporaryDirectory


class 轉:
    台文資料夾 = join(dirname(abspath(__file__)), '台語文本')
    語言模型資料夾所在 = join(dirname(abspath(__file__)), '語言模型資料夾')
    正規化過的分詞 = [
        'su-lui.分詞.gz',
        'moedict_su.分詞.gz',
        '例句.分詞.gz',
        '陳先生60句.分詞.gz',
        '陳先生提供的語句.分詞.gz',
    ]

    def 全部台語(self):
        全部詞 = set()
        with TemporaryDirectory() as 暫時:
            全部資料暫時所在 = join(暫時, '全部資料.txt')
            with open(全部資料暫時所在, 'w') as 全部資料暫時檔案:
                for 句物件 in self.全部正規化分詞台語():
                    for 詞物件 in 句物件.網出詞物件():
                        全部詞.add(詞物件)

                    print(句物件.看分詞(), file=全部資料暫時檔案)

            語言模型檔 = KenLM語言模型訓練().訓練(
                [全部資料暫時所在], 暫存資料夾=self.語言模型資料夾所在, 連紲詞長度=3
            )
        print(len(全部詞))
        語言模型 = KenLM語言模型(語言模型檔)

        辭典 = 型音辭典(4)
        for 詞物件 in 全部詞:
            辭典.加詞(詞物件)
        for 句物件 in self.其他猶未整理台語():
            標好句物件 = (
                句物件
                .揣詞(拄好長度辭典揣詞, 辭典)
                .揀(語言模型揀集內組, 語言模型)
            )
            for 字物件 in 標好句物件.篩出字物件():
                if 字物件.音 == 無音:
                    字物件.音 = 字物件.型
            yield 標好句物件
        yield from self.全部正規化分詞台語()

    def 其他猶未整理台語(self):
        for 檔案 in sorted(listdir(self.台文資料夾)):
            if 檔案.endswith('.txt.gz'):
                yield from self._txt句(join(self.台文資料夾, 檔案))
            elif 檔案.endswith('.分詞.gz') and 檔案 not in self.正規化過的分詞:
                yield from self._分詞混合(join(self.台文資料夾, 檔案))

    def 全部正規化分詞台語(self):
        for 檔名 in self.全部正規化分詞檔案():
            yield from self._分詞句(檔名)

    def 全部正規化分詞檔案(self):
        for 檔案 in sorted(listdir(self.台文資料夾)):
            if 檔案 in self.正規化過的分詞:
                yield join(self.台文資料夾, 檔案)

    def _txt句(self, 檔名):
        for 一逝 in 程式腳本._讀檔案(檔名):
            句物件 = (
                拆文分析器.建立句物件(
                    文章粗胚.建立物件語句前處理減號(
                        臺灣閩南語羅馬字拼音相容教會羅馬字音標,
                        文章粗胚.數字英文中央全加分字符號(一逝)
                    )
                )
                .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
            )
            yield 句物件

    def _分詞混合(self, 檔名):
        for 一逝 in 程式腳本._讀檔案(檔名):
            yield self._提出一句(一逝)

    def _提出一句(self, 一逝):
        if '｜' not in 一逝:
            return (
                拆文分析器.建立句物件(
                    文章粗胚.建立物件語句前處理減號(
                        臺灣閩南語羅馬字拼音相容教會羅馬字音標,
                        文章粗胚.數字英文中央全加分字符號(一逝)
                    )
                )
                .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
            )

        句物件 = 拆文分析器.分詞句物件(一逝)
        for 字物件 in 句物件.篩出字物件():
            if not 用字表.有這个字無(字物件):
                字物件.型 = 字物件.音
                字物件.音 = 無音
        return 句物件

    def _分詞句(self, 檔名):
        for 一逝 in 程式腳本._讀檔案(檔名):
            yield (
                拆文分析器.分詞句物件(一逝)
                .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
            )


def main():
    安裝KenLM訓練程式().安裝kenlm()
    with open('漢佮羅lm-臺羅無標.txt', 'w') as 輸出:
        for 第幾筆, 句物件 in enumerate(轉().全部台語(), start=1):
            詞陣列 = []
            for 詞物件 in 句物件.網出詞物件():
                for 字物件 in 詞物件.篩出字物件():
                    if 臺灣閩南語羅馬字拼音(字物件.音).音標 is None:
                        break
                else:
                    詞陣列.append(詞物件)
            組物件 = 組(詞陣列)
            print(組物件.看分詞(), file=輸出)
            print(句物件.看分詞())
            print(組物件.看分詞())

            if 第幾筆 % 1000 == 0:
                print('第 {} 筆'.format(第幾筆))


if __name__ == '__main__':
    main()
