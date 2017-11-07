import csv
from os.path import abspath, dirname, join
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class 轉:
    nng7tshing1su5 = '/home/ciciw/Dropbox/母語/語料/錄音檔-阿國/阿國-試/聽拍.csv'

    def _台語詞(self):
        with open(self.nng7tshing1su5) as tong2an3:
            for tsua7 in csv.DictReader(tong2an3):
                句物件 = (
                    拆文分析器.建立句物件(
                        文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, tsua7['口語調臺羅'])
                    )
                    .轉音(臺灣閩南語羅馬字拼音)
                    .轉音(臺灣閩南語羅馬字拼音, 函式='轉通用拼音')
                )
                yield tsua7['檔名'], 句物件.看型('-', ' ')


if __name__ == '__main__':
    for 檔名,通用 in 轉()._台語詞():
        print(檔名,通用)
