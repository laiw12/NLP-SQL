#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:12:00 2018

@author: csking
"""



from NodeMapper import NodeMapper
from SQLgenerator import SQLgenerator 
 


## really simple interface for user to change the mapping


if __name__ == "__main__":
    
    
    while True:
        sentence = input("please enter your query in natural language: ")
        map_result = NodeMapper.get_final_map(sentence)
        print("The following information is your map result: ")
        print(map_result)
        
        
        while True:
            print("Please select one of the following: ")
            print("1. I want to change my mapping results. ")
            print("2. I want remove one or more mapping results. ")
            print("3. The mapping is perfect, go ahead and generate possible SQL queries. ")
            change = input("Please enter your selection: (1,2 or 3)")
            
            
            if change == "1":
                while True:
                    index = input("please select the index of the element you want to change: ")
                    del map_result[int(index)]
                    word_in_sentence = input("please enter the word in the sentence you want to change: ")
                    word_node_type = input("please enter the node type for this word: ")
                    word_map_result = input("please enter the mapping result for this word: ")
                    
                    map_result.append((word_in_sentence , word_node_type , word_map_result))
                 
                    print("mapping after the change: ",map_result)
                    q = input("change completed, do you want to quit? (y/n)")
                    if q == "y":
                        break 
            
            if change == "2":
                while True:
                    index = input("please select the index of the element you want to remove: ")
                    del map_result[int(index)]
                    print("mapping after the removal: ")
                    print("map result: ", map_result)
                    q = input("removal completed, do you want to quit? (y/n)")
                    if q == "y":
                        break
                
            if change == "3":
                 break
        sql_result = SQLgenerator.generate_final_sql(sentence,map_result)
        ("The best sql best on the map result is the following: ")
        
        if len(sql_result) !=0:
            print(sql_result)
        
   
    
             
                
                
                
        
        
        
        
        
        
        
        
        
        
        
        
            
    
    

