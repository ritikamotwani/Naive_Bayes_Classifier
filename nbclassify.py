# @Author: Sagar Makwana

from sys import argv
import re
import json 
import math

#File Loc
trainTextFileLoc = argv[1]

#Raw file input
corpus = [re.sub(r'[^\w\s]','',line.rstrip('\n')).lower().split(' ', 1)[1] for line in open(trainTextFileLoc)]

model = {}
with open('nbmodel.txt', 'r') as fp:
    model = json.load(fp)

resultDict1 = []
resultDict2 = []
for entry in corpus:
    logProbTruthful = 0
    logProbDeceptive = 0
    logProbPositive = 0
    logProbNegative = 0
    words = entry.split(' ')
    for word in words:
        if word in model:
            logProbTruthful += math.log(model[word]['truthful'])
            logProbDeceptive += math.log(model[word]['deceptive'])
            logProbPositive += math.log(model[word]['positive'])
            logProbNegative += math.log(model[word]['negative'])
            
    if logProbTruthful > logProbDeceptive:
        resultDict1.append('truthful')
    else:
        resultDict1.append('deceptive')
            
    if logProbPositive > logProbNegative:
        resultDict2.append('positive')
    else:
        resultDict2.append('negative')
            
print 'Done'