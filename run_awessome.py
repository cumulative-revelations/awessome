# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@author: Amal Htait and Leif Azzopardi
"""


from builder import *
from similarity_measure import *


if __name__ == "__main__":

    avg_builder = SentimentIntensityScorerBuilder('avg','bert-base-nli-mean-tokens')
    max_builder = SentimentIntensityScorerBuilder('max', 'bert-base-nli-mean-tokens')
    vader_scorer = avg_builder.build_scorer_from_prebuilt_lexicon('vader')
    labmt_scorer = max_builder.build_scorer_from_prebuilt_lexicon('labmt')

    sentences = ['I am happy',
                'I am feeling very sad',
                'I cant wait to go to the party',
                'I am not happy',
                 'This is awessome!!']


    for sentence in sentences:
        print(vader_scorer.name, sentence, vader_scorer.score_sentence(sentence))
        print(labmt_scorer.name, sentence, labmt_scorer.score_sentence(sentence))

