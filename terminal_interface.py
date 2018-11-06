#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:12:00 2018

@author: csking
"""



from NodeMapper import NodeMapper
 


## really simple interface for user to change the mapping


if __name__ == "__main__":
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
                new_change = input("please enter the tuple you want to insert")
                map_result[int(index)] = new_change
                print("mapping after the change: ",map_result)
                q = input("change completed, do you want to quit? (y/n)")
                if q == "y":
                    break 
        if change == "2":
            while True:
                index = input("please select the index of the element you want to remove: ")
                remove_element = map_result[int(index)]
                map_result.remove(remove_element)
                print("mapping after the removal: ",map_result)
                q = input("removal completed, do you want to quit? (y/n)")
                if q == "y":
                    break
                
        if change == "3":
            break 
                
                
                
        
        
        
        
        
        
        
        
        
        
        
        
            
    
    

