# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:20:20 2020
@authors: Amal Htait and Leif Azzopardi
For license information, see LICENSE.TXT
"""

from awessome.awessome_builder import *

if __name__ == "__main__":

    avg_builder = SentimentIntensityScorerBuilder('avg','bert-base-nli-mean-tokens')
    max_builder = SentimentIntensityScorerBuilder('avg', 'bert-base-nli-mean-tokens')
    vader_scorer = avg_builder.build_scorer_from_prebuilt_lexicon('vader')
    labmt_scorer = avg_builder.build_scorer_from_prebuilt_lexicon('labmt')

    sentences = ['I am happy',
                'I am feeling very sad',
                'I cant wait to go to the party',
                'I am not happy',
                 'This is awessome!!',
                 'This is awesome!!',
                 'This is awesome',
                 'lol',
                 ':-)']

    for sentence in sentences:
        print(vader_scorer.name, sentence, vader_scorer.score_sentence(sentence))
        print(labmt_scorer.name, sentence, labmt_scorer.score_sentence(sentence))

