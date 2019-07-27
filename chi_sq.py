# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 17:12:14 2018

@author: payam.bagheri
"""

# This code takes in categorical data and calculates Chi-sqauerd statistic for each pair of variables

import pandas as pd
from os import path
import tqdm

dir_path = path.dirname(path.dirname(path.abspath(__file__)))
print(dir_path)


data = pd.read_csv(dir_path + '/0_input_data/chi_data.csv')
data.head()

chi2tab = pd.read_csv(dir_path + '/0_input_data/chi2_table.csv')

cols = list(data.columns)
cols.remove('weights')

cols_df = []
for i in cols:
    cols_df.append(i)
    cols_df.append(i+'_90perc_thr')
    cols_df.append(i+'_95perc_thr')
        

results_weighted = pd.DataFrame(index = cols, columns = cols_df)
results_weighted.columns

c=0
for a in tqdm.tqdm(cols):
    for b in cols:
        c+=1
        #print(c)
        #print(a,b)
        au = list(data[a].unique())
        au = sorted([x for x in au if str(x) != 'nan'])
        #print(au)
        bu = list(data[b].unique())
        bu = sorted([x for x in bu if str(x) != 'nan'])
        df = (len(au)-1)*(len(bu)-1)
        #print(df)
        #print(bu)
                
        #a_count = [sum(data['weights'][data[a] == i]) for i in au]
        #a_perc = [x/sum(a_count) for x in a_count]
        #print('a_count is, ', a_count)
        #print('a_perc is, ', a_perc)
        
        ab = []
        
        for i in bu:
            for j in au:
              ab.append(sum(data['weights'][data[a] == j][data[b] == i]))
        
        #print('ab is, ', ab)
        
        for_a = []
        for i in au:
            for j in bu:
              for_a.append(sum(data['weights'][data[a] == i][data[b] == j]))
              
        #print('for_a is, ', for_a)
        
        a_count = [sum(for_a[(x+1)*len(bu)-len(bu):(x+1)*len(bu)]) for x in range(len(au))]
        a_perc = [x/sum(a_count) for x in a_count]
        #print('a_count is 2, ', a_count)
        #print('a_perc is 2, ', a_perc)
        
        sums = [sum(ab[(x+1)*len(au)-len(au):(x+1)*len(au)]) for x in range(len(bu))]
        sums_rep = [x for x in sums for i in range(len(au))]
        #print('sums_rep is, ', sums_rep)        
        a_perc_rep = [x for i in range(len(bu)) for x in a_perc ]
        mult = [x*y for (x,y) in zip(sums_rep,a_perc_rep)]
        #print('mult is, ', mult)
        chi_sq = sum([(x-y)**2/y for (x,y) in zip(ab,mult)])
        #print(chi_sq)
        thr90 = a+'_90perc_thr'
        thr95 = a+'_95perc_thr'
        results_weighted[a].loc[b] = chi_sq
        if chi_sq >= float(chi2tab['p0.1'][chi2tab['df'] == df]):
            results_weighted[thr90].loc[b] = "significant_90perc"
        else:
            results_weighted[thr90].loc[b] = "non-significant_90perc"
        
        if chi_sq >= float(chi2tab['p0.05'][chi2tab['df'] == df]):
            results_weighted[thr95].loc[b] = "significant_95perc"
        else:
            results_weighted[thr95].loc[b] = "non-significant_95perc"
        
results_weighted.to_csv(dir_path + '/0_output/chi_sq_weighted.csv')

#float(chi2tab['p0.1'][chi2tab['df'] == 1])

'''
results = pd.DataFrame(index = cols, columns = cols_df)

c=0
for a in cols:
    for b in cols:
        c+=1
        print(c)
        #print(a,b)
        au = sorted(list(data[a].unique()))
        bu = sorted(list(data[b].unique()))
        #print(au)
        #print(bu)
        
        a_count = [data[a][data[a] == i].count() for i in au]
        a_perc = a_count/sum(a_count)
        #print(a_perc)
        
        ab = []
        
        for i in bu:
            for j in au:
              ab.append(data[data[a] == j][data[b] == i].shape[0])
              
        #print(ab)
        
        sums = [sum(ab[(x+1)*len(au)-len(au):(x+1)*len(au)]) for x in range(len(bu))]
        #print(sums)
        sums_rep = [x for x in sums for i in range(len(au))]   
        #print(sums_rep)
        a_perc_rep = [x for i in range(len(bu)) for x in a_perc ]
        #print(a_perc_rep)
        mult = [x*y for (x,y) in zip(sums_rep,a_perc_rep)]
        #print(mult)
        chi_sq = sum([(x-y)**2/y for (x,y) in zip(ab,mult)])
        #print(chi_sq)
        thr90 = a+'_90perc_thr'
        thr95 = a+'_95perc_thr'
        results[a].loc[b] = chi_sq
        if chi_sq >= float(chi2tab['p0.1'][chi2tab['df'] == df]):
            results[thr90].loc[b] = "significant_90perc"
        else:
            results[thr90].loc[b] = "non-significant_90perc"
        
        if chi_sq >= float(chi2tab['p0.05'][chi2tab['df'] == df]):
            results[thr95].loc[b] = "significant_95perc"
        else:
            results[thr95].loc[b] = "non-significant_95perc"
        
results.to_csv(dir_path + '/0_output/chi_sq.csv')

'''


