import csv
from os.path import abspath, dirname, join


class 轉:
    nng7tshing1su5 = join(dirname(abspath(__file__)), '台語', '台語2000詞.csv')

    def _台語詞(self):
        with open(self.nng7tshing1su5) as tong2an3:
            for tsua7 in csv.DictReader(tong2an3):
                yield tsua7['漢字'],tsua7['臺羅']
                
if __name__=='__main__':
    轉()._台語詞()
