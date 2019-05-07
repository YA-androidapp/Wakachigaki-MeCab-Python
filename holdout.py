#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.


from glob import glob
import datetime
import os
import random


scrpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrpath)

input_dirname = 'input'
log_file = 'log_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

# 訓練データ、検証データ、テストデータをこのディレクトリに出力
output_dirname = 'holdout'

output_train_suffix    = 'train.txt'    # 訓練データ
output_validate_suffix = 'validate.txt' # 検証データ
output_test_suffix     = 'test.txt'     # テストデータ

# 訓練データ、検証データ、テストデータに振り分ける割合(和が1でなくてもよい)
ratio_train = 0.06
ratio_validate = 0.02
ratio_test = 0.02


def main():
    if not os.path.exists(os.path.join(scrpath, output_dirname)):
        os.mkdir(os.path.join(scrpath, output_dirname))
    else:
        nowstr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        os.rename(os.path.join(scrpath, output_dirname), os.path.join(
            scrpath, output_dirname + '_' + nowstr + '.bak'))
        os.mkdir(os.path.join(scrpath, output_dirname))

    files = glob(os.path.join(scrpath, input_dirname, '*.txt'))
    count_originalfile = 0
    with open(os.path.join(scrpath, output_dirname, log_file), 'a', encoding="utf-8") as fo:
        for file in files:
            print(
                '  {:.2%} {}\n'.format(
                    (count_originalfile/len(files)),
                    os.path.basename(file)
                    ), end='', file=fo)
            if os.path.isfile(file):
                count_line = 0
                with open(file, encoding="utf-8") as fi:
                    line = fi.readline().rstrip('\r\n')
                    while line:
                        print(
                            '  {:.2%} {} {} {}\n'.format(
                                (count_originalfile/len(files)),
                                count_line,
                                datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                                str(line)
                                ), end='', file=fo)

                        if random.random() <= ratio_train:
                            with open(os.path.join(scrpath, output_dirname, os.path.basename(file) + '.' + output_train_suffix), 'a', encoding="utf-8") as ftrain:
                                print(line, end='', file=ftrain)
                        elif random.random() <= ratio_train + ratio_validate:
                            with open(os.path.join(scrpath, output_dirname, os.path.basename(file) + '.' + output_validate_suffix), 'a', encoding="utf-8") as fvalidate:
                                print(line, end='', file=fvalidate)
                        elif random.random() <= ratio_train + ratio_validate + ratio_test:
                            with open(os.path.join(scrpath, output_dirname, os.path.basename(file) + '.' + output_test_suffix), 'a', encoding="utf-8") as ftest:
                                print(line, end='', file=ftest)
                        else:
                            pass
                        line = fi.readline()
                        count_line += 1
            count_originalfile += 1



if __name__ == '__main__':
    main()

