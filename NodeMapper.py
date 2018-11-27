#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:56:06 2018

@author: csking
"""


import nltk
from  WordNetScore import WordNetScore
from tools import helpertools
from JaccordScore import JaccordScore

## the class that maps each word 


class NodeMapper:
    """
    Function that maps the sentence words to SQL components accroding to WUP_similarity score"
    
    input format:
        wordlist: LIST[String]  (list of words that is parsed from the orginal sentence)
        eg:['GET','authors','who','published','in','database','area']
        schema: LIST[String] (list of words that is parsed by the original database schema)
        
    return format: 
        Array[(word,schema)]
        
    """
    
    
    DB_Name = "authorship"
    DB_Attributes = ["author","age","publication","gender","field"]
    
    
    
    def map_node_by_wup_score(wordlist,schema): 
        map_result = []
        for i in range(len(wordlist)):
            sim_score = []
            for j in range(len(schema)):
                score = WordNetScore.average_wup_similarity(wordlist[i],schema[j])
                sim_score.append(score)
            max_index = sim_score.index(max(sim_score))
            map_result.append((wordlist[i],schema[max_index]))
        return map_result
    
    
    """
    Function that input a sentence and returns an array of nouns in that sentence 
    input format:
        wordlist: Array[string]
    
    output format：
        Array[String]
    
    """
    def filter_nouns(wordlist):
        nouns = []
        
        for word,pos in nltk.pos_tag(wordlist):
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)
        
        #is_noun = lambda pos: pos[:2] == 'NN' or pos[:2] == 'NNP'
        #nouns = [word for (word, pos) in nltk.pos_tag(wordlist) if is_noun(pos)]
        
        if 'gender' in wordlist and ('gender' not in nouns):
            nouns.append('gender')
            
        if 'male' in wordlist and (' male' not in nouns):
            nouns.append('male')
      
    
        return nouns
    
        
    
    
    """
    Function that maps the word by keyword in convention
    Input:  array[string]
    Output: (word, node tpye, sql translation)
    
    """
    
    def map_node_by_keyword(wordlist):
       
        mapped_node = []
        res = []
        for i in range(len(wordlist)):
        
            ## ----   selection node ------
            if wordlist[i] == "return" or wordlist[i] == "find" or wordlist[i] == "get":
                res.append((wordlist[i],"SN","SELECT"))  
                mapped_node.append(wordlist[i])
            
            # ------  Operator Node ------
            if wordlist[i] =="equals" or wordlist[i] == "equal" :
            
                res.append((wordlist[i],"ON","="))
                mapped_node.append(wordlist[i])
            if wordlist[i] == "less":
                res.append((wordlist[i],"ON","<"))
                mapped_node.append(wordlist[i])
            if wordlist[i] =="greater":
                 res.append((wordlist[i],"ON",">"))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="not":
                 res.append((wordlist[i],"ON","!="))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="before":
                 res.append((wordlist[i],"ON","<"))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="after":
                 res.append((wordlist[i],"ON",">"))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="more":
                 res.append((wordlist[i],"ON",">"))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="older":
                 res.append((wordlist[i],"ON",">"))
                 mapped_node.append(wordlist[i])
            if wordlist[i] =="newer":
                 res.append((wordlist[i],"ON","<"))
                 mapped_node.append(wordlist[i])
            
            #-------- function node ---------#
            
            if wordlist[i] == "average":
                res.append((wordlist[i],"FN","AVG"))
                mapped_node.append(wordlist[i])
            
            if wordlist[i] == "most":
                res.append((wordlist[i],"FN","MAX"))
                mapped_node.append(wordlist[i])
            
            if wordlist[i] == "total":
                res.append((wordlist[i],"FN","SUM")) 
                mapped_node.append(wordlist[i])
            
            if wordlist[i] == "number":
                res.append((wordlist[i],"FN","COUNT"))
                mapped_node.append(wordlist[i])
            
            # -------- logic node ------------#
            
            if wordlist[i] == "and":
                res.append((wordlist[i],"LN","AND"))
                mapped_node.append(wordlist[i])
            if wordlist[i] == "or":
                res.append((wordlist[i],"LN","OR"))
                mapped_node.append(wordlist[i])
                
            ## -------- value node ---------# 
            
            if helpertools.intTryParse(wordlist[i])[1]:
                res.append((wordlist[i],"VN",wordlist[i]))
                mapped_node.append(wordlist[i])
                
       
        return (res,mapped_node)
    
    
    
    
    '''
    function that takes input as sentence in String format
    Returns the final mapping result. 
    '''
    def get_final_map(sentence):
        parse_sentence = sentence.split(" ")
        keyword_map = NodeMapper.map_node_by_keyword(parse_sentence)
        keyword_map_result = keyword_map[0]
        mapped_index = keyword_map[1]
        
        for i in range(len(mapped_index)):
         
            parse_sentence.remove(mapped_index[i])
        
        without_noun = NodeMapper.filter_nouns(parse_sentence)
        similarity_map = NodeMapper.map_node_by_wup_score(without_noun,NodeMapper.DB_Attributes)
       
        
        ## process the format:
        similarity_result = []
        for i in range(len(similarity_map)):
            item = (similarity_map[i][0],"NN",similarity_map[i][1])
            similarity_result.append(item)
            
        
        ## Double check NN  not a VN:
        
        
        for i in range(len(similarity_result)):
            if similarity_result[i][1] == "NN":
                if JaccordScore.get_jaccordscore(similarity_result[i][0],similarity_result[i][2]) < 0.13:
                    item = (similarity_map[i][0],"VN", similarity_map[i][0])
                    similarity_result[i] = item
                    
        fix_order = NodeMapper.preserve_orginal_order_mapping(sentence,similarity_result + keyword_map_result)
                    
        return fix_order
    
    
    
    def preserve_orginal_order_mapping(sentence,final_map_result):
        
        
        orginal_order_index = []
        sentence_split = sentence.split(" ")
        orginal_order_map = [0 for x in range(len(sentence_split))]
        for i in range(len(final_map_result)):
            orginal_order_index.append(sentence_split.index(final_map_result[i][0]))

        for i in range(len(final_map_result)):
             orginal_order_map[orginal_order_index[i]] = final_map_result[i]
        
        final_result = [x for x in orginal_order_map if x !=0]
    
        return final_result 
    
    
    
    def preserve_orginal_order_mapping2(sentence,final_map_result):
        orginal_order_index = []
        sentence_split = sentence.split(" ")
        orginal_order_map = [0 for x in range(len(sentence_split))]
        for i in range(len(final_map_result)):
            orginal_order_index.append(sentence_split.index(final_map_result[i][0]))

        for i in range(len(final_map_result)):
             orginal_order_map[orginal_order_index[i]] = final_map_result[i]
        
        for i in range(len(sentence_split)):
            if  orginal_order_map[i] == 0:
                orginal_order_map[i] = (sentence_split[i],None,None)
        
        return orginal_order_map
        
    
    
    
        
        
        
        
if __name__ == "__main__":
    #sentence  = ['Get','authors','whose','name','is','BOB','and','published','in','database','area']
    #sentence1 = "Get authors whose name is BOB and published in database area"
    #nouns = NodeMapper.filter_nouns(sentence)
    #schema = ['author','area']
    #print(NodeMapper.map_node_by_wup_score(nouns,schema))
    
    sentence = "get the authors whose name equal to BOB or age is greater than 38"
    
    sentence2 = "Get authors whose name equal to BOB and published in database area"
    
    
    
    sentence4 ="Get the average age of author whose gender equals to male"
  #  s1 = 'get the authors whose name equal to BOB or age is greater than 38'
 #   print("input sentence: ", sentence2)
    print("map results: ", NodeMapper.get_final_map(sentence))
    b = NodeMapper.get_final_map(sentence)
    d = NodeMapper.display_mapping(sentence)
    print(d)
    
    
    
    
    
        
        
        
    