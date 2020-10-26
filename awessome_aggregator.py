# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:36:44 2020
@author: Amal Htait
"""

class SentimentIntensityAggregator:
    def __init__(self):
        pass
    
class SumSentimentIntensityAggregator(SentimentIntensityAggregator):
    def __init__(self):
        pass

    def getScore(self, pos_dists, neg_dists):  
        pos_score=0.0
        neg_score=0.0
        for i in range(len(self.pos_dists)):
            pos_score=pos_score + (1-self.pos_dists[i])
            neg_score=neg_score + (1-self.neg_dists[i])
        score=pos_score - neg_score       
        return score

class AvgSentimentIntensityAggregator(SentimentIntensityAggregator):
    def __init__(self):
        pass

    def getScore(self, pos_dists, neg_dists):   
        pos_sum=0.0
        neg_sum=0.0
        for i in range(len(self.pos_dists)):
            pos_sum=pos_sum + (1-self.pos_dists[i])
            neg_sum=neg_sum + (1-self.neg_dists[i])
        pos_score=sum(pos_sum)/len(self.pos_dists)
        neg_score=sum(neg_score)/len(self.neg_dists)
        score=pos_score - neg_score
        return score

class MaxSentimentIntensityAggregator(SentimentIntensityAggregator):
    def __init__(self):
        pass

    def getScore(self, pos_dists, neg_dists):    
        pos_score=(1-(min(self.pos_dists)))
        neg_score=(1-(min(self.neg_dists)))
        score=pos_score - neg_score
        return score
