import csv
from os.path import abspath, dirname, join
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語.通用拼音音標 import 通用拼音音標


class 轉:
    台華有對應 = join(dirname(abspath(__file__)), '台語', '台華有對應{}.csv')
    台華無對著 = join(dirname(abspath(__file__)), '台語', '台華無對著.csv')

    def 全部台語詞(self):
        yield from self._台語詞()
        yield from self._台語詞無對著()

    def _台語詞(self):
        for 編號 in range(1, 5):
            with open(self.台華有對應.format(編號)) as tong2an3:
                頭一逝 = True
                for tsua7 in csv.reader(tong2an3):
                    if 頭一逝:
                        頭一逝 = False
                        continue
                    try:
                        愛 = (tsua7[4].strip() == '')
                    except IndexError:
                        愛 = True
                    if 愛:
                        句物件 = (
                            拆文分析器.建立句物件(
                                文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, tsua7[1])
                                .replace('0', '-0')
                            )
                            .轉音(臺灣閩南語羅馬字拼音)
                            .轉音(臺灣閩南語羅馬字拼音, 函式='轉通用拼音')
                        )
                        yield 句物件, tsua7[3],

    def _台語詞無對著(self):
        with open(self.台華無對著) as tong2an3:
            頭一逝 = True
            for tsua7 in csv.reader(tong2an3):
                if 頭一逝:
                    頭一逝 = False
                    continue
                try:
                    愛 = (tsua7[3].strip() == '')
                except IndexError:
                    愛 = True
                if 愛:
                    句物件 = (
                        拆文分析器.建立句物件(
                            文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, tsua7[1])
                            .replace('0', '-0')
                        )
                        .轉音(臺灣閩南語羅馬字拼音)
                        .轉音(臺灣閩南語羅馬字拼音, 函式='轉通用拼音')
                    )
                    for 華語 in tsua7[4:]:
                        if 華語.strip():
                            yield 句物件, 華語,


if __name__ == '__main__':
    with open('lexicon.txt', 'w') as lexicon:
        for 通用, 華語 in 轉().全部台語詞():
            資料 = []
            for 字物件 in 通用.篩出字物件():
                音標 = 通用拼音音標(字物件.型)
                資料.append(音標.聲)
                資料.append(音標.韻)
            print('{}    {}'.format(華語, ' '.join(資料)), file=lexicon)
