#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WordNet class.
# caculate the similarity scores between nouns. 

from nltk.corpus import wordnet as wn

class WordNetScore:
    
    ## calculate the wup_similarity between two words in string using the package from nltk.corpus 
    """
    input format:
        word1: String
        word2: String 
    
    """    
         
    def average_wup_similarity(word1, word2):
        synsets1 = wn.synsets(word1, pos =wn.NOUN)
        synsets2 = wn.synsets(word2, pos =wn.NOUN)
     
        ## input check
        if len(synsets1) == 0:
         #   print('word1 empty synsets')
            return 0
        if len(synsets2) == 0:
          #  print('word2 empty synsets')
            return 0
        
        #calculate average
        avg = 0
        for i in range(len(synsets1)):
            for j in range(len(synsets2)):
                avg += wn.wup_similarity(synsets1[i],synsets2[j])
        avg = avg/ (len(synsets1)* len(synsets2))
        
        return avg
                

## test the wordnet wup similarity calculation
if __name__ == "__main__":
  print("similarity score between words bob and year is" ,WordNetScore.average_wup_similarity('bob','year'))
  print("similarity score between words bob and author is",WordNetScore.average_wup_similarity('bob','author'))
  print("similarity score between words database and area is",WordNetScore.average_wup_similarity('database','area'))
  print("similarity score between words database and area is",WordNetScore.average_wup_similarity('database','author'))
  
  
  
  
  
  
  
  
  
  
  
   
    
    