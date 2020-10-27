# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@author: Amal Htait and Leif Azzopardi
"""


import scipy
from sentence_transformers import SentenceTransformer
import operator
from aggregator import SumSentimentIntensityAggregator, AvgSentimentIntensityAggregator, MaxSentimentIntensityAggregator
from scorer import SentimentIntensityScorer


DEFAULT_SEED_SIZE =600
DEFAULT_AGGREGATOR ='avg'
DEFAULT_LEXICON = 'vader'
DEFAULT_LANGUAGE_MODEL = 'bert-base-nli-mean-tokens'

class SentimentIntensityScorerBuilder:

   def __init__(self, aggregation_method, language_model_name):
      self.aggregator = self._create_aggregator(aggregation_method)
      self.language_model  = self._create_language_model(language_model_name)


   def build_from_lexicon_file(self, lexicon_file, seed_size=DEFAULT_SEED_SIZE):
       scorer = None

       lexicon_list, lexicon_dict = self._load_lexicon_from_file(lexicon_file)
       pos_seeds_embeddings, neg_seeds_embeddings = self._make_seed_lists(lexicon_list, self.language_model)
       scorer = SentimentIntensityScorer(pos_seeds_embeddings, neg_seeds_embeddings, self.aggregator, self.language_model, self.weighted)

       return scorer


   def build_from_prebuilt_lexicon(self, lexicon, seed_size=DEFAULT_SEED_SIZE):
      """
      :param lexicon: the name of a prebuilt lexicon (string)
      :param seed_size: the number of positive and negative seed terms to use given the lexicon
      :return: SentimentIntensityScorer
      """

      lexicons = ['vader',
                  'labmt']

      if lexicon not in lexicons:
         lexicon = DEFAULT_LEXICON

      lexicon_file  =  'lexicon/{}.lex'.format(lexicon)

      return self.build_from_lexicon_file(lexicon_file, seed_size)


   def _load_lexicon_from_file(lexicon_file):
      """
      :param lexicon_file: the name of the file containing seed terms and their sentiment intensity score (tab separated file)
      :return: the list of lexicon terms, and a dictionary of terms (key) and SI scores (value)
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

      :param aggregation_method:
      :return:
      """

      aggregators={
         'sum': SumSentimentIntensityAggregator,
         'avg': AvgSentimentIntensityAggregator,
         'max': MaxSentimentIntensityAggregator
        }

      am = aggregation_method.lower()
      if am in aggregators:
         aggregator = aggregators[am]
      else:
         aggregator=aggregators[DEFAULT_AGGREGATOR]

      return aggregator


   def _create_language_model(self, language_model_name):
      """

      :param language_model_name:
      :return:
      """

      models_name = [
         'bert-base-nli-mean-tokens',
         'bert-large-nli-mean-tokens',
         'bert-base-nli-stsb-mean-tokens',
         'bert-large-nli-stsb-mean-tokens',
         'roberta-base-nli-stsb-mean-tokens',
         'roberta-large-nli-stsb-mean-tokens',
         'distilbert-base-nli-stsb-mean-tokens',
         'xlm-r-100langs-bert-base-nli-stsb-mean-tokens',
         'xlm-r-100langs-bert-base-nli-mean-tokens'
      ]

      if language_model_name in models_name:
         language_model = SentenceTransformer(language_model_name)
      else:
         language_model = SentenceTransformer('bert-base-nli-mean-tokens')

      return language_model


   def _make_seed_lists(self, lexicon_list, language_model, seed_size):
      """

      :param lexicon_list:
      :param language_model:
      :param seed_size:
      :return:
      """

      max_seed_size = len(lexicon_list)/2
      if seed_size > max_seed_size:
         seed_size=max_seed_size

      pos_seeds=lexicon_list[:int(seed_size)]
      neg_seeds=lexicon_list[-int(seed_size):]

      pos_seeds_embeddings=language_model.encode(pos_seeds)
      neg_seeds_embeddings=language_model.encode(neg_seeds)

      return pos_seeds_embeddings, neg_seeds_embeddings





