#response function
def response(outcome):
        if outcome[0] == 'UNSURE':
		return "Your input doesn't have enough information for a precise prediction."
	elif outcome[0] == '':
		return "Your input doesn't have enough information for the cancer site prediction."
#	elif outcome[0] == 'OTHER':
#		return "The report shows that the cancer site is other than BREAST, LUNG, PROSTATE, CRC."
	elif outcome[0] == 'BREAST':
		str1= "The report indicates the possibility of BREAST cancer. "
		if outcome[1] != 'UNSURE' and outcome[2] != 'UNSURE':
			str2="The report test "+ str(outcome[1]) + " for estrogen receptor and " + str(outcome[2]) + " for progesterone receptor."
		elif outcome[1] =='UNSURE' and outcome[2] != 'UNSURE': 
			str2="The report test "+ str(outcome[2]) + " for progesterone receptor. However, no precise prediction was made for estrogen receptor."
		elif outcome[1] !='UNSURE' and outcome[2] == 'UNSURE':
			str2="The report test "+ str(outcome[2]) + " for estrogen receptor. However, no precise prediction was made for progesterone receptor."
		else:
			str2="However, the information in you input is not enough for a precise hormone receptor status prediction."
		return str1 + str2
	elif outcome[0] == 'LUNG':
		str1= "The report indicates the possibility of LUNG cancer. "
		if outcome[3] == 'UNSURE':
			str2 = "No precise cell type prediction was made."
		elif outcome[3] == 'OTHER':
			str2 = "The report shows the cancer is neither squamous cell carcinoma nor adenocarcinoma."
		else: 
			str2 = "The report shows the cancer cell type is " + str(outcome[3]) + "."
		return str1 + str2
	elif outcome[0] == 'CRC':
		str1= "The report indicates the possibility of COLORECTAL cancer. "
		if outcome[4]=='UNSURE':
			str2="No precise prediction was made for carcinoembryonic antigen."
		else:
			str2-"The report shows the carcinoembryonic antigen status is " + str(outcome[4]) + "."
		return str1 + str2
	else:
		return "The report indicates the possibility of PROSTATE cancer. "

