from builder import *



if __name__ == "__main__":

   sis_builder = SentimentIntensityScorerBuilder('avg','bert-base-nli-mean-tokens')
   
   sis_scorer = sis_builder.build_scorer_from_prebuilt_lexicon('vader')

   print(sis_scorer.name)
   
   sentences = ['I am happy',
                'I am feeling very sad',
                'I cant wait to go to the party',
                'I am not happy']
   
   for sentence in sentences:
       print(sentence, sis_scorer.score(sentence))
 