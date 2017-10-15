# encoding: utf-8
from math import exp, log
import random
from SparseWeightVector import SparseWeightVector

test = "src/sequoia-corpus.np_conll"


def split(filename, randomize=False, proportions=(0.8, 0.1, 0.1)):
    sentence = []
    sentences = []
    instream = open(filename, 'r')
    line = instream.readline()
    while line:
        if line == "\n":
            if len(sentence) != 0:
                sentences.append(sentence)
            sentence = []
        else:
            sentence.append(line)
        line = instream.readline()
    if len(sentence) != 0:
        sentences.append(sentence)
    if randomize:
        random.shuffle(sentences)
    instream.close()
    print(len(sentences))
    train = sentences[:int(len(sentences) * proportions[0])]
    dev = sentences[int(len(sentences) * proportions[0]):int(len(sentences) * proportions[0]+len(sentences) * proportions[1])]
    test = sentences[int(len(sentences) * proportions[0]+len(sentences) * proportions[1]):]
    print(len(train))
    print(len(dev))
    print(len(test))
    trainfile = open(filename+".train", 'w')
    devfile = open(filename+".dev", 'w')
    testfile = open(filename+".test", 'w')
    for sentence in train:
        for word in sentence:
            trainfile.write(word)
        trainfile.write("\n")
    for sentence in dev:
        for word in sentence:
            devfile.write(word)
        devfile.write("\n")
    for sentence in test:
        for word in sentence:
            testfile.write(word)
        testfile.write("\n")
    trainfile.close()
    devfile.close()
    testfile.close()

def read_corpus(filename):
    sentence = ""
    sentences = []
    instream = open(filename, 'r', encoding="utf-8")
    line = instream.readline()
    while line:
        word_annotation = line.split()
        if line == "\n":
            if sentence != "":
                sentences.append(sentence)
            sentence = ""
        else:
            sentence += " " + word_annotation[1] + "}" + word_annotation[3]
        line = instream.readline()
    if sentence != "":
        sentences.append(sentence)
    instream.close()
    return make_dataset(sentences)

def make_dataset(text):
    """
    @param text: a list of strings of the form : Le/D chat/N mange/V la/D souris/N ./PONCT
    @return    : an n-gram style dataset
    """
    BOL = '@@@'
    EOL = '$$$'

    dataset = []
    for line in text:
        line         = list([ tuple(w.split('}'))  for w in line.split()])
        tokens       = [BOL] + list([tok for(tok, pos) in line]) + [EOL]
        pos          = list([pos for(tok,pos) in line])
        tok_trigrams = list(zip(tokens, tokens[1:],tokens[2:]))
        # tok_bigramsL = list(zip(tokens,tokens[1:]))
        # tok_bigramsR = list(zip(tokens[1:],tokens))

        dataset.extend(zip(pos, zip(tok_trigrams)))

    return dataset


class AvgPerceptron:

    def __init__(self):

        self.model   = SparseWeightVector()
        self.Y       = [] #classes

    def train(self,dataset,step_size=0.1,max_epochs=50):

        self.Y = list(set([y for (y,x) in dataset]))

        for e in range(max_epochs):

            loss = 0.0
            for y,x in dataset:
                ypred = self.tag(x)
                if y != ypred:
                    loss += 1.0
                    delta_ref  = SparseWeightVector.code_phi(x,y)
                    delta_pred = SparseWeightVector.code_phi(x,ypred)
                    self.model += step_size*(delta_ref-delta_pred)
            print ("Loss (#errors) = ",loss)
            if loss == 0.0:
                return

    def predict(self,dataline):
        return list([self.model.dot(dataline,c) for c in self.Y])

    def tag(self,dataline):

        scores = self.predict(dataline)
        imax   = scores.index(max(scores))
        return self.Y[ imax ]

    def test(self,dataset):

        result = list([ (y == self.tag(x)) for y,x in dataset ])
        return sum(result) / len(result)





# # corpus = ['Le/D chat/N mange/V la/D souris/N ./PONCT','La/D souris/N danse/V ./PONCT','Il/Pro la/Pro voit/V dans/P la/D cour/N ./PONCT','Le/D chat/N la/Pro mange/V ./PONCT',"Le/D chat/V la/Pro mange/V"]
# D = make_dataset(corpus)
# print(D)



p = read_corpus(test+".test")
perc = AvgPerceptron()
perc.train(p,step_size=1.0)
print(perc.test(D))
