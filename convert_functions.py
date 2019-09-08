import json
import requests
from babel import Locale
from babel.numbers import *
from babel import Locale

def getResponse(api_address):
    api_address=str(api_address)
    try:
        requestStatus = requests.get(api_address)
        return requestStatus
    except:
        return 'Connection error'



def inputvalidation(input_currency,rates_source):
	input_currency=str(input_currency)
	if (len(input_currency) == 1):
		for curr_code in rates_source:
			cur_symbol=get_currency_symbol(curr_code,locale='en_US.utf8')
			if(input_currency==cur_symbol):
				toCode=curr_code
				return toCode				
	elif (len(input_currency) == 3):
		for curr_code in rates_source:
			if(input_currency==curr_code):
				toCode = curr_code
				return toCode				
	else:
		if((input_currency == '') | (input_currency == 'None')):
			return ''
		else:
			return 'ERROR-bad input format'

	return 'ERROR-unknown currency symbol/code'

def getRates(api):
	requestStatus=getResponse(api)
	if(str(requestStatus) == '<Response [200]>'):
		request = requestStatus.json()
		rates = request["rates"]
		rates["EUR"] = float(1)
		request["rates"]=rates
		with open('data.json', 'w') as outfile:
				json.dump(request, outfile)
	else:
		with open('data.json', 'r') as f:
			curencies_file = json.load(f)
		rates = curencies_file["rates"]

	return rates

def converter(amount,input_currency,base,output_currency=None):
	result = ((output_currency / base) / input_currency) * amount
	return round(float(result),2)
