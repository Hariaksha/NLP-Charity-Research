import spacy # free open-source library for NLP in Python. features NER, POS tagging, dependency parsing, word vectors, and more
from spacy import displacy # library for displaying sentence structures. works in jupyter notebook but not in vsc
import numpy as np
from spacy.matcher import Matcher
from spacy.language import Language
import re
from spacy.tokens import Span
from spacy.util import filter_spans
# https://github.com/explosion/spaCy/issues/4577

nlp = spacy.load('en_core_web_sm')

# containers are spaCy objects that contain a large quantity of data about a text
# when we analyze texts with the spaCy framework, we create different container objects to do that

# open the text file and read it into a text variable before printing it
with open("tutorials/wiki_us.txt", 'r') as f:
    text = f.read()
print(text)

# using nlp function (which uses the en_core_web_sm library) with text as an argument
# this prints something slightly different than the original
doc = nlp(text)
print(doc)

# the length of the two are not the same. why?
print(len(text))
print(len(doc))

# iterate a little through text and doc to see how they are different
for token in text[:10]: # each character is the element
    print(token)
for token in doc[:10]: # text is tokenized so words and important elements become one element
    # this is different from python split method because spacy separates punctuation marks when they are not relevant
    print(token)

# sentence boundary detection (SBD) is the identification of sentences in a text
for sent in doc.sents:
    print(sent)

# the .sents attribute is a generator object, so it is not subscriptable as done in the line below
# sentence1 = doc.sents[0]
    
# do this instead
sentence1 = list(doc.sents)[0]

# exploring attribute types of tokens here
token2 = sentence1[2]
print(token2)
print(token2.text)
print(token2.left_edge) # tells us that this is part of a multi-token span, and whatever is here is the word left to the entire span. prints "The" from "The United States" because the token is "States"
print(token2.right_edge)
print(token2.ent_type) # type of entity -> provides an integer
print(token2.ent_type_) # type of entity as a string (more useful)
print(token2.ent_iob_) # if 'I' is produced, it is inside an entity, 'B' means beginning of an entity, 'O' means outside of entity
print(token2.lemma_) # what word looks like with no inflection
print(sentence1[12].lemma_) # in this example, prints 'know' when original text was 'known'. basically shows uninflected form of verb
print(token2.morph) # morphological output ex. noun/verb type, etc.
print(token2.pos_) # part of speech
print(token2.dep_) # what role it plays in sentence (dependency) ex. nominal subject, verb
print(token2.lang_) # world language

text = "Mike enjoys playing football."
doc2 = nlp(text)
for token in doc2:
    print(token.text, token.pos_, token.dep_)

displacy.render(doc2, style='dep')

# learning Named Entity Recognition (NER) now
for ent in doc.ents:
    print(ent.text, ent.label_)
displacy.render(doc, style='ent')

# we will now use the medium size english nlp model
nlp = spacy.load('en_core_web_md')
with open('tutorials/wiki_us.txt') as f:
    text = f.read()
doc = nlp(text)
sentence1 = list(doc.sents)[0]

# print words similar to given word
your_word = 'country'
ms = nlp.vocab.vectors.most_similar(
    np.asarray([nlp.vocab.vectors[nlp.vocab.strings[your_word]]]), n=10)
words = [nlp.vocab.strings[w] for w in ms[0][0]]
distances = ms[2]
print(words)

# find similarity between two documents. similarity is calculated with word embeddings (semantic/pragmatic meanings of words)
doc1 = nlp("I like salty fries and hamburgers.")
doc2 = nlp("Fast food tastes very good.")
print(doc1, '<->', doc2, doc1.similarity(doc2))
doc3 = nlp("The Empire State Building is in New York.")
print(doc1, '<->', doc3, doc1.similarity(doc3))
doc4 = nlp("I enjoy oranges.")
doc5 = nlp("I enjoy apples.")
print(doc4, '<->', doc5, doc4.similarity(doc5))
doc6 = nlp("I enjoy burgers.")
print(doc4, '<->', doc6, doc4.similarity(doc6))
french_fries = doc1[2:4]
burgers = doc1[5]
print(french_fries, "<->", burgers, french_fries.similarity(burgers))

# spaCy is an NLP framework as well as a way of designing/implementing complex pipelines
# a pipeline is a sequence of pipes, or actors on data, that make alterations to data or extract information from it
# if i only have to do one task, like separate by sentences, it is smart to create your own pipeline like above with the features that you want. using one of the premade pipelines will take longer

nlp = spacy.blank('en') # blank spaCy pipeline with english tokenizer
nlp.add_pipe('sentencizer') # create a pipeline with sentencizer. adds a pipe to a spaCy pipeline
nlp.analyze_pipes()

# you can use a rules-based or ML-based approach to add custom features to a language pipeline
# rules-based when you can make a set of rules for known things, or when you can use regex or linguistic features
# ML for when rules are complicated or you do not know the rules
# NER date recognition (ex. 1/1/2000, 1 January 2000, etc.) uses rules-based approach
# capturing names uses ML-based approach because there are too many options for names (prefixes, first name, last name, suffixes, etc.)

# we want our pipeline to recognize the place as a place (geopolitical entity) and the name as a film
nlp = spacy.load('en_core_web_sm')
text = 'West Chestertenfieldville was referenced in Mr. Deeds.'
doc = nlp(text)
for ent in doc.ents: 
    print (ent.text, ent.label_) # this makes West Chestertenfieldville and Deeds a person. 
    # we want the first to be a location and the other to be a film, but there is no entity label for film.
    # we will fix this with an entity ruler, which are useful for fictional things
