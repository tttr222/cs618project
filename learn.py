import nltk, csv
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer

# transforms text to a word frequency dictionary
def text2dict(text):
	tokens = nltk.word_tokenize(text)

	dictionary = {}
	for t in tokens:
		if not t.isalnum():
			continue
		t = t.lower()
		if t not in dictionary:
			dictionary[t] = 0
		dictionary[t] += 1

	return dictionary

# translate csv into rows
rows = []
with open('data/training_data.csv','r') as f:
	reader = csv.reader(f,delimiter=',', quotechar='"')
	for r in reader:
		rows.append(r)

# translate each row into an object
columns = []
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

dictlist = []
y = []

# concatenate text fields from objects, tokenize,
# create a list of word frequency dictionaries
# one for each row
for obj in data:
	text = ''
	for k in columns:
		if 'TEXT' in k:
			text += obj[k]
			
	dt = text2dict(text)
	
	dictlist.append(dt)
	y.append(obj['SITE_TYPE'])

# print out a sample dictionary for testing
print dictlist[0]

# convert the dictionaries into a matrix
dv = DictVectorizer()
X = dv.fit_transform(dictlist)

# fit the matrix to a model 
lr = LogisticRegression()
lr.fit(X,y)

# try to predict one example
test = "Gross Description.The specimen, labeled right breast ultrasound guided biopsy, received in.formalin, consists of a 1.8x1.0x0.3 cm aggregate of tan/pink fibroadipose breast.tissue cores which were placed in formalin at 11:55 am and are now submitted in.one cassette..HM/mbc Microscopic Description.Sections show a needle core biopsy in which there is extensive infiltrating and.in situ ductal adenocarcinoma. The tumor shows focal comedo necrosis in the in.situ tumor and a desmoplastic response in the fibrous connective tissue.intimately associated with the invasive carcinoma. The tumor is high-grade with.marked nuclear pleomorphism, single cell necrosis, prominent nucleoli and no.propensity to form tubules. Cancerization of lobules by the DCIS is noted. .Lymphvascular invasion is not identified.    .DGD/mbc .ADDITIONAL MICROSCOPIC DESCRIPTION: Immunohistochemistry for estrogen receptor.shows focal nuclear positivity in less than 5% of the tumor nuclei..Immunohistochemistry for progesterone receptor shows a similar approximately 5%.positivity in the tumor. There is very good staining of the adjacent normal.neoplastic breast tissue. All controls stain appropriately including external.positive, internal negative and external negative controls as required.   .**INITIALS"

ex = dv.transform(text2dict(test))
pd = lr.predict(ex)

print pd 
