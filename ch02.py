# !/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
# import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import timeit

start = timeit.timeit()

path = "ch02/usagov_bitly_data2012-03-16-1331923249.txt"

# print(path)

# records = []

# with open(path) as f:
#     records.append(json.loads(f.readline()))

# 掌握此列表推导式写法
records = [json.loads(line) for line in open(path)]

# print(records[0]['tz'])

time_zones = [rec['tz'] for rec in records if 'tz' in rec]


# print(time_zones[:10])

def get_counts1(seq):
    counts = {}
    for x in seq:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def get_counts2(seq):
    counts = defaultdict(int)  # 记住标准库的支持
    for x in seq:
        counts[x] += 1
    return counts


def top_counts(cnt_dic, n=10):
    value_key_pairs = [(count, tz) for tz, count in cnt_dic.items()]
    value_key_pairs.sort()
    # value_key_pairs.reverse()
    return value_key_pairs[-n:]


my_counts = get_counts2(time_zones)
my_counts_std = Counter(time_zones)

top_cnt = top_counts(my_counts)

# print(top_cnt)
# print(my_counts_std.most_common(10))

frame = DataFrame(records)
# tz_counts = frame['tz'].value_counts()
clean_tz = frame['tz'].fillna('Missing')  # 填充空白
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

# print(tz_counts[:10])
tz_counts[:10].plot(kind='barh', rot=0)  # 不使用IPython，在Pycharm中单步走可显示图像，直接运行太短暂看不到

rlt = Series([x.split()[0] for x in frame.a.dropna()])
# print(rlt[:5])
# print(rlt.value_counts()[:8])

cframe = frame[frame.a.notnull()]
operating_sys = np.where(cframe['a'].str.contains('Windows'), 'Wdinows', 'Not Windows')
# print(operating_sys[:5])

by_tz_os = cframe.groupby(['tz', operating_sys])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

indexer = agg_counts.sum(1).argsort()
print(indexer[:10])

count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)

end = timeit.timeit()
print("It takes ", end - start, "second(s)")