ruler = nlp.add_pipe('entity_ruler')
patterns = [{'label': 'GPE', 'pattern': 'West Chestertenfieldville'}] # patterns are the things that spaCy model will look for and assign when it finds a pattern. it will always be a list of dictionaries
ruler.add_patterns(patterns)
doc2 = nlp(text)
for ent in doc2.ents:
    print(ent.text, ent.label_) # does not work because NER happens before entity ruler

# this version of the code fixes the last error
nlp2 = spacy.load('en_core_web_md')
patterns = [{'label': 'GPE', 'pattern': 'West Chestertenfieldville'}, {'label': 'film', 'pattern': 'Mr. Deeds'}]
ruler = nlp2.add_pipe("entity_ruler", before='ner')
ruler.add_patterns(patterns)
doc = nlp2(text)
for ent in doc.ents:
    print(ent.text, ent.label_) # does not work because NER happens before entity ruler

# toponym resolution = labeling things that can have many labels depending on context. for example, Mr. Deeds can be film or person. this is an unresolved problem in NLP, but it is better with ML than rules



# now we learn to use the Matcher, which helps us find specific linguistic structures in text
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
pattern = [{"LIKE_EMAIL":True}] # pattern is always a list of dictionaries
matcher.add("EMAIL_ADDRESS", [pattern]) # add pattern to matcher
doc = nlp("This is an email address: hari@gmail.com")
matches = matcher(doc)
print(matches) # each match is a tuple with three numbers: lexeme (id), start index, end index
print(nlp.vocab[matches[0][0]].text) # this shows us what the lexeme is in the nlp.vocab


# in example below, we use Matcher to recognize Martin Luther King Jr. and other multi-names as one entity/pattern in text. we also find all instances of proper nouns being followed by verbs
with open('tutorials/wiki_mlk.txt', 'r') as f:
    text = f.read()
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
pattern = [{'POS': "PROPN", 'OP':'+'}, {'POS':'VERB'}] # looks for proper noun 1 or more times to create one pattern. greedy makes the matches have longest first instead of in sequential order
matcher.add("PROPER_NOUN", [pattern], greedy='LONGEST')
doc = nlp(text)
matches = matcher(doc)
matches.sort(key = lambda x: x[1]) # sort it by index 1 or start index so that matches are in sequential order in text again.
print(len(matches))
for match in matches[:10]:
    print(match, doc[match[1]:match[2]])

# we will now learn about custom components, which are things that you can modify to make spaCy capable of tasks it cannot do by default
nlp = spacy.load("en_core_web_sm")
doc = nlp("Britain is a place. Mary is a doctor.")
for ent in doc.ents:
    print(ent.text, ent.label_) # this prints; Britain GPE, Mary PERSON
# maybe we want to get rid of every GPE tag and/or label it as LOC instead
@Language.component('remove_gpe')
def remove_gpe(doc): # this is a custom component
    original_ents = list(doc.ents)
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            original_ents.remove(ent)
    doc.ents = original_ents
    return doc
nlp.add_pipe("remove_gpe")
nlp.analyze_pipes()


# now we will learn basic usage of regex with spaCy
# regex does not work across multiple tokens in current spaCy
# use regex when pattern matching is independent of lemma, POS, other linguistic features of spaCy
text = 'Paul Newman was an American actor, but Paul Hollywood is a British TV host. The name Paul is quite common.' 
pattern = r'Paul [A-Z]\w+'
matches = re.finditer(pattern, text)
for match in matches:
    print(match) # regex Match objects



nlp = spacy.blank('en')
doc = nlp(text)
original_ents = list(doc.ents)
mwt_ents = [] # multi word token entity
for match in re.finditer(pattern, doc.text):
    start, end = match.span()
    span = doc.char_span(start, end)
    print(span)
    if span is not None:
        mwt_ents.append((span.start, span.end, span.text))
print(mwt_ents)
for ent in mwt_ents:
    start, end, name = ent
    per_ent = Span(doc, start, end, label='PERSON')
    original_ents.append(per_ent)
doc.ents = original_ents
print(doc.ents)
for ent in doc.ents:
    print(ent.text, ent.label_)


# create custom component or pipe using regex. this works on multi token spans
@Language.component("paul_ner")
def paul_ner(doc):
    pattern = r'Paul [A-Z]\w+'
    original_ents = list(doc.ents)
    mwt_ents = [] # multi word token entity
    for match in re.finditer(pattern, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span is not None:
            mwt_ents.append((span.start, span.end, span.text))
    for ent in mwt_ents:
        start, end, name = ent
        per_ent = Span(doc, start, end, label='PERSON')
        original_ents.append(per_ent)
    doc.ents = original_ents
    return doc

@Language.component("cinema_ner")
def cinema_ner(doc):
    pattern = r'Hollywood'
    original_ents = list(doc.ents)
    mwt_ents = [] # multi word token entity
    for match in re.finditer(pattern, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span is not None:
            mwt_ents.append((span.start, span.end, span.text))
    for ent in mwt_ents:
        start, end, name = ent
        per_ent = Span(doc, start, end, label='PERSON')
        original_ents.append(per_ent)
    filtered = filter_spans(original_ents) # if there is any span overlap like in 'Hollywood' and 'Paul Hollywood', preference goes to larger span so that there is no span overlap
    doc.ents = filtered
    return doc



# add custom component to a blank spaCy model
nlp2 = spacy.blank('em')
nlp2.add_pipe('paul_ner')
doc2 = nlp2(text)
print(doc2.ents)
