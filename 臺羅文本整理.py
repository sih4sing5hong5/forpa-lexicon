from os.path import abspath, dirname, join
from posix import listdir
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.基本物件.組 import 組


class 轉:
    台文資料夾 = join(dirname(abspath(__file__)), '台語文本')

    def 全部台語(self):
        for 檔案 in sorted(listdir(self.台文資料夾)):
            if 檔案.endswith('.txt.gz'):
                yield from self._台語句(join(self.台文資料夾, 檔案))
            elif 檔案.endswith('.分詞.gz'):
                yield from self._分詞句(join(self.台文資料夾, 檔案))

    def _台語句(self, 檔名):
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

    def _分詞句(self, 檔名):
        for 一逝 in 程式腳本._讀檔案(檔名):
            句物件 = (
                拆文分析器.分詞句物件(一逝)
                .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
            )
            for 字物件 in 句物件.篩出字物件():
                字物件.型 = 字物件.音
            yield 句物件


def main():
    with open('臺語lm-臺羅無標.txt', 'w') as 輸出:
        with open('臺語lm-通用無標.txt', 'w') as 通用檔案:
            標點符號 = set()
            臺羅 = []
            通用 = []
            for 第幾筆, 句物件 in enumerate(轉().全部台語(), start=1):
                臺羅.append(句物件.看型('-', ' '))
                try:
                    通用.append(句物件.轉音(臺灣閩南語羅馬字拼音, '轉通用拼音').看型('-', ' '))
                except:
                    print(臺羅[-1])
                for 字物件 in 句物件.篩出字物件():
                    if 臺灣閩南語羅馬字拼音(字物件.型).音標 is None:
                        標點符號.add(字物件.型)

                詞陣列 = []
                for 詞物件 in 句物件.網出詞物件():
                    for 字物件 in 詞物件.篩出字物件():
                        if 臺灣閩南語羅馬字拼音(字物件.型).音標 is None:
                            break
                    else:
                        詞陣列.append(詞物件)
                組物件 = 組(詞陣列)
                try:
                    print(組物件.看型('-', ' '), file=輸出)
                    print(
                        組物件.轉音(臺灣閩南語羅馬字拼音, '轉通用拼音')
                        .看型('-', ' ')
                        .replace('or', 'er'),
                        file=通用檔案
                    )
                except IndexError:
                    print(組物件)

                if 第幾筆 % 1000 == 0:
                    print('第 {} 筆'.format(第幾筆))

            程式腳本._陣列寫入檔案('臺語lm-臺羅.txt', 臺羅)
            程式腳本._陣列寫入檔案('臺語lm-通用.txt', 通用)
            程式腳本._陣列寫入檔案('臺語lm-標點符號.txt', 標點符號)


if __name__ == '__main__':
    main()
