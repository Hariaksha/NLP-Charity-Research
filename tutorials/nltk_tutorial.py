# Natural Language Toolkit - Python's API library for performing an array of tasks in human language
# like classification, tokenization, stemming, tagging, Leparsing, semantic reasoning, etc.
import re
import string

import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords          # module for stop words that come with NLTK
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer   # module for tokenizing strings
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def tokenization(): 
    # breaking down text into smaller units (paragraphs -> sentences, sentences -> words)
    # an initial step of any NLP pipeline
    sentence = "GeeksforGeeks is a great learning platform. It is one of the best for Computer Science students."
    print(word_tokenize(sentence))
    print(sent_tokenize(sentence))

    # instantiate your own tokenizer
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    sentence_tokens = tokenizer.tokenize("I ate the cookie.")
    print(sentence_tokens)

def canonicalization_notes():
    # we do not care about form of words, but about conveyed meaning of words
    # so we map each word to root/base form in a process called canonicalization
    # example: play, plays, played, etc. all convey same meaning and are linked to base 'play'
    # two canonicalization techniques are stemming and lemmatization
    return

def stemming():  
    # stemming generates base word by removing affixes
    # uses pre-defined rules to do this
    # do not always lead to semantically meaningful base words
    # but are faster and computationally less expensive than lemmatizers

    porter = PorterStemmer() # create an object of class PorterStemmer
    
    # these four examples make the word 'play'
    print(porter.stem("play"))
    print(porter.stem("playing"))
    print(porter.stem("plays"))
    print(porter.stem("played"))
    
    # this example reduces the input to a meaningless word
    print(porter.stem("Communication"))

def lemmatization():
    # lematization involves grouping together inflected forms of the same word    
    # so we can reach out to the base form of any word which will be meaningful in nature
    # slower and computationally more expensive than stemmers
    
    lemmatizer = WordNetLemmatizer() # create an object of class WordNetLemmatizer

    # these four examples make 'play'
    # lemmatization requires the part of speech (verb here) as input
    print(lemmatizer.lemmatize("plays", 'v'))
    print(lemmatizer.lemmatize("played", 'v'))
    print(lemmatizer.lemmatize("play", 'v'))
    print(lemmatizer.lemmatize("playing", 'v'))

    # always result in meaningful base words
    print(lemmatizer.lemmatize("Communication", 'v'))

def POS_tagging():
    # part-of-speech (POS) tagging refers to assigning each word to its POS
    # helps give a better syntactic overview of a sentence
    text = "GeeksforGeeks is a Computer Science platform."
    tokenized_text = word_tokenize(text)
    print(tokenized_text)
    tags = tokens_tag = pos_tag(tokenized_text)
    print(tags)

def stopwords_and_punctuation():
    nltk.download('stopwords')
    stopwords_english = stopwords.words('english') # sometimes must customize stop words list for our applications
    print('Stop words\n')
    print(stopwords_english)

    print('\nPunctuation\n')
    print(string.punctuation)

def main():
    POS_tagging()
    nltk.download('stopwords')


if __name__=="__main__":
    main()

