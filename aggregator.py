# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@author: Amal Htait and Leif Azzopardi
"""

class SentimentIntensityAggregator:
    
    def __init__():
       pass
    
        
    def agg_score(pos_dists, neg_dists):
        """
        pos_dists: a list of scores for pos terms
        neg_dists: a list of scores for neg terms
        returns: a score(float)
        """
        pass

    
class SumSentimentIntensityAggregator(SentimentIntensityAggregator):

    def agg_score(pos_dists, neg_dists):  
        pos_score=0.0
        neg_score=0.0
        dists_size = len(pos_dists.tolist())
        for i in range(dists_size):
            pos_score=pos_score + (1-pos_dists[i])
            neg_score=neg_score + (1-neg_dists[i])
        score=pos_score - neg_score
               
        return score


class AvgSentimentIntensityAggregator(SentimentIntensityAggregator):

    def agg_score(pos_dists, neg_dists):   
        pos_sum=0.0
        neg_sum=0.0
        dists_size = len(pos_dists.tolist())
        for i in range(dists_size):
            pos_sum=pos_sum + (1-pos_dists[i])
            neg_sum=neg_sum + (1-neg_dists[i])
        pos_score=pos_sum/dists_size
        neg_score=neg_sum/dists_size
        score=pos_score - neg_score
        
        return score
        

class MaxSentimentIntensityAggregator(SentimentIntensityAggregator):

    def agg_score(pos_dists, neg_dists):    
        pos_score=(1-(min(pos_dists)))
        neg_score=(1-(min(neg_dists)))
        score=pos_score - neg_score
        
        return score