#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 22:47:22 2018

@author: csking
"""

from NodeMapper import NodeMapper

### class that generates SQL statements from the mapping verified by the user. 




class SQLgenerator:
    '''
    Rules:
        1. The leftside of an ON Node should be an NN node
        2. The rightside of an ON node should be an VN node
        3. The first word should be an SN node
        4. The sql word after "FROM" should be an NN node
        5. The left and right side of an LN node should consist of 2 ON nodes
        6. If no ON nodes, there should not be a "WHERE" in generaged SQL
        
        
    Sample SQL: SELECT author FROM authorship WHERE  author = "BOB" and age > 38
    '''
    
        
    def Check_Valid_SQL(sql,map_result):
        return



    '''
    Given an valid generated SQL, a score is assigned to this SQL by compare:
        1. the order of word in orginal sentence
        2.
    
    
    '''

    def Score(sql,map_result,sentence):
        return
        
        
    
    
    def sql_random_generation(map_result):
        return
    
    
    def sql_valid_generation():
        return 
        



if __name__ == "__main__":
    sentence = "get the authors whose name equal to BOB and age is greater than 38"
    map_result = print("map results: ", NodeMapper.get_final_map(sentence))
    map_result_after_user_edit = [('authors', 'NN', 'author'), ('BOB', 'VN', 'author'), ('age', 'NN', 'age'), ('get', 'SN', 'SELECT'), ('and', 'LN', 'AND'), ('greater', 'ON', '>'), ('38', 'VN', '38')]
    
    
    
    
    
    
    
    
    