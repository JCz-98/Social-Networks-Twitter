# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:32:47 2020

@author: erick
"""
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt

filename = "08.05.2020.Midday"

def main():
    
    graph = nx.Graph()
    
    df = pd.read_csv("./dataframes/df_{}.csv".format(filename))
    df_main = df.copy()
    df_main = df_main[df['Type']=='main']
    central_nodes = {}
    
    print(central_nodes)
    
    print(df.head(5))
    
    scoreTotal = 0
    
    scores_main = []

    for row in df.itertuples():
        #print("tuple row: {}".format(row[2]))
        scoreInd = row[3] + row[4]   
        scoreTotal += scoreInd
            
        if row[8] != 'none':
            #G.add_edge(row['tweet_id_string'], row['Next_TweetId'])
            
            end1 = str(row[2])
            end2 = str(row[8])
            
            if not graph.has_node(end1):
                graph.add_node(end1)
            if not graph.has_node(end2):
                graph.add_node(end2)
                
            graph.add_edge(end1, end2)
            
            
        else:
            
            end = str(row[2])
            if not graph.has_node(end):
                graph.add_node(end)
            
            central_nodes[end] = 'main'
            scores_main.append(scoreTotal) 
            
            #nx.draw(G, node_color=range(len(G)), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
            #plt.savefig('./graphs/{}.png'.format(row['tweet_id_string']))
            #plt.clf()
            #plt.close()
            #plt.draw()
            #plt.show()
            
            scoreTotal = 0
            #G.clear()
    
    df_main['Score'] = scores_main
    df_main = df_main.sort_values(by='Score', ascending=False)
    df_main.to_csv("./dataframes_scores/df_score_{}.csv".format(filename), index=False)    
    print(df_main.head(5))
    
    
    #print("node graph: {} dict: {}".format(len(graph), len(labeldic)))
    #print(central_nodes)
    #print(len(central_nodes))
    
    #nx.draw(graph)
    pos = nx.spring_layout(graph, k=0.05)
    
    nx.draw_networkx(graph, pos, node_color=range(len(graph)), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
    #nx.draw_networkx_labels(graph, pos, central_nodes)
    #nx.draw_circular(graph, node_color=range(len(graph)), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
    nx.draw_networkx_nodes(graph, pos=pos, nodelist=central_nodes, node_size=40, node_color='red')
    
    plt.savefig('./graphs_df_complete/graph_{}.png'.format(filename))
    plt.show()
    
if __name__ == "__main__":
    main()