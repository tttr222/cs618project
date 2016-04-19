import nltk, csv, random, numpy
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD

# transforms text to a word frequency dictionary
def text2dict(text):
	sentences = text.split('.')
	tokens = []
	for s in sentences:
		tks = nltk.word_tokenize(s)

		# consider unigrams and 2-grams
		for i in range(len(tks)-1):
			tks.append(tks[i] + '' + tks[i+1])
			
		tokens += tks

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
# transform rows into objects
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
			# remove newline encoding
			obj[rows[0][k]] = r[k].replace('\\X0D\\\\X0A\\',' -- ').replace('.','. ')
		
		data.append(obj)

	return data
	
# create a list of word frequency dictionaries one for each row
def dictlist(data):
	dictlist = []

	for obj in data:
		text = ''
		# concatenate text fields from objects, tokenize
		for k in columns:
			if 'TEXT' in k:
				text += obj[k]
				
		dt = text2dict(text)
		
		dictlist.append(dt)
		
	return dictlist


# convert the dictionaries into a matrix
def dictionary(rows):
	dl = dictlist(rows2objects(rows))

	dv = DictVectorizer()
	dv.fit(dl)
	
	return dv

# take the objects and extract the target output label
# and return it as a vector 
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
		
		if obj['BREAST_ER'].strip() == '' or obj['BREAST_ER'] == 'OTHER':
			y1.append('NULL')
		else:
			y1.append(obj['BREAST_ER'])
		
		if obj['BREAST_PR'].strip() == '' or obj['BREAST_PR'] == 'OTHER':
			y2.append('NULL')
		else:
			y2.append(obj['BREAST_PR'])
		
		if obj['LUNG_CELLTYPE'].strip() == '' or obj['LUNG_CELLTYPE'] == 'OTHER':
			y3.append('NULL')
		else:
			y3.append(obj['LUNG_CELLTYPE'])
		
		if obj['CRC_CEA'].strip() == '' or obj['CRC_CEA'] == 'OTHER':
			y4.append('NULL')
		else:
			y4.append(obj['CRC_CEA'])
	
	return [y0, y1, y2, y3, y4]

# for testing the accuracy of the machine
def test():
	rows = []
	with open('data/training_data.csv','r') as f:
		reader = csv.reader(f,delimiter=',', quotechar='"')
		for r in reader:
			rows.append(r)
			
	dv = dictionary(rows)

	# split the dataset into training and testing examples
	# the ratio will be 70:30 training to testing
	header = rows[0]
	rows = rows[1:]
	random.shuffle(rows)
	l = len(rows)
	
	rowTrain = rows[:int(l*0.7)]
	rowTrain.insert(0,header)
	rowTest = rows[int(l*0.7):]
	rowTest.insert(0,header)
	
	# transform the rows into objects, and then to matrix
	# additionally extract y labels
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
		yCurrentLevel = numpy.array(eyTrain[i])
		idx = numpy.where(yCurrentLevel != 'NULL')[0]
		lrx = LogisticRegression()
		lrx.fit(XTrain[idx],yCurrentLevel[idx])
		lr.append(lrx)
	
	#print zip(lr[0].predict(XTest),lr[0].predict_proba(XTest))
	print len(rowTrain), len(rowTest)
	print "Training Size is", XTrain.shape
	print "Testing Size is", XTest.shape
	print "Row length is", len(rows)

	levels = ['SITE_TYPE', 'BREAST_ER', 'BREAST_PR','LUNG_CELLTYPE','CRC_CEA']
	
	for i in range(5):
		yCurrentLevel = numpy.array(eyTest[i])
		#print yCurrentLevel
		idx = numpy.where(yCurrentLevel != 'NULL')[0]
		#print idx
		X = XTest[idx]
		y = yCurrentLevel[idx]
		score = lr[i].score(X,y)
		print "Score for",levels[i],"of shape",X.shape,"is", score

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
			outcome.append('NULL')
		elif i == 2 and outcome[0] != 'BREAST':
			outcome.append('NULL')
		elif i == 3 and outcome[0] != 'LUNG':
			outcome.append('NULL')
		elif i == 4 and outcome[0] != 'CRC':
			outcome.append('NULL')
		elif float(confidence) > 0.6:
			outcome.append(prediction)
		else:
			outcome.append('UNSURE')

	return response(outcome)
	
def response(outcome):
	return "The diagnosis is ", outcome[0], "Also, ", str(outcome[1:])

# The specimen, labeled right breast ultrasound guided biopsy, received in formalin, consists of a 1.8x1.0x0.3 cm aggregate of tan/pink fibroadipose breast tissue cores which were placed in formalin at 11:55 am and are now submitted in one cassette. HM/mbc Microscopic Description. Sections show a needle core biopsy in which there is extensive infiltrating and in situ ductal adenocarcinoma. The tumor is high-grade with marked nuclear pleomorphism, single cell necrosis, prominent nucleoli and no propensity to form tubules. Cancerization of lobules by the DCIS is noted. Lymphvascular invasion is not identified.
