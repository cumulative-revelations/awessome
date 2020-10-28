# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""

import operator
import os

from awessome.awessome_aggregator import SumSentimentIntensityAggregator, AvgSentimentIntensityAggregator, \
   MaxSentimentIntensityAggregator
from awessome.awessome_scorer import SentimentIntensityScorer
from awessome.awessome_similarity import CosineSimilarity, EuclideanSimilarity
from sentence_transformers import SentenceTransformer

# Default values
DEFAULT_SEED_SIZE =500
DEFAULT_AGGREGATOR ='avg'
DEFAULT_LEXICON = 'vader'
DEFAULT_LANGUAGE_MODEL = 'bert-base-nli-mean-tokens'
DEFAULT_SIMILARITY_METHOD = 'cosine'
DEFAULT_WEIGHTED = False


class SentimentIntensityScorerBuilder(object):
    """
    Build the sentiment intensity scorer
    """

    def __init__(self, aggregation_method_name, language_model_name, similarity_method_name=DEFAULT_SIMILARITY_METHOD, seed_size=DEFAULT_SEED_SIZE, weighted=DEFAULT_WEIGHTED):
        """

        :param aggregation_method_name: Selected aggregation method : avg, sum or max (default = avg)
        :param language_model_name: Selected pre-trained language model: bert-base-nli-mean-tokens, distilbert-base-nli-stsb-mean-tokens, etc
                (default = bert-base-nli-mean-tokens)
        :param similarity_method_name: Selected similarity method : cosine or euclidean (default = cosine)
        :param seed_size: Selected seeds lists size (default = 500)
        :param weighted: Option of adding weight to aggregated similarity scores in the sentiment (default = False)
        """
        self.aggregator_method_name = aggregation_method_name
        self.language_model_name = language_model_name
        self.similarity_method_name = similarity_method_name
        self.seed_size=seed_size
        self.weighted=weighted
        self.lexicon_name=None
        self.aggregator = self._create_aggregator(aggregation_method_name)
        self.similarity_method = self._create_similarity(similarity_method_name)
        self.language_model  = self._create_language_model(language_model_name)

    def build_scorer_from_lexicon_file(self, lexicon_file):
        """
        Build and return a scorer object built using all the given parameters, including an input lexicon file

        :param lexicon_file:
        :return: Sentiment Intensity Scorer Object
        """
        filename = os.path.basename(lexicon_file)
        lexicon_list, lexicon_dict = self._load_lexicon_from_file(lexicon_file)
        pos_seeds_embeddings, neg_seeds_embeddings = self._make_seed_lists(lexicon_list, self.language_model, self.seed_size)

        scorer = SentimentIntensityScorer(pos_seeds_embeddings=pos_seeds_embeddings, neg_seeds_embeddings=neg_seeds_embeddings,
                                                        aggregator=self.aggregator, language_model_embedder=self.language_model, similarity=self.similarity_method, weighted=self.weighted, lexicon_list=lexicon_list, lexicon_dict=lexicon_dict)

        scorer.name = 'awessome-{}-{}-{}-{}-{}'.format(self.aggregator_method_name, self.language_model_name, self.seed_size, self.similarity_method_name, filename)
        return scorer

    def build_scorer_from_prebuilt_lexicon(self, lexicon):
        """
        Build and return a scorer object built using all the given parameters, using a prebuilt lexicon
        by calling the function: build_scorer_from_lexicon_file

        :param lexicon: the name of a prebuilt lexicon (string)
        :param seed_size: the number of positive and negative seed terms to use given the lexicon
        :return: SentimentIntensityScorer
        """
        self.lexicon_name = lexicon

        lexicons = ['vader',
                          'labmt']

        if lexicon not in lexicons:
            lexicon = DEFAULT_LEXICON

        lexicon_file  =  'lexicon/{}.txt'.format(lexicon)
        #lexicon_file  =  'lexicon/{}.lex'.format(lexicon) => we'll need to change our lexicon files to .lex

        return self.build_scorer_from_lexicon_file(lexicon_file)

    def _load_lexicon_from_file(self, lexicon_file):
        """
        Load the lexicon to be used in the scorer from an input file.

        :param lexicon_file: the name of the file containing seed terms and their
                sentiment intensity score (tab separated file).
        :return: the list of lexicon terms, and a dictionary of terms (key) and SI scores (value).
        """
        lexicon_dict = {}
        seeds = open(lexicon_file, 'r', encoding='utf-8-sig').readlines()
        for i in range(len(seeds)):
            line = seeds[i].split('\t')
            lexicon_dict[line[0].strip()] = line[1].strip()
            lexicon_dict = dict( sorted( lexicon_dict.items(), key=operator.itemgetter(1), reverse=True ) )

        return list(lexicon_dict.keys()), lexicon_dict

    def _create_aggregator(self, aggregation_method):
        """
        Return the aggregation class to use based on an input parameter.

        :param aggregation_method: Aggregation method that can be : avg, sum or max.
        :return: Aggregation class to use.
        """

        aggregators={
            'sum': SumSentimentIntensityAggregator,
            'avg': AvgSentimentIntensityAggregator,
            'max': MaxSentimentIntensityAggregator
         }

        am = aggregation_method.lower()
        if am in aggregators:
              aggregator = aggregators[am]()
        else:
            aggregator=aggregators[DEFAULT_AGGREGATOR]()
            self.aggregator_method_name = DEFAULT_AGGREGATOR

        return aggregator

    def _create_language_model(self, language_model_name):
        """
        Return a created embedder based on an input parameter.

        :param language_model_name: pretrained language model name (ex: bert-base-nli-mean-tokens).
        :return: the embedder created using the language model, 
                   that will be used to create the embedding representation of text.
        """

        models_name = [
            'bert-base-nli-mean-tokens', #fast
            'bert-large-nli-mean-tokens', 
            'bert-base-nli-stsb-mean-tokens', 
            'bert-large-nli-stsb-mean-tokens',
            #'roberta-base-nli-stsb-mean-tokens', #TypeError: __init__() got an unexpected keyword argument 'do_lower_case'
            #'roberta-large-nli-stsb-mean-tokens', #TypeError: __init__() got an unexpected keyword argument 'do_lower_case'
            'distilbert-base-nli-stsb-mean-tokens', # needs GPU
            'xlm-r-100langs-bert-base-nli-stsb-mean-tokens', # needs GPU
            'xlm-r-100langs-bert-base-nli-mean-tokens' # needs GPU
        ]

        if language_model_name in models_name:
            language_model_embedder = SentenceTransformer(language_model_name)
        else:
            language_model_embedder = SentenceTransformer(DEFAULT_LANGUAGE_MODEL)
            self.language_model_name = DEFAULT_LANGUAGE_MODEL

        return language_model_embedder

    def _make_seed_lists(self, lexicon_list, language_model_embedder, seed_size):
        """
        Return two embedding lists representing the seeds lists (positive and negative)

        :param lexicon_list: a lexicon list extracted from the lexicon file (from _create_language_model)
        :param language_model_embedder: embedder created based on the pretrained language model
                (from_create_language_model)
        :param seed_size: size of seeds lists (default = 500)
        :return: Two embedding lists representing the seeds lists
        """

        max_seed_size = len(lexicon_list)/2
        if int(seed_size) > max_seed_size:
            seed_size=max_seed_size

        pos_seeds=lexicon_list[:int(seed_size)]
        neg_seeds=lexicon_list[-int(seed_size):]

        pos_seeds_embeddings=language_model_embedder.encode(pos_seeds)
        neg_seeds_embeddings=language_model_embedder.encode(neg_seeds)

        return pos_seeds_embeddings, neg_seeds_embeddings

    def _create_similarity(self, similarity_method):
        """
        Return the Class to use for the input similarity method

        :param similarity_method: 'cosine','euclidean'
        :return: a Similarity scoring object
        """

        similarity_methods = {
            'cosine': CosineSimilarity,
            'euclidean': EuclideanSimilarity
        }

        sm = similarity_method.lower()
        if sm in similarity_methods:
            sim = similarity_methods[sm]()
        else:
            sim = similarity_methods[DEFAULT_SIMILARITY_METHOD]()
            self.similarity_method_name = DEFAULT_SIMILARITY_METHOD

        return sim




