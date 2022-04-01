#!/usr/bin/env python
# coding: utf-8
from typing import Counter
import pandas as pd
import sys
import numpy as np

# Simple metric for help in calculating disagreements 
def nominal_metric(x, y):
    return 1 if x != y else 0

# Get filename from command line
filename = sys.argv[1]

# Reading the annotaions csv
annotations = pd.read_csv(filename) 

# Converting the read dataframe to a format suitable for calculating Krippendorff's alpha
original_table = pd.DataFrame.melt(annotations, id_vars=['tweet_ID'], value_vars=['annotator_1', 'annotator_2', 'annotator_3'],
                                   var_name='annotator_ID', value_name='annotation')
s_df = original_table.pivot_table(index = 'annotator_ID', columns = 'tweet_ID', values = 'annotation', aggfunc = 'first')

# Calculating the number of annotations for each class by each annotator 
a = s_df.T.sort_index(axis = 1).sort_index()
td = {}
for exp, row in a.iterrows():
    vals = row.dropna().values
    td[exp] = Counter()
    for val in vals:
      td[exp][val] += 1

t_df = pd.DataFrame.from_dict(td, orient="index")

# Masking of missing values is not required as we know that each experiment was annotated by atleast two annotators
t_df_sorted = t_df.T.sort_index(axis = 0).sort_index(axis = 1).fillna(0) 
f_dict = dict(
        unit_freqs=t_df_sorted.sum().to_dict(),
        class_freqs=t_df_sorted.sum(1).to_dict(),
        total=t_df_sorted.sum().sum(),
    )

# Calculating expected disagreement by chance 
de = 0
class_frequencies = f_dict['class_freqs']
class_names = list(class_frequencies.keys())

for i,c in enumerate(class_names):
  for k in class_names:
    de += class_frequencies[c] * class_frequencies[k] * nominal_metric(c, k)

# Calculating observed disagreement
do = 0
unit_freqs = f_dict["unit_freqs"]
unit_names = list(unit_freqs.keys())
for name in unit_names:
  unit_classes = list(t_df_sorted[name].keys())
  if unit_freqs[name] < 2:
    pass
  else:
    weight = 1 / (unit_freqs[name] - 1)
    for i, c in enumerate(unit_classes):
      for k in unit_classes:
        do += (t_df_sorted[name][c] * t_df_sorted[name][k] * weight * nominal_metric(c, k))

# Total number of annotations
total = f_dict['total']

# Calculating Krippendorff's alpha
alpha = 1 - (do/de) * (total - 1)

# Calculating pairwise agreement (or) percentage agreement 
conditions = [annotations['annotator_1'] == annotations['annotator_2'], annotations['annotator_2'] == annotations['annotator_3'],
              annotations['annotator_1'] == annotations['annotator_3']]

choices = [1, 1, 1]

annotations['agreement'] = np.select(conditions, choices, default=0)
percent_agreement = np.sum(annotations['agreement'])/150 

print('{:.2f}'.format(alpha) +'\t' + '{:.0%}'.format(percent_agreement))
