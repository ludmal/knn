 
import csv
import random
import math
import operator
 
def loadDs(filename, split, trainSet=[] , testSet=[], signal = 4):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(signal):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
 
 
def distance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNN(trainSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainSet)):
		dist = distance(testInstance, trainSet[x], length)
		distances.append((trainSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
def resp(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def accuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	
def main():
	# prepare data
	trainSet=[]
	testSet=[]
	split = 0.67
	loadDs('traindata.csv', split, trainSet, testSet, 4)
	print 'Train set: ' + repr(len(trainSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNN(trainSet, testSet[x], k)
		result = resp(neighbors)
		predictions.append(result)
		print('> predicted Decision=' + repr(result) + ', Actual Decision=' + repr(testSet[x][-1]))
	accuracy = accuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
main()
