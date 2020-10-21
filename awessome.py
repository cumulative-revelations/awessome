# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:36:44 2020
@author: Amal Htait
"""

import scipy
from sentence_transformers import SentenceTransformer
import operator



class SentimentIntensityAggregator:
    def __init__(self, pos_dists, neg_dists):
        self.pos_dists=pos_dists
        self.neg_dists=neg_dists
    
class SumSentimentIntensityAggregator(SentimentIntensityAggregator):
    def __init__(self, pos_dists, neg_dists):
        super().__init__(pos_dists, neg_dists)

    def getScore(self)    
        pos_score=0.0
        neg_score=0.0
        for i in range(len(self.pos_dists)):
            pos_score=pos_score + (1-self.pos_dists[i])
            neg_score=neg_score + (1-self.neg_dists[i])
        score=pos_score - neg_score       
        return score

class AvgSentimentIntensityAggregator(SentimentIntensityAggregator):
    def __init__(self, pos_dists, neg_dists):
        super().__init__(pos_dists, neg_dists)

    def getScore(self)    
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
    def __init__(self, pos_dists, neg_dists):
        super().__init__(pos_dists, neg_dists)

    def getScore(self)    
        pos_score=(1-(min(self.pos_dists)))
        neg_score=(1-(min(self.neg_dists)))
        score=pos_score - neg_score
        return score



class SentimentIntensityScorerCreator:

    def __init__(self, lexicon_file, seed_size, aggregation_method, model_language, weighted=False):
        
        self.lexicon_list=lexicon_list
        self.seed_size=seed_size
        self.aggregation_method=aggregation_method
        self.model_language=model_language
        self.weighted=weighted

        #The lexicon source of seed-words
        self.lexicons=['vader','labmt']
        if self.lexicon_file in self.lexicons:
            self.lexicon_list, self.lexicon_dict=readSeedLexicon(self.lexicon_file)
        else:
            #default
            self.lexicon_list, self.lexicon_dict=readSeedLexicon('vader')

        #The size of seeds list   
        if self.seed_size > len(self.lexicon_list)/2:
            self.seed_size=len(self.lexicon_list)/2

        #The used model language for embedding
        self.models=[
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

        if self.model_language in self.models:
            self.embedder=SentenceTransformer(self.model_language)
        else:
            #default
            self.embedder=SentenceTransformer('bert-base-nli-mean-tokens')


        #The seeds selection + their embeddings
        pos_seeds=self.lexicon_list[:int(seed_size)]
        neg_seeds=self.lexicon_list[-int(seed_size):]
        self.pos_seeds_embeddings=self.embedder.encode(pos_seeds)        
        self.neg_seeds_embeddings=self.embedder.encode(neg_seeds)

        self.aggregators={
            'sum': SumSentimentIntensityAggregator(),
            'avg': AvgSentimentIntensityAggregator(),
            'max': MaxSentimentIntensityAggregator()
        }

        if self.aggegration_method in self.aggregators:
            self.aggregator=self.aggregators[self.aggregation_method]
        else:
            #default
            self.aggregator=self.aggregators['avg']


    def readSeedLexicon(self, lexicon_file):
        lexicon_list=[]
        lexicon_dict={}
        seeds=open("lexicon/"+lexicon_file+".txt", "r", encoding='utf-8-sig').readlines()
        for i in range(len(seeds)):
            line=seeds[i].split('\t')
            lexicon_dict[line[0].strip()]=line[1].strip()
            lexicon_dict=dict(sorted(lexicon_dict.items(), key=operator.itemgetter(1),reverse=True))
        return lexicon_dict.keys(), lexicon_dict

    def cosinSim(self, text_embedding, seeds_embeddings):
        return scipy.spatial.distance.cdist([text_embedding], seeds_embeddings, "cosine")[0]

    def splitLongText(self, text):
        max_length=256
        separator=' '
        text_length=len(text.split())
        if text_length > max_length:
            text_list=text.split()[:max_length]   
            text=separator.join(text_list) 
        return text 

    def add_weight(self, distances_pos, distances_neg):
            distances_pos_w=[]
            distances_neg_w=[]  
            for i in range(len(distances_pos)):
                distances_pos_w.append(distances_pos[i] * float(self.lexicon_dict[self.lexicon_list[i]]))
                distances_neg_w.append(distances_neg[i] * float(self.lexicon_dict[self.lexicon_list[i]]))
    return distances_pos_w,distances_neg_w

class SentimentIntensityScorer(SentimentIntensityScorerCreator):

    def __init__(self, lexicon_file, seed_size, aggregation_method, model_language, weighted):
        super().__init__(lexicon_file, seed_size, aggregation_method, model_language, weighted)
         
    def scoreSentence(self, text):
        text=super.splitLongText(text)
        text_embedding=super.embedder.encode(text)
        distances_pos=super.cosinSim(text_embedding, super.pos_seeds_embeddings)
        distances_neg=super.cosinSim(text_embedding, super.neg_seeds_embeddings)
        if super.weighted == True:
            distances_pos, distances_neg=super.add_weight(distances_pos,distances_neg)
        score=super.aggregator.getScore(distances_pos,distances_neg)
        return score

    def scoreList(self, sentences_list):
        score_dict={}
        for i in range(len(sentences_list)):
            score=self.score_sentence(sentences_list[i])
            score_dict[sentences_list[i]]=score
        return score_dict






