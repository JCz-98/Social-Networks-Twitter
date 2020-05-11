# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:26:07 2020

@author: erick
"""

import pandas as pd

files = ["07.05.2020.Night","08.05.2020.Midday","08.05.2020.Afternoon","08.05.2020.Night","08.05.2020.LateNight", "09.05.2020.Morning", "09.05.2020.LateNight"]

rate = 1.50

def main():
    
    for file in files:
        df_scores = pd.read_csv("./dataframes_scores/df_score_{}.csv".format(file))
        
        dic = {}
        for row in df_scores.itertuples():
            
            #print(type(row[2]))
            #print(type(row[3]))
            #print(type(row[8]))
            
            inScore = (row[3] + row[4]) * rate
            #print("{}->{}".format(inScore, row[9]))
            if row[9] > inScore and row[9] > 100:
                if not row[2] in dic:
                    dic[row[2]] = []
                    
                dic[row[2]].append(row)
            elif row[2] in dic:
                dic[row[2]].append(row)
        
        #print(dic)
        data_tuples = []
        
        for key, values in dic.items():
            
            for tpl in values:
                data_tuples.append(tpl[1:])
        
        sorted(data_tuples, key= lambda tup: (tup[8]))
        
        df_filtered = pd.DataFrame(data_tuples, columns = df_scores.columns)
        
        df_unique = df_filtered.drop_duplicates("tweet_id_string")
        
        df_unique.to_csv("./tweets_filtered/unique/df_twt_flt_{}.csv".format(file), index=False)
        df_filtered.to_csv("./tweets_filtered/all/df_twt_flt_{}.csv".format(file), index=False)
        
    

if __name__ == "__main__":
    main()