#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 22:47:22 2018

@author: csking
"""

from NodeMapper import NodeMapper
import math
import itertools

### class that generates SQL statements from the mapping verified by the user. 




class SQLgenerator:
  
    """
    Start from evaluating the format NN_ON_VN
    
    input: map results after user edit
    output: possible NN_ON_VN format where NN is the attribute node, ON is the operator node and VN is the value node
    
    """
    
    
    
 
    def group_NN_ON_VN(map_result):
        
        ## Rule  NN ON VN 
        perm_NN_ON_VN =[]
        NN_ON_VN = [ x[2] for x in map_result if x[1] == "VN" or x[1] =="NN" or x[1] =="ON" ]
        perm = itertools.permutations(NN_ON_VN ,3)
        for item in list(perm):
            if SQLgenerator.check_node_type(item[0],map_result) == "NN" and SQLgenerator.check_node_type(item[1],map_result) == "ON" and SQLgenerator.check_node_type(item[2],map_result) =="VN":
                perm_NN_ON_VN.append(item)   
        
        return perm_NN_ON_VN
            
    """
    connect  NN_ON_VN to generate a list of valid sql statements.
    
    """
    
    
    
    def connect_NN_ON_VN(perm_NN_ON_VN):
        sql = []
        for i in range(len(perm_NN_ON_VN)):
            sql_string = ""
            for j in range(len(perm_NN_ON_VN[0])):
                sql_string += perm_NN_ON_VN[i][j] + " "
        
            sql.append(sql_string)
        return sql
    
   
    
    
    
    """
    Based on the input of possible NN_ON_VN format, choose the valid ones based on mapping results and the operators.
    
    input possible NN_ON_VN formats, the map result
    
    output valid NN_ON_VN results that can be used to connect by operator
    
    """
            
    
    def select_valid_LN(perm_NN_ON_VN,map_result):
        valid = []
        key_words = [ x[2] for x in map_result ]
        n = len([x for x in map_result if x[1] == "LN"])
        selection_c = 2*n
        perm = list(itertools.permutations(perm_NN_ON_VN,selection_c))
        for item in perm:
            key_words_c = key_words.copy()
            boolean = True
            for j in range(len(item)):
                
                if item[j][0] not in key_words_c:
                    boolean = False
                if item[j][1] not in key_words_c:
                    boolean = False
                if item[j][2] not in key_words_c:
                    boolean = False
                if item[j][0] in key_words_c:
                    key_words_c.remove(item[j][0])
                if item[j][1] in key_words_c:
                    key_words_c.remove(item[j][1])
                if item[j][2] in key_words_c:
                    key_words_c.remove(item[j][2])
            if boolean == True:
                valid.append(item)
        return valid
                
    
    """
    connect the NN_ON_VN format based on the operators
    
    input valid NN_ON_VN format
    
    output:  the sql strings in the format  (NN ON VN) LN (NN ON VN)
    
    """
    
    
   
    def connect_LN(valid_LN,map_result):
        sql = []    
        logic = [x[2] for x in map_result if x[1] == "LN"]

        for i in range(len(valid_LN)):
            n = len([x for x in map_result if x[1] == "LN"])
            sql_string = ""
            for j in range(len(valid_LN[0])):
                for m in range(len(valid_LN[0][0])):
                    sql_string +=  valid_LN[i][j][m] + " "
                while n > 0:
                    sql_string += logic[n-1] + " "
                    n = n - 1
            sql.append(sql_string)
        return sql
        
    
    
    """
    Hepler function that returns the type of the node
    
    """
                    
        
    def check_node_type(sql_word,map_result):
        for i in range(len(map_result)):
            if map_result[i][2] == sql_word:
                return map_result[i][1]
            
        
        
    
    """
    evaluate the LN connection based on the score
    
    returns a list of scores of each (NN ON VN) LN (NN ON VN) node 
    

    """
    
    def assign_connect_ln_score(valid_ln_string, map_result, sentence):
        sql_scores = []
        
        for i in range(len(valid_ln_string)):
            score = SQLgenerator.calculate_single_score(valid_ln_string[i],map_result,sentence)
            sql_scores.append([valid_ln_string[i],score])
        
        print(sql_scores)
        return sql_scores
            
            
        
         
    """
    
    healper fucntion that checks if word1 is before word2 in the orginal sentence
    return true if word1 is before word2

    """       
    def is_before(sentence,word1,word2):
        sentence_split = sentence.split(" ")
        for i in range(len(sentence_split)):
            if sentence_split.index(word1) < sentence_split.index(word2):
                return True
        
        return False
    
    
    
    
    
    """
    Score function: evaluating an SQL statements by comparing the matching order between the orginal sentence
    and the generated ln_sql results. 

    """        
    
    def calculate_single_score(ln_sql,map_results,sentence):
        dic = {}
        score = 0 
        for i in range(len(map_results)):
            dic[map_results[i][2]] = map_results[i][0]
         
        ln_sql_split = ln_sql.split(' ')
        ln_sql_split =ln_sql_split[:-1]
        for i in range(len(ln_sql_split)):
            for j in range(i,len(ln_sql_split)):
                if i == j:
                    continue
                if SQLgenerator.is_before(sentence,dic[ln_sql_split[i]], dic[ln_sql_split[j]]):
                    score += 1
        return score
                    
    
    
    """
    score function: evaluating an SQL statements by calculating the distance of  a and and b in "a ON b"
    
    """
    
    
    def calculate_distance_score(ln_sql,map_results,sentence):
        dic ={}
        
        for i in range(len(map_results)):
            dic[map_results[i][2]] = map_results[i][0]
        ln_sql_split = ln_sql.split(' ')
        ln_sql_split =ln_sql_split[:-1]
        sentence = sentence.split(" ")
        
        score = abs(sentence.index(ln_sql_split[0]) - sentence.index(ln_sql_split[2]))
        
        return score
    
    
    def assign_distance_score(valid_ln_string, map_result, sentence):
        sql_scores = []
        
        for i in range(len(valid_ln_string)):
            score = SQLgenerator.calculate_distance_score(valid_ln_string[i],map_result,sentence)
            sql_scores.append([valid_ln_string[i],score])
        
        return sql_scores
            
            
        
    
    
    
    """
    1. Generation of the final sql once we decide the (NN ON VN) LN (NN ON VN) in WHERE CLAUSE 
    2. Decide the NN attributes after select by finding a nearest NN node in the orginal sentence
    
    """
    
    def generate_final_sql(sentence,map_results):
        
        selection_NN = SQLgenerator.get_selection_NN(sentence,map_results)
        new_map_results = selection_NN[1]
      #  print(new_map_results)
        NN_ON_VN = SQLgenerator.group_NN_ON_VN(new_map_results)
        print(NN_ON_VN)
        
        bool_ln_mode = "LN" in [ x[1] for x in map_results ]
        aggregate_mode = "FN" in [ x[1] for x in map_results ]
        
        
        #aggregate_mode
        if aggregate_mode:
            if not bool_ln_mode:

                aggregate_notation = [  x[2] for x in map_results if x[1] == 'FN' ]
                component = aggregate_notation[0] + "(" +  selection_NN[0][2] + ")"
                sql_list = SQLgenerator.connect_NN_ON_VN(NN_ON_VN)
                score_list = SQLgenerator.assign_distance_score(sql_list,new_map_results,sentence)  
                where = SQLgenerator.get_lowest_score(score_list)
                sql = "SELECT " + component + " FROM " + NodeMapper.DB_Name + " WHERE " + where + ";"
                return sql
            
            
            if bool_ln_mode:
                LN = SQLgenerator.select_valid_LN(NN_ON_VN , new_map_results)
                if len(LN) == 0:
                    print("Mapping selection is incorrect")
                    return
                connect_ln = SQLgenerator.connect_LN(LN, new_map_results)
                score_list = SQLgenerator.assign_connect_ln_score(connect_ln, new_map_results,sentence)
                where = SQLgenerator.get_highest_score(score_list)
                aggregate_notation = [  x[2] for x in map_results if x[1] == 'FN' ]
                component = aggregate_notation[0] + "(" +  selection_NN[0][2] + ")"
                sql = "SELECT " + component + " FROM " + NodeMapper.DB_Name + " WHERE " + where + ";"
                return sql
                
        
            
          # start logic operator mode
        if bool_ln_mode:
            LN = SQLgenerator.select_valid_LN(NN_ON_VN , new_map_results)
            if len(LN) == 0:
                print("Mapping selection is incorrect")
                return
            connect_ln = SQLgenerator.connect_LN(LN, new_map_results)
            score_list = SQLgenerator.assign_connect_ln_score(connect_ln, new_map_results,sentence)
            where = SQLgenerator.get_highest_score(score_list)
            sql = "SELECT " + selection_NN[0][2] + " FROM " + NodeMapper.DB_Name + " WHERE " + where + ";"
            return sql
        
        # start the mode without logic operator
        
        if not bool_ln_mode:
            sql_list = SQLgenerator.connect_NN_ON_VN(NN_ON_VN)
            sql = "SELECT " + selection_NN[0][2] + " FROM " + NodeMapper.DB_Name + " WHERE " + sql_list[0] + ";"
            return sql
            
        
    
        
        
    """
    helper function to Decide the NN attributes after select by finding a nearest NN node in the orginal sentence
    
    """
    
            
    def get_selection_NN(sentence,map_results):
      
        sentence_split = sentence.split(" ")
        
        NN_Node = [x for x in map_results if x[1] == "NN"]
        
        node = []
        min_index = math.inf
        for i in range(len(NN_Node)):
            index = sentence_split.index(NN_Node[i][0])
            if index < min_index:
                 node = NN_Node[i]
                 min_index = index
        
        map_results.remove(node)
        return (node,map_results) 
                 
                
    """
    helper function to Decide the highest order score for a score list of NN ON VN) LN (NN ON VN)
    
    """
                
            
    def get_highest_score(score_list):
        score = 0
        node = []
        for i in range(len(score_list)):
            if score_list[i][1] > score:
                score = score_list[i][1]
                node = score_list[i][0]
        
        return node
    
    '''
    helper function to decide the lowest distance score
    '''
    def get_lowest_score(score_list):
        score = 99999
        node = []
        for i in range(len(score_list)):
            if score_list[i][1] < score:
                score = score_list[i][1]
                node = score_list[i][0]
        
        return node
    
                
            


if __name__ == "__main__":
    demo_sentence1 = "get the authors whose name equal to BOB or age is greater than 38"
    demo_sentnece2= "get the age of author whose name is equal to BOB and gender equals to male" 
   
   
  #  map_result = NodeMapper.get_final_map(sentence)
   # map_result2 = NodeMapper.get_final_map(sentence2)
  #  print(map_result)
  #  print(map_result)
   
    
   
    map3 = [('age', 'NN', 'age'), ('author', 'NN', 'author'), ('get', 'SN', 'SELECT'), ('equal', 'ON', '='),('BOB', 'VN', 'BOB')]
    map_result_after_user_edit = [('authors', 'NN', 'author'),('BOB', 'VN', 'BOB'), ('age', 'NN', 'age'), ('get', 'SN', 'SELECT'), ('or', 'LN', 'OR'), ('greater', 'ON', '>'), ('38', 'VN', '38'),('equal', 'ON', '=') ,('name', 'NN', 'author'),('average','FN','AVG')]
    map_result_after_user_edit2 = [('authors', 'NN', 'author'),('BOB', 'VN', 'BOB'),  ('get', 'SN', 'SELECT'), ('equal', 'ON', '=') ,('name', 'NN', 'author')]   
    map_demo2 = [('age', 'NN', 'age'), ('author', 'NN', 'author'), ('BOB', 'VN', 'BOB'), ('gender', 'NN', 'gender'), ('get', 'SN', 'SELECT'), ('equal', 'ON', '='), ('and', 'LN', 'AND'), ('equals', 'ON', '=')]
  
  
    
    '''                 ln_operator_mode DEMO                       '''
    print("ln_operator_mode Demon: ")
    ln_operator_sentence = "get the authors whose name equals to BOB or age is greater than 38"
    print("input sentence :",ln_operator_sentence)
    ln_map_result = NodeMapper.get_final_map(ln_operator_sentence)
    print("---------------result_after_mapping----------------------- ")
    print(ln_map_result)
    print("---------------result_after_user_edit----------------------")
    ln_map_after_user_edit = [('authors', 'NN', 'author'),('BOB', 'VN', 'BOB'), ('age', 'NN', 'age'), ('get', 'SN', 'SELECT'), ('or', 'LN', 'OR'), ('greater', 'ON', '>'), ('38', 'VN', '38'),('equals', 'ON', '=') ,('name', 'NN', 'author')]
    print(ln_map_after_user_edit)
    print("---------------Final SQL-----------------------------------")
    print(SQLgenerator.generate_final_sql(ln_operator_sentence, ln_map_after_user_edit))
    
    
    
    print()
    print()
    print()
    
        
    '''                  aggregate_mode  DEMO                   ''' 
    print("aggregate_mode DEMO: ")
    aggregate_sentence = "get the average age of author whose gender equals to male"
    print("input sentence :", aggregate_sentence)
    aggregate_map_result = NodeMapper.get_final_map(aggregate_sentence)
    print("---------------result_after_mapping----------------------- ")
    print(aggregate_map_result)
    print("---------------Final SQL-----------------------------------")
    print(SQLgenerator.generate_final_sql(aggregate_sentence, aggregate_map_result))
  
    
    
    
    
    #a = "author = male "
    #b = "gender = male "
    #m = SQLgenerator.calculate_distance_score(a,aggregate_map_result,aggregate_sentence)
    #print(m)
    
    
    
  
  
    
    
    
#    a = SQLgenerator.generate_final_sql( demo_sentence1, map_result_after_user_edit)
 #   print(a)
   # print(a)
 #   print(a)
  
    
    
    
    
    
    
    
    
    