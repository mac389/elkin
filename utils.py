import json

import matplotlib.pyplot as plt 
import numpy as np 

READ = 'rb'

import nltk, os, itertools, json, re, string, collections, requests

#from spacy.en import English
from nltk import wordnet
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

READ = 'rb' 
translation_table = json.load(open(os.path.join(os.getcwd(),'..','phikal','data','drug_misnaming.json'),READ))

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return wn.NOUN

def standardize_drug_names(list_of_words):
    #Reconstitute to filter out known words
    for bigram in list(itertools.combinations(list_of_words, 2)):
        if ' '.join(bigram) in translation_table:
            #in place replacement to avoid creating null list
            try:
                list_of_words[list_of_words.index(bigram[0])] = translation_table[' '.join(bigram)]
                list_of_words.remove(bigram[1])
            except ValueError as e:
                print 'Already removed %s'%(' '.join(bigram))

    return list(flatten(list_of_words))

def flatten_(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

def matrix_jaccard(m,jacc):
    idx = np.tril_indices_from(jacc)
    for i,j in zip(*idx):
        jacc[i,j] = jaccard(m[i,:],m[j,:])
    jacc += np.tril(jacc,k=-1).T
    return jacc

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

def jaccard(one,two):
    return np.logical_and(one,two).sum()/float(np.logical_or(one,two).sum())

