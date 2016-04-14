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
		
		if obj['BREAST_ER'] == '':
			y1.append(obj['BREAST_ER'])
		else:
			y1.append('Null')
		
		if obj['BREAST_PR'] == '':
			y2.append(obj['BREAST_PR'])
		else:
			y2.append('Null')
		
		if obj['LUNG_CELLTYPE'] == '':
			y3.append(obj['LUNG_CELLTYPE'])
		else:
			y3.append('Null')
		
		if obj['CRC_CEA'] == '':
			y4.append(obj['CRC_CEA'])
		else:
			y4.append('Null')
	
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

	X, y, dv = format(rows)

	# fit the matrix to a model 
	lr = LogisticRegression()
	lr.fit(X,y)

	# try to predict one example
	#test = "Gross Description.The specimen, labeled right breast ultrasound guided biopsy, received in.formalin, consists of a 1.8x1.0x0.3 cm aggregate of tan/pink fibroadipose breast.tissue cores which were placed in formalin at 11:55 am and are now submitted in.one cassette..HM/mbc Microscopic Description.Sections show a needle core biopsy in which there is extensive infiltrating and.in situ ductal adenocarcinoma. The tumor shows focal comedo necrosis in the in.situ tumor and a desmoplastic response in the fibrous connective tissue.intimately associated with the invasive carcinoma. The tumor is high-grade with.marked nuclear pleomorphism, single cell necrosis, prominent nucleoli and no.propensity to form tubules. Cancerization of lobules by the DCIS is noted. .Lymphvascular invasion is not identified.    .DGD/mbc .ADDITIONAL MICROSCOPIC DESCRIPTION: Immunohistochemistry for estrogen receptor.shows focal nuclear positivity in less than 5% of the tumor nuclei..Immunohistochemistry for progesterone receptor shows a similar approximately 5%.positivity in the tumor. There is very good staining of the adjacent normal.neoplastic breast tissue. All controls stain appropriately including external.positive, internal negative and external negative controls as required.   .**INITIALS"

	ex = dv.transform(text2dict(query))
	pd = lr.predict(ex)

	return pd
