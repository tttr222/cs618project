CS618 Project
March 25 2016
Tung Tran
Xiaofei Zhang

Core Design
* The program will employ a client-server architecture.
* With the clientside interface, the user is able to submit a textual 
example to be classified.
* The client component will submit a request to the HTTP server, 
which will run an instance to classify the example text.
* The text will be a snippet phrase/sentence of a pathological 
report. The learning/classification component will diagnose the 
type of cancer and location site of cancer.
* The result will be returned to the user in the form of a 
natural language textual report.

Additional Design  
* If there is time, we will implement the following additional features:
	* Learning/classification workload is distributed over 
	  multiple worker nodes.
	* User of the tool is able to submit own training data. 

Technologies and Implementation Details
* Client-side GUI front-end will be implemented with HTML/CSS. 
* JavaScript with AJAX will be used to send HTTP requests to the server.
* The server will be implemented via Python 2.7 with a simple HTTP library.
* The core learning and classifying algorithm will be implemented with 
  the following libraries:
	* Natural Language Toolkit - nltk
	* Machine Learning Library - scikit-learn 

Prerequisites
* Install nltk - http://www.nltk.org/install.html
	* On linux, run sudo pip install nltk

* Install scikitlearn - http://scikit-learn.org/stable/install.html
	* On linux, run sudo pip install scikit-learn

* Might also need numpy, but that probably comes with scikit-learn 
