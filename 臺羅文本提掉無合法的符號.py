from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.基本物件.組 import 組
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.基本物件.公用變數 import 標點符號

if __name__ == '__main__':
    with open('臺語lm-臺羅.txt') as 輸入:
        with open('臺語lm-臺羅無標.txt', 'w') as 輸出:
            for 一逝 in 輸入.readlines():
                詞陣列 = []
                for 詞物件 in 拆文分析器.建立句物件(
                    文章粗胚.數字英文中央全加分字符號(一逝.strip())
                ).轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標).網出詞物件():
                    for 字物件 in 詞物件.篩出字物件():
                        if not 字物件.音標敢著(臺灣閩南語羅馬字拼音) or 字物件.型 in 標點符號:
                            break
                    else:
                        詞陣列.append(詞物件)
                print(組(詞陣列).看型('-', ' '), file=輸出)
