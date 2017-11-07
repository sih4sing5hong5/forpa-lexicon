import csv
import json
from os.path import abspath, dirname, join


class 轉:
    nng7tshing1su5 = '/home/ciciw/git/ami_dict_crawler/data/bnn.json'

    def _台語詞(self):
        ww = set()
        ss = set()
        with open(self.nng7tshing1su5) as tong2an3:
            for tsua7 in json.load(tong2an3):
                ww.add(tsua7['name'].strip('1234567890').lower())
                for ee in tsua7['examples']:
                    if (
                        ee['sentence'] is not None and '詞' not in ee['sentence']
                        and '：' not in ee['sentence']
                        
                        ):
                        for eew in (
                            ee['sentence']
                            .replace(',', ' ')
                            .replace('.', ' ')
                            .replace('?', ' ')
                            .replace('!', ' ')
                            .replace('“', ' ')
                            .split()
                        ):
                            ss.add(eew.lower())
        tsha=ss-ww
        print(len(tsha),len(ss),len(ww))
        print(sorted(tsha)[:100])
        print(sorted(ss)[:100])
        print(sorted(ww)[:100])
        print(sorted(tsha)[-100:])


if __name__ == '__main__':
    轉()._台語詞()
