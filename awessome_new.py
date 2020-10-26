# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:36:44 2020
@author: Amal Htait
"""

import scipy
from sentence_transformers import SentenceTransformer
import operator
from awessome_aggregator import SumSentimentIntensityAggregator, AvgSentimentIntensityAggregator, MaxSentimentIntensityAggregator


class Builder:

   def getLexicon(self): pass
   def getAggregation(self): pass
   def getModel(self): pass
   def getSeeds(self): pass
   def scorer(self): pass

class SentimentIntensityFromPrebuiltLexiconsBuilder(Builder):

   def __init__(self, lexiconFile, seedSize, aggregationMethod, modelLanguage, weighted=False):
      self.lexiconFile=lexiconFile
      self.seedSize=seedSize
      self.aggregationMethod=aggregationMethod
      self.modelLanguage=modelLanguage
      self.weighted=weighted

      self.reset()

   def reset(self):
      lexiconList, lexiconDict = self.getLexicon()
      aggregator = self.getAggregation()
      embedder = self.getModel()
      pos_seedsEmbeddings, neg_seedsEmbeddings = self.getSeeds(lexiconList,embedder)

      self._scorer = SentimentIntensityScorer(pos_seedsEmbeddings, neg_seedsEmbeddings, aggregator, embedder, self.weighted)


   def scorer(self):
      scorer = self._scorer
      self.reset()
      return scorer

   def getLexicon(self):
      lexicons=['vader','labmt']
      if self.lexiconFile in lexicons:
         lexicon = self.lexiconFile
      else:
         #default
         lexicon = 'vader'

      lexiconDict={}
      seeds=open("lexicon/"+lexicon+".txt", "r", encoding='utf-8-sig').readlines()
      for i in range(len(seeds)):
         line=seeds[i].split('\t')
         lexiconDict[line[0].strip()]=line[1].strip()
         lexiconDict=dict(sorted(lexiconDict.items(), key=operator.itemgetter(1),reverse=True))

      return list(lexiconDict.keys()), lexiconDict

   
   def getAggregation(self):
      aggregators={
         'sum': SumSentimentIntensityAggregator,
         'avg': AvgSentimentIntensityAggregator,
         'max': MaxSentimentIntensityAggregator
        }

      if self.aggregationMethod in aggregators:
         aggregator=aggregators[self.aggregationMethod]
      else:
         #default
         aggregator=aggregators['avg']

      return aggregator



   def getModel(self):
      models=[
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

      if self.modelLanguage in models:
         embedder=SentenceTransformer(self.modelLanguage)
      else:
         #default
         embedder=SentenceTransformer('bert-base-nli-mean-tokens')
      return embedder


   def getSeeds(self,lexiconList,embedder):

      if int(self.seedSize) > len(lexiconList)/2:
         __seedSize=len(lexiconList)/2
      else:
         __seedSize = self.seedSize

      posSeeds=lexiconList[:int(__seedSize)]
      negSeeds=lexiconList[-int(__seedSize):]
      pos_seedsEmbeddings=embedder.encode(posSeeds)        
      neg_seedsEmbeddings=embedder.encode(negSeeds)

      return pos_seedsEmbeddings, neg_seedsEmbeddings



class SentimentIntensityScorer:
   def __init__(self, pos_seedsEmbeddings, neg_seedsEmbeddings, aggregator, embedder, weighted=False):
      self.pos_seedsEmbeddings=pos_seedsEmbeddings
      self.neg_seedsEmbeddings=neg_seedsEmbeddings
      self.aggregator=aggregator
      self.embedder=embedder
      self.weighted=weighted
         

   def scoreSentence(self, text):
      text=self.splitLongText(text)
      text_embedding=self.embedder.encode(text)
      distances_pos=self.cosinSim(text_embedding, self.pos_seeds_embeddings)
      distances_neg=self.cosinSim(text_embedding, self.neg_seeds_embeddings)
      if self.weighted == True:
         distances_pos, distances_neg=self.add_weight(distances_pos,distances_neg)
      score=self.aggregator.getScore(distances_pos,distances_neg)
      return score

   def scoreList(self, sentences_list):
      scoreDict={}
      for i in range(len(sentencesList)):
         score=self.scoreSentence(sentencesList[i])
         scoreDict[sentencesList[i]]=score
      return scoreDict  

   def cosinSim(self, textEmbedding, seedsEmbeddings):
      return scipy.spatial.distance.cdist([textEmbedding], seedsEmbeddings, "cosine")[0]

   def splitLongText(self, text):
      max_length=256
      separator=' '
      textLength=len(text.split())
      if text_length > max_length:
         textList=text.split()[:maxLength]   
         text=separator.join(textList) 
      return text 

   def addWeight(self, distances_pos, distances_neg):
      distances_pos_w=[]
      distances_neg_w=[]  
      for i in range(len(distances_pos)):
         distances_pos_w.append(distances_pos[i] * float(self.lexiconDict[self.lexiconList[i]]))
         distances_neg_w.append(distances_neg[i] * float(self.lexiconDict[self.lexiconList[i]]))
      return distances_pos_w,distances_neg_w

  
if __name__ == "__main__":

   builder = SentimentIntensityFromPrebuiltLexiconsBuilder('vader','100','avg','bert-base-nli-mean-tokens')
   
   print(builder.scorer.scoreSentence("I am Happy"))
