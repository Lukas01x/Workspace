import json
import requests
from babel import Locale
from babel.numbers import *
from babel import Locale

#Function to get rates from API
#Arguments- api_address<string>
#Returns request or error
def getResponse(api_address):
    api_address=str(api_address)
    try:
        requestStatus = requests.get(api_address)
        return requestStatus
    except:
        return 'Connection error'

#Function to get rates from local file or from online API
#Arguments- api_address<string>
#Returns rates dictionary
def getRates(api):
	requestStatus=getResponse(api)
	#If response is successfull, overwrite local data file with new rates and use current rates 
	if(str(requestStatus) == '<Response [200]>'):
		request = requestStatus.json()
		rates = request["rates"]
		rates["EUR"] = float(1)
		request["rates"]=rates
		with open('data.json', 'w') as outfile:
				json.dump(request, outfile)
	#If response is unsuccessfull, use local data file with rates 
	else:
		with open('data.json', 'r') as f:
			curencies_file = json.load(f)
		rates = curencies_file["rates"]

	return rates

#Funtction to check inputs agains rates dictionary
#Arguments- api_address<string>,rates_source<dictionary>
#Returns empty string, 3 letters country code or error
def inputvalidation(input_currency,rates_source):
	input_currency=str(input_currency)
	#If its 1 letter input, check if its symbol of available currency, then convert it to 3 ltters country code
	if (len(input_currency) == 1):
		for curr_code in rates_source:
			cur_symbol=get_currency_symbol(curr_code,locale='en_US.utf8')
			if(input_currency==cur_symbol):
				return curr_code
	#If its 3 letters input, check if its available currency country code			
	elif (len(input_currency) == 3):
		for curr_code in rates_source:
			if(input_currency==curr_code):
				return curr_code
	#If empty, return empty string				
	else:
		if((input_currency == '') | (input_currency == 'None')):
			return ''
		else:
			return 'ERROR-bad input format'
	#If nothing passes return error
	return 'ERROR-unknown currency symbol/code'


#Function which convert currencies
#Arguments- amount<float>,input_currency<3 letters country code>,base<3 letters country code>,output_currency<3 letters country code>
#Returns converted currency
def converter(amount,input_currency,base,output_currency):
	result = ((output_currency / base) / input_currency) * amount
	return round(float(result),2)
