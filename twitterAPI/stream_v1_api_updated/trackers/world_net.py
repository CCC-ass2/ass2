from nltk.corpus import wordnet as wn
import nltk

nltk.download('wordnet')
print(wn.synsets('sofa') )