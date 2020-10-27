# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@author: Amal Htait and Leif Azzopardi
""" 


import scipy 


class Similarity:
    
    def __init__():
        pass
        
    def similarity_value(text_embedding, seeds_embeddings, similarity_measure):
        """
        :param similarity_measure: scipy offers several measures ex: cosine, jaccard, etc
        :param text_embedding: an embedding representation for the text using the language model
        :param seeds_embeddings: a list of embeddings representing the seed words using the language model
        :returns: a similarity(float)
        """
        pass

    
class ScipySimilarity(Similarity):

    def similarity_value(text_embedding, seeds_embeddings, similarity_measure):  
        value = scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, similarity_measure)[0]
               
        return value
