# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""


class SentimentIntensityAggregator:
    """
    Apply an aggregation to a list of similarity scores.
    """

    def __init__(self):
        pass

    def agg_score(self, pos_dists, neg_dists):
        """
        Return a float as a score of aggregated similarity scores with positive and negative seeds lists.

        :param pos_dists: a list of similarity scores with pos seeds
        :param neg_dists: a list of similarity scores with neg seeds
        :return: a score (float)
        """
        pass


class SumSentimentIntensityAggregator(SentimentIntensityAggregator):
    """
    Apply an sum aggregation to a list of similarity scores.
    """
    def agg_score(self, pos_dists, neg_dists):
        pos_score=0.0
        neg_score=0.0
        dists_size = len(pos_dists)
        for i in range(dists_size):
            pos_score=pos_score + (1.0-pos_dists[i])
            neg_score=neg_score + (1.0-neg_dists[i])
        score=pos_score - neg_score
               
        return score


class AvgSentimentIntensityAggregator(SentimentIntensityAggregator):
    """
    Apply an average aggregation to a list of similarity scores.
    """
    def agg_score(self, pos_dists, neg_dists):
        pos_sum = 0.0
        neg_sum = 0.0
        dists_size = len(pos_dists)
        for i in range(dists_size):
            pos_sum = pos_sum + (1.0-pos_dists[i])
            neg_sum = neg_sum + (1.0-neg_dists[i])
        pos_score = pos_sum/dists_size
        neg_score = neg_sum/dists_size
        score = pos_score - neg_score
        
        return score
        

class MaxSentimentIntensityAggregator(SentimentIntensityAggregator):
    """
    Selecting the maximum value in a list of similarity scores.
    """
    def agg_score(self, pos_dists, neg_dists):
        pos_score = (1.0-(min(pos_dists)))
        neg_score = (1.0-(min(neg_dists)))
        score = pos_score - neg_score
        
        return score
