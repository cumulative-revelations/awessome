# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@author: Amal Htait and Leif Azzopardi
""" 


import scipy 


class Similarity(object):
    
    def __init__(self):
        pass
        
    def score(self, text_embedding, seeds_embeddings):
        """
        :param text_embedding: an embedding representation for the text using the language model
        :param seeds_embeddings: a list of embeddings representing the seed words using the language model
        :returns: a similarity(float)
        """
        return 0.0

    
class CosineSimilarity(Similarity):

    def score(self, text_embedding, seeds_embeddings):
        sim_score = scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, 'cosine')[0]
               
        return sim_score



class EuclideanSimilarity(Similarity):
    def score(self, text_embedding, seeds_embeddings):
        sim_score = scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, 'euclidean')[0]

        return sim_score