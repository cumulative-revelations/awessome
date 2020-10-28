# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""


class SentimentIntensityScorer(object):
    """
    Give a sentiment intensity score to sentences.
    """

    def __init__(self, pos_seeds_embeddings, neg_seeds_embeddings, aggregator,  language_model_embedder, similarity, weighted, lexicon_list, lexicon_dict):
        """

        :param pos_seeds_embeddings: The word embedding representation of positive seed words from awessome.awessome_builder
        :param neg_seeds_embeddings: The word embedding representation of negative seed words from awessome.awessome_builder
        :param aggregator: expects an aggregation object from awessome.awessome_aggregator
        :param language_model_embedder: The embedder created based on pre-trained model, provided by awessome.awessome_builder
        :param similarity: expects a similarity object from awessome.awessome_similarity
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
        """
        Return the sentiment strength of the input text.
        Positive values are positive scores, negative value are negative
        scores.

        :param text: The sentence to predict its sentiment intensity
        :return: a float for sentiment strength
        """
        text = self.split_long_sentence(text)
        text_embedding = self.language_model_embedder.encode(text)

        distances_pos = self.similarity.score(text_embedding, self.pos_seeds_embeddings)
        distances_neg = self.similarity.score(text_embedding, self.neg_seeds_embeddings)

        if self.weighted:
            distances_pos, distances_neg = self.add_weight(distances_pos, distances_neg)

        score = self.aggregator.agg_score(distances_pos, distances_neg)

        return score

    def score_list(self, sentence_list):
        """
        Return the sentiment strength of the input list of sentences.

        :param sentence_list: The list of sentences to predict their sentiment intensity.
        :return: a dictionary of sentence and sentiment strength (float)
        """
        score_dict = {}
        for i in range(len(sentence_list)):
            score = self.score_sentence(sentence_list[i])
            score_dict[sentence_list[i]] = score

        return score_dict

    def split_long_sentence(self, text):
        """
        Limit the input text to 256 only,
        due to pre-trained language models input limitation

        :param text: The sentence to predict its sentiment intensity
        :return: new shorter text
        """
        max_length = 256
        separator = ' '
        text_length = len(text.split())

        if text_length > max_length:
            text_list = text.split()[:max_length]
            text = separator.join(text_list)

        return text 

    def add_weight(self, distances_pos, distances_neg):
        """
        Add a weight value to the distance similarity score between the sentence and the seeds lists.

        :param distances_pos: The distance similarity score between the sentence and the positive seeds lists, via awessome.awessome_similarity.
        :param distances_neg: The distance similarity score between the sentence and the negative seeds lists, via awessome.awessome_similarity.
        :return: New distance similarity scores with weight application.
        """
        distances_pos_w = []
        distances_neg_w = [] 

        for i in range(len(distances_pos)):
            distances_pos_w.append(distances_pos[i] * float(self.lexicon_dict[self.lexicon_list[i]]))
            distances_neg_w.append(distances_neg[i] * float(self.lexicon_dict[self.lexicon_list[i]]))

        return distances_pos_w, distances_neg_w

