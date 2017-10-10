import random

test = "sequoia-corpus.np_conll"

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

split(test, True)
