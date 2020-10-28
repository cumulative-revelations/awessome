A Word Embedding Sentiment Scorer Of Many Emotions (AWESSOME) is a framework with 
the purpose of predicting the sentiment intensity of sentences.


AWESSOME relies on sentiment seed-words and word embedding, 
where the similarity between the vector representation of two sentences is considered as a 
reflection of their sentiment similarity. 


AWESSOME capitalizes on pre-existing lexicons ([VADER](https://github.com/cjhutto/vaderSentiment) , 
[LabMT](https://trinker.github.io/qdapDictionaries/labMT.html)), but custom lexicons can also be used, and created
using AWESSOME.


AWESSOME also draws upon the recent advances in language model by using the Transformers from HuggingFace,
 to create word embeddings using BERT, RoBERTa, etc.


AWESSOME is scalable, and does not require any training data, while providing more fine grained (and accurate) 
sentiment intensity scores of words,  phrases and text.
