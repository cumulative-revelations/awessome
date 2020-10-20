# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:36:44 2020
@author: Amal Htait
"""

import scipy
from sentence_transformers import SentenceTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from nltk.stem.snowball import SnowballStemmer
import nltk
from nltk.corpus import words
import operator

class SentimentIntensityScore(object):

    def __init__(self, lexicon_file, seed_size, aggregation_method, model_language):

        self.clean_lexicon_list=[]
        seeds = open("lexicon/"+lexicon_file+".txt", "r", encoding='utf-8-sig').readlines()
        for i in range(len(seeds)):
            line = seeds[i].split('\t')
            self.clean_lexicon_list.append(line[0].strip())

        self.seed_size = seed_size       
        self.aggregation_method = aggregation_method
        self.model_language = model_language

    '''
    # get Vader lexicon from source
        if lexicon_file.lower() == "vader":
            vader_obj = SentimentIntensityAnalyzer() 
            print("Get Lexicon")
            self.lexicon_dict = vader_obj.lexicon
            print("Clean Lexicon")
            self.clean_lexicon_dict, self.clean_lexicon_list = self.clean_lexicon()

    def clean_lexicon(self):
        englishStemmer=SnowballStemmer("english")
        stemWords = []
        final_lexicon_dict={}
        final_lexicon_list=[]

        for key, values in self.lexicon_dict.items():
            if key in words.words():
                stemWords.append(englishStemmer.stem(key))

        stemWords = list(dict.fromkeys(stemWords))

        for i in range(len(stemWords)):
            if stemWords[i] in self.lexicon_dict:
                final_lexicon_dict[stemWords[i]] = self.lexicon_dict[stemWords[i]]
                final_lexicon_list.append(stemWords[i])

        sorted_lexicon_dict = sorted(final_lexicon_dict.items(), key=operator.itemgetter(1))
        sorted_lexicon_list = final_lexicon_list.sort()
        print(sorted_lexicon_list)

        return (sorted_lexicon_dict, sorted_lexicon_list)


    '''

    def score_sentence(self, text):

        #get_language_model
        embedder = SentenceTransformer(self.model_language)

        #get_seeds_embeddings
        pos_seeds = self.clean_lexicon_list[:int(self.seed_size)]
        neg_seeds = self.clean_lexicon_list[-int(self.seed_size):]

        pos_corpus_embeddings = embedder.encode(pos_seeds)        
        neg_corpus_embeddings = embedder.encode(neg_seeds)


        #get_distance
        text_embedding = embedder.encode(text)
        distances_pos = scipy.spatial.distance.cdist([text_embedding], pos_corpus_embeddings, "cosine")[0]
        distances_neg = scipy.spatial.distance.cdist([text_embedding], neg_corpus_embeddings, "cosine")[0]


        if self.aggregation_method == "sum":
            pos_score=0.0
            neg_score=0.0

            for i in range(len(distances_pos)):
                pos_score = pos_score + (1-distances_pos[i])
                neg_score = neg_score + (1-distances_neg[i])

            score = pos_score - neg_score

        if self.aggregation_method == "avg":
            pos_score = sum(1-distances_pos)/len(distances_pos)
            neg_score = sum(1-distances_neg)/len(distances_neg)
            score = pos_score - neg_score

            #normalisation between [-1,1]
            #old_max_val = 0.5
            #old_min_val = -0.5
            #new_max_val = 1
            #new_min_val = -1
            #score = new_min_val + (score - old_min_val) * (new_max_val - new_min_val) / (old_max_val - old_min_val)

        if self.aggregation_method == "max":
            pos_score = (1-(min(distances_pos)))
            neg_score = (1-(min(distances_neg)))
            score = pos_score - neg_score

        return score

    def score_list(self, thelist):
        score_dict={}
        for x in range(len(thelist)):
            score = self.score_sentence(thelist[x])
            score_dict[thelist[x]]=score
        return score_dict



