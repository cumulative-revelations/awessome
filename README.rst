====================================
AWESSOME
====================================

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


* `Citation Information`_
* `Installation`_
* `Python Demo and Code Examples`_


Citation Information
------------------------------------

If you use the AWESSOME sentiment analysis tools in your research, please cite the following paper. For example:  

  **Htait, A. & Azzopardi, L. (2020). ...... 2020.** 


====================================
Installation
====================================

To install AWESSOME:  

#. The simplest is to use the command line to do an installation from `[PyPI] <https://pypi.python.org/pypi/awessome>`_ using pip, e.g., 
    ``> pip install awessome``
#. If you already have AWESSOME and simply need to upgrade to the latest version, e.g., 
    ``> pip install --upgrade awessome``
#. You could also clone this `[GitHub repository] <https://github.com/cumulative-revelations/awessome>`_ 
#. You could download and unzip the `[full master branch zip file] <https://github.com/cumulative-revelations/awessome/archive/master.zip>`_ 

In addition to the AWESSOME Python module, you will also be downloading two lexicon dictionaries ([VADER](https://github.com/cjhutto/vaderSentiment) , 
[LabMT](https://trinker.github.io/qdapDictionaries/labMT.html)).


====================================
Python Demo and Code Examples
====================================

The AWESSOME framework can be flexibility adapted to cater for different seed lexicons and different neural word embeddings models in order to produce corpus specific lexicons without the need for extensive supervised learning and retraining.

Through parameters, AWESSOME gives the possibility to:

#. Choose between different available pre-trained language models, such as: BERT (bert-base-nli-mean-tokens) and Distilbert (distilbert-base-nli-stsb-mean-tokens)
   Note: some pre-trained language models would need GPU.
#. Employ different aggregation methods on the similarity scores of the sentence with each term in the seeds lists: Average (avg), Maximum (max) and Sum (sum).
#. Select one of two possible similarity measures, provided by [scipy](https://www.scipy.org/): cosine and euclidean.
   Note: if no similarity measure is provided, cosine is applied as a default measure.
#. Select a source of positive and negative seeds lists, where the user can provide a new lexicon file, or used the pre-built lexicons: vader or labmt (built based on VADER and LabMT sentiment lexicons).
   Note: if no lexicon file is provided, vader is applied as a default seeds lists source.
#. Choose the size of seeds lists, created based on the lexicon files.
   Note: if no size is provided, the value of 500 is used as default seeds lists size.
#. In addition, AWESSOME gives the possiblity to apply a "Weighted Similarity" to seeds, by multiplying the similarity score by the sentiment score of the seeds.
   users have the option to use that feature of note by simply choosing "weighted" as True or False.
   Note: if the weighted value is not provided, it is considered by default as False.
 
An example Demo is added under the name of : awessome_demo.py


