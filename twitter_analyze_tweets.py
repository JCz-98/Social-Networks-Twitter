# -*- coding: utf-8 -*-
"""
Created on Sat May  9 16:24:32 2020

@author: erick
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

import os

import twitter_backtracking_news

files = twitter_backtracking_news.files
#files = ["07.05.2020.Night"]

def main():
    
    for file in files:
        df_unique = pd.read_csv("./tweets_filtered/unique/df_twt_flt_{}.csv".format(file))
        df_all = pd.read_csv("./tweets_filtered/all/df_twt_flt_{}.csv".format(file))
        
        
        for row in df_unique.itertuples():
            
            G = nx.DiGraph()
            
            df_indv = df_all.copy()
            df_indv = df_indv[df_indv["tweet_id_string"] == row[2]]
            
            #central_node = str(row[2])
            
            df_all_data = pd.read_csv("./dataframes/df_{}.csv".format(file))
            
            print(df_indv.head(10))
            print("Edges:")
            
            for row in df_indv.itertuples():
                
                for i in range(row[1], -1, -1):
                    
                    if df_all_data.iat[i,6] == 'main':
                        
                        if i != row[1]:
                            break
                        elif i == row[1]:
                            if not G.has_node(str(df_all_data.iat[i, 1])):
                                G.add_node(str(df_all_data.iat[i, 1]))
                    
                    else:
                        print("{} -> {}".format(df_all_data.iat[i, 1], df_all_data.iat[i,7]))
                        
                        if not G.has_node(str(df_all_data.iat[i, 1])):
                            G.add_node(str(df_all_data.iat[i, 1]))
                        
                        if not G.has_node(str(df_all_data.iat[i,7])):
                            G.add_node(str(df_all_data.iat[i,7]))
                            
                        G.add_edge(str(df_all_data.iat[i, 1]), str(df_all_data.iat[i,7]))
            
            nx.draw_networkx(G, node_color=range(len(G)), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
            #nx.draw(G, with_labels = False)
            #nx.draw(G, pos=pos, node_color=range(len(G)), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
            
            try:
            # Create target Directory
                os.mkdir("./graphs_df_study/{}".format(file))
                print("Directory " , file ,  " Created ") 
            except FileExistsError:
                print("Directory " , file ,  " already exists")
                
            plt.savefig('./graphs_df_study/{}/{}_{}.png'.format(file, row[2], file))
            plt.show()
            plt.clf()
            plt.close()
            
            G.clear()
                    


if __name__ == "__main__":
    main()