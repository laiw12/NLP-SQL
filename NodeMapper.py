#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:56:06 2018

@author: csking
"""


import nltk
from  WordNetScore import WordNetScore

## the class that maps each word 


class NodeMapper:
    
    
    
    """
    Function that maps the sentence words to SQL components accroding to WUP_similarity score"
    
    input format:
        wordlist: LIST[String]  (list of words that is parsed from the orginal sentence)
        eg:['GET','authors','who','published','in','database','area']
        schema: LIST[String] (list of words that is parsed by the original database schema)
        
    """
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
    
    
    
    
    
    def filter_nouns(lines):
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(lines)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        return nouns
        
        
        
    
    
    
    
            

if __name__ == "__main__":
    sentence  = "Get authors whose name is BOB and published in database area" 
    nouns = NodeMapper.filter_nouns(sentence)
    print()
    schema = ['author','area']
    print(NodeMapper.map_node_by_wup_score(nouns,schema))
        
        
        
    