import nltk, csv, random, numpy
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer

# transforms text to a word frequency dictionary
def text2dict(text):
	tokens = nltk.word_tokenize(text)

	#for i in range(len(tokens)-1):
	#	tokens.append(tokens[i] + '0' + tokens[i+1])

	dictionary = {}
	for t in tokens:
		if not t.isalnum():
			continue
		t = t.lower()
		if t not in dictionary:
			dictionary[str(t)] = 0
		dictionary[str(t)] += 1

	return dictionary

columns = []
def rows2objects(rows):
	# translate each row into an object
	global columns
	data = []
	first = True
	for r in rows:
		if first:
			columns = r
			first = False
			continue
		
		obj = {}
		for k in range(len(rows[0])):
			obj[rows[0][k]] = r[k].replace('\\X0D\\\\X0A\\',' -- ')
		
		data.append(obj)

	return data

def dictlist(data):
	dictlist = []

	# concatenate text fields from objects, tokenize,
	# create a list of word frequency dictionaries
	# one for each row
	#print columns
	for obj in data:
		text = ''
		for k in columns:
			if 'TEXT' in k:
				text += obj[k]
				
		dt = text2dict(text)
		
		dictlist.append(dt)
		
	return dictlist

def dictionary(rows):
	
	dl = dictlist(rows2objects(rows))

	# print out a sample dictionary for testing
	#print dictlist[0]

	# convert the dictionaries into a matrix
	dv = DictVectorizer()
	#X = dv.fit_transform(dictlist)
	dv.fit(dl)
	
	#return X, y, dv
	return dv

def extractY(data):
	# 0 = SITE_TYPE
	# 1 = BREAST_ER
	# 2 = BREAST_PR
	# 3 = LUNG_CELLTYPE
	# 4 = CRC_CEA
	y0 = []
	y1 = []
	y2 = []
	y3 = []
	y4 = []
	for obj in data:
		y0.append(obj['SITE_TYPE'])
		
		if obj['BREAST_ER'].strip() == '':
			y1.append('NULL')
		else:
			y1.append(obj['BREAST_ER'])
		
		if obj['BREAST_PR'].strip() == '':
			y2.append('NULL')
		else:
			y2.append(obj['BREAST_PR'])
		
		if obj['LUNG_CELLTYPE'].strip() == '':
			y3.append('NULL')
		else:
			y3.append(obj['LUNG_CELLTYPE'])
		
		if obj['CRC_CEA'].strip() == '':
			y4.append('NULL')
		else:
			y4.append(obj['CRC_CEA'])
	
	return [y0, y1, y2, y3, y4]

def test():
	rows = []
	with open('data/training_data.csv','r') as f:
		reader = csv.reader(f,delimiter=',', quotechar='"')
		for r in reader:
			rows.append(r)
			
	dv = dictionary(rows)

	header = rows[0]
	rows = rows[1:]
	random.shuffle(rows)
	l = len(rows)
	
	rowTrain = rows[:int(l*0.7)]
	rowTrain.insert(0,header)
	rowTest = rows[int(l*0.7):]
	rowTest.insert(0,header)
	
	dataTrain = rows2objects(rowTrain)
	XTrain = dv.transform(dictlist(dataTrain))
	eyTrain = extractY(dataTrain)
	yTrain = eyTrain[0]
	
	dataTest = rows2objects(rowTest)
	XTest = dv.transform(dictlist(dataTest))
	eyTest = extractY(dataTest)
	yTest = eyTest[0]

	lr = []
	# fit the matrix to a model 
	for i in range(5):
		lrx = LogisticRegression()
		lrx.fit(XTrain,eyTrain[i])
		lr.append(lrx)
	
	print zip(lr[0].predict(XTest),lr[0].predict_proba(XTest))
	print len(rowTrain), len(rowTest)
	print "Training Size is", XTrain.shape
	print "Testing Size is", XTest.shape
	print "Row length is", len(rows)

	for i in range(5):
		print "Score for",i,"is", lr[i].score(XTest,eyTest[i])

def execute(query):
	# translate csv into rows
	rows = []
	with open('data/training_data.csv','r') as f:
		reader = csv.reader(f,delimiter=',', quotechar='"')
		for r in reader:
			rows.append(r)
			
	dv = dictionary(rows)

	dataTrain = rows2objects(rows)
	XTrain = dv.transform(dictlist(dataTrain))
	eyTrain = extractY(dataTrain)

	# fit the matrix to a model 
	lr = []
	for i in range(5):
		lrx = LogisticRegression()
		lrx.fit(XTrain,eyTrain[i])
		lr.append(lrx)

	ex = dv.transform(text2dict(query))
	outcome = []
	for i in range(5):
		probas = lr[i].predict_proba(ex)[0]
		prediction = lr[i].predict(ex)[0]
		classes = list(lr[i].classes_)
		
		print probas
		print classes
		confidence = probas[classes.index(prediction)]
		print prediction, confidence
		
		if i == 1 and outcome[0] != 'BREAST':
			outcome.append('DNA')
		elif i == 2 and outcome[0] != 'BREAST':
			outcome.append('DNA')
		elif i == 3 and outcome[0] != 'LUNG':
			outcome.append('DNA')
		elif i == 4 and outcome[0] != 'CRC':
			outcome.append('DNA')
		elif float(confidence) > 0.6:
			outcome.append(prediction)
		else:
			outcome.append('UNSURE')

	return response(outcome)

# return the prediction string
def response(outcome):
	if outcome[0] == 'UNSURE':
		return "Your input doesn't have enough information for a precise prediction."
	elif outcome[0] == '':
		return "Your input doesn't have enough information for the cancer site prediction."
	elif outcome[0] == 'OTHER':
		return "The cancer site is other than BREAST, LUNG, PROSTATE, CRC."
	elif outcome[0] == 'BEAST':
		return "The cancer site is BREAST. Estrogen receptor is ", str(outcome[1])," and progesterone receptor is ", str(outcome[2]), "."
	elif outcome[0] == 'LUNG':
		return "The cancer site is LUNG. Cancer cell type is ", str(outcome[3])
	elif outcome[0] == 'CRC':
		return "The cancer site is COLON or RECTUM. Carcinoembryonic antigen result is ", str(outcome[4])
	else:
		return "The cancer site is PROSTATE"

#return "The diagnosis is ", outcome[0], "Also, ", str(outcome[1:])
