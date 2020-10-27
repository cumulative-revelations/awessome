



class SentimentIntensityScorer:
    
   def __init__(self, pos_seedsEmbeddings, neg_seedsEmbeddings, aggregator, embedder, weighted=False):
      self.pos_seedsEmbeddings=pos_seedsEmbeddings
      self.neg_seedsEmbeddings=neg_seedsEmbeddings
      self.aggregator=aggregator
      self.embedder=embedder
      self.weighted=weighted
         

   def score_sentence(self, text):
      text=self.splitLongText(text)
      text_embedding=self.embedder.encode(text)
      distances_pos=self.cosinSim(text_embedding, self.pos_seeds_embeddings)
      distances_neg=self.cosinSim(text_embedding, self.neg_seeds_embeddings)

      if self.weighted == True:
         distances_pos, distances_neg=self.add_weight(distances_pos, distances_neg)
      score=self.aggregator.aggscore(distances_pos, distances_neg)

      return score


   def score_list(self, sentence_list):
      scoreDict={}
      for i in range(len(sentence_list)):
         score=self.scoreSentence(sentence_list[i])
         scoreDict[sentence_list[i]]=score

      return scoreDict  


   def cosinSim(self, textEmbedding, seedsEmbeddings):
      return scipy.spatial.distance.cdist([textEmbedding], seedsEmbeddings, "cosine")[0]


   def split_long_sentence(self, text):
      max_length=256
      separator=' '
      textLength=len(text.split())

      if text_length > max_length:
         textList=text.split()[:maxLength]   
         text=separator.join(textList) 

      return text 


   def add_weight(self, distances_pos, distances_neg):
      distances_pos_w=[]
      distances_neg_w=[]  

      for i in range(len(distances_pos)):
         distances_pos_w.append(distances_pos[i] * float(self.lexiconDict[self.lexiconList[i]]))
         distances_neg_w.append(distances_neg[i] * float(self.lexiconDict[self.lexiconList[i]]))

      return distances_pos_w,distances_neg_w

