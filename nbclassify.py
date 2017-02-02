# @Author: Sagar Makwana

from sys import argv
import re
import json 
import math

#SuperDict
superDict = {}

#Stopwords
stopWords = ["", "-", "!", ",", ".", ":"," "
                   "a", "able", "about", "all", "also", "am", "an", "and", "any", "as", "are", "at",
                   "be", "but", "by",
                   "can",
                   "did", "do"
                          "etc",
                   "find", "for", "from",
                   "get", "go",
                   "have", "had", "he", "her", "him", "how",
                   "i", "if", "in", "is", "it", "its",
                   "me", "my",
                   "of", "on", "or", "our",
                   "so",
                   "than", "that", "the", "their", "there", "these", "they", "things", "this", "to", "too",
                   "you", "youll", "your",
                   "us", "up",
                   "was", "want", "we", "were", "what", "when", "where", "which", "whom", "why", "will", "with", "who"]


#File Loc
trainTextFileLoc = argv[1]

#Generation of raw text and the uids
corpus = []
uuids = []

for line in open(trainTextFileLoc):
    temp = line.split(' ',1)
    corpus.append(re.sub(r'[^\w\s]',' ',temp[1].strip()).lower())
    uuids.append(temp[0].strip())

#retrieve the model from nbmodel.txt
model = {}
priors = {}

with open('nbmodel.txt', 'r') as fp:
    superDict = json.load(fp)

priors = superDict['priors']
model = superDict['conditionals']    

#Calculating the final results
resultDict1 = []
resultDict2 = []
for entry in corpus:
    logProbTruthful = 0
    logProbDeceptive = 0
    logProbPositive = 0
    logProbNegative = 0
    words = entry.split(' ')
    for word in words:
        if word in model and word not in stopWords:
            logProbTruthful += math.log(model[word]['truthful'])
            logProbDeceptive += math.log(model[word]['deceptive'])
            logProbPositive += math.log(model[word]['positive'])
            logProbNegative += math.log(model[word]['negative'])
            
    logProbTruthful += math.log(priors['truthful'])
    logProbDeceptive += math.log(priors['deceptive'])
    logProbPositive += math.log(priors['positive'])
    logProbNegative += math.log(priors['negative'])
    
    if logProbTruthful > logProbDeceptive:
        resultDict1.append('truthful')
    else:
        resultDict1.append('deceptive')
            
    if logProbPositive > logProbNegative:
        resultDict2.append('positive')
    else:
        resultDict2.append('negative')
        
#Printing the resultsto nboutput.txt    
with open('nboutput.txt', 'w') as fp:
    for count in range(len(uuids)):
        fp.write(uuids[count] + ' ' + resultDict1[count] + ' ' + resultDict2[count] + '\n' )
