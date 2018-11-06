#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:02:44 2018

@author: csking
"""


import nltk

class helpertools:
    
    """
    Helper function to see if the string value can be parsed into integers
    return: Boolean 
    """
    
    def intTryParse(value):
        try:
            return int(value), True
        
        except ValueError:
            return value, False
        
 