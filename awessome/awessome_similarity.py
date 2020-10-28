# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""

import scipy 


class Similarity(object):
    """
    Apply a similarity measure between a text embedding and seeds lists embeddings: cosine or  euclidean.
    """
    def __init__(self):
        pass
        
    def score(self, text_embedding, seeds_embeddings):
        """
        Return the similarity distance between embeddings using scipy.

        :param text_embedding: an embedding representation for the text using the language model.
        :param seeds_embeddings: a list of embeddings representing the seed words using the language model
        :returns: a similarity (float)
        """
        return 0.0

    
class CosineSimilarity(Similarity):
    """
    Apply a cosine similarity measure between a text embedding and seeds lists embeddings.
    """
    def score(self, text_embedding, seeds_embeddings):
        sim_score = scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, 'cosine')[0]
               
        return sim_score


class EuclideanSimilarity(Similarity):
    """
    Apply a euclidean similarity measure between a text embedding and seeds lists embeddings.
    """
    def score(self, text_embedding, seeds_embeddings):
        sim_score = scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, 'euclidean')[0]

        return sim_score
