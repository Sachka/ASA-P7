import random

test = "src/sequoia-corpus.np_conll"

def split(filename, randomize=False, proportions=(0.8,0.1,0.1)):
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
    corpus = []
    sentence = [['B1','B'],['B2','B']]
    sentences = []
    instream = open(filename, 'r', encoding="utf-8")
    line = instream.readline()
    while line:
        word_annotation = line.split()
        if line == "\n":
            if len(sentence) != 0:
                sentence.extend([['F1'],['F2']])
                sentences.append(sentence)
            sentence = [['B1', 'B'], ['B2', 'B']]
        else:
            sentence.append([word_annotation[1],word_annotation[3]])
        line = instream.readline()
    if len(sentence) != 0:
        sentence.extend([['F1'], ['F2']])
        sentences.append(sentence)
    instream.close()
    # print(sentences[0])
    for sent in sentences:
        for i in range(2, len(sent)-2):
            feats = {}
            feats["w-2={}".format(sent[i-2][0])] = 1
            feats["w-1={}".format(sent[i-1][0])] = 1
            feats["w={}".format(sent[i][0])] = 1
            feats["w+1={}".format(sent[i+1][0])] = 1
            feats["w+2={}".format(sent[i+2][0])] = 1
            feats["t-2={}".format(sent[i-2][1])] = 1
            feats["t-1={}".format(sent[i-1][1])] = 1
            corpus.append((feats,sent[i][1]))
    print(corpus[0])
    return corpus







#split(test, True)
read_corpus(test+".test")
