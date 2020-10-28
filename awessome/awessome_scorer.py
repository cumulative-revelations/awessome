# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""


class SentimentIntensityScorer(object):

    def __init__(self, pos_seeds_embeddings, neg_seeds_embeddings, aggregator,  language_model_embedder, similarity, weighted, lexicon_list, lexicon_dict):
        """

        :param pos_seeds_embeddings:
        :param neg_seeds_embeddings:
        :param aggregator: expects an aggregation object from awessome.aggegrator
        :param language_model_embedder:
        :param similarity: expects a similarity object from awessome.similarity_measure
        :param weighted: is a boolean, if True we use a dictionary of terms as weights to modify the similarity between 
        """
        self.pos_seeds_embeddings = pos_seeds_embeddings
        self.neg_seeds_embeddings = neg_seeds_embeddings
        self.aggregator = aggregator
        self.similarity = similarity
        self.language_model_embedder = language_model_embedder
        self.weighted = weighted
        self.lexicon_list = lexicon_list
        self.lexicon_dict = lexicon_dict
        self.name = 'awessome'

    def score_sentence(self, text):
        text = self.split_long_sentence(text)
        text_embedding = self.language_model_embedder.encode(text)

        distances_pos = self.similarity.score(text_embedding, self.pos_seeds_embeddings)
        distances_neg = self.similarity.score(text_embedding, self.neg_seeds_embeddings)

        if self.weighted:
            distances_pos, distances_neg = self.add_weight(distances_pos, distances_neg)

        score = self.aggregator.agg_score(distances_pos, distances_neg)

        return score

    def score_list(self, sentence_list):
        score_dict = {}
        for i in range(len(sentence_list)):
            score = self.score_sentence(sentence_list[i])
            score_dict[sentence_list[i]] = score

        return score_dict

    def split_long_sentence(self, text):
        max_length = 256
        separator = ' '
        text_length = len(text.split())

        if text_length > max_length:
            text_list = text.split()[:max_length]
            text = separator.join(text_list)

        return text 

    def add_weight(self, distances_pos, distances_neg):
        distances_pos_w = []
        distances_neg_w = [] 

        for i in range(len(distances_pos)):
            distances_pos_w.append(distances_pos[i] * float(self.lexicon_dict[self.lexicon_list[i]]))
            distances_neg_w.append(distances_neg[i] * float(self.lexicon_dict[self.lexicon_list[i]]))

        return distances_pos_w, distances_neg_w

