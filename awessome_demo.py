# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""

from awessome.awessome_builder import *

if __name__ == "__main__":

    avg_builder = SentimentIntensityScorerBuilder('avg','bert-base-nli-mean-tokens','euclidean','100',True)
    max_builder = SentimentIntensityScorerBuilder('max', 'bert-base-nli-mean-tokens')
    vader_avg_scorer = avg_builder.build_scorer_from_prebuilt_lexicon('vader')
    labmt_avg_scorer = avg_builder.build_scorer_from_prebuilt_lexicon('labmt')
    vader_max_scorer = max_builder.build_scorer_from_prebuilt_lexicon('vader')
    labmt_max_scorer = max_builder.build_scorer_from_prebuilt_lexicon('labmt')

    sentences = ['I am happy',
                'I am very happy',
                'I am not happy',
                'I am feeling very sad',
                'I cant wait to go to the party',
                'This is awessome!!',
                'This is awesome!!',
                'This is awesome',
                'lol',
                ':-)']

    for sentence in sentences:
        print(sentence)
        print(vader_avg_scorer.name, vader_avg_scorer.score_sentence(sentence))
        print(labmt_avg_scorer.name, labmt_avg_scorer.score_sentence(sentence))
        print(vader_max_scorer.name, vader_max_scorer.score_sentence(sentence))
        print(labmt_max_scorer.name, labmt_max_scorer.score_sentence(sentence))
        print('------------------------------------------------------------------------')
