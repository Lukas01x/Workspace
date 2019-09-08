#!/usr/bin/env python3.6

import sys
import getopt
import json
import requests
from babel import Locale
from babel.numbers import *


def getResponse(api_address):
    api_address=str(api_address)
    try:
        requestStatus = requests.get(api_address)
        return requestStatus
    except:
        return 'Connection error'



def inputvalidation(input_currency,rates_source):
	input_currency=str(input_currency)
	found = 0
	if (len(input_currency) == 1):
		for curr_code in rates_source:
			#cur_symbol=Locale('en', 'US').currency_symbols[curr_code]
			cur_symbol=get_currency_symbol(curr_code,locale='en_US.utf8')
			if(input_currency==cur_symbol):
				found = 1
				toCode=curr_code
				break
	elif (len(input_currency) == 3):
		for curr_code in rates_source:
			if(input_currency==curr_code):
				found = 1
				toCode = curr_code
				break
	else:
		found = 1
		if(input_currency == ''):
			toCode=''
		else:
			toCode = 'ERROR-bad input format'

	if(found==1):
		return toCode
	else:
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

def main(argv):
	input_amount=""
	input_cur=""
	output_cur=""
	try:
		opts, args = getopt.getopt(argv,"ha:i:o:",["amount=","input_currency=","output_currency="])
	except getopt.GetoptError:
		print ('Usage of script:')
		print ('currconv.py -a <amount> -i <input currency> -o <output currency>')
		print ('currconv.py --amount <amount> --input_currency <input currency> --output_currency <output currency>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('currconv.py -a <amount> -i <input currency> -o <output currency>')
			print ('currconv.py --amount <amount> --input_currency <input currency> --output_currency <output currency>')
			sys.exit()
		elif opt in ("-a", "--amount"):
			input_amount = float(arg)		
		elif opt in ("-i", "--input_currency"):
			input_cur = arg
		elif opt in ("-o", "--output_currency"):
			output_cur = arg


	rates = getRates('https://api.exchangeratesapi.io/latest')
	base = rates["EUR"]

	converted={}
	input_validated = inputvalidation(input_cur,rates)
	output_validated = inputvalidation(output_cur, rates)

	if (("ERROR" in input_validated) | (input_validated == '')):
		print ("Input value-" + input_validated)
	elif ("ERROR" in output_validated):
		print ("Output value-" + output_validated)
	else:
		if (output_validated != '') & (output_validated is not None) & ("ERROR" not in output_validated):
			result = converter(input_amount, rates[input_validated], base, rates[output_validated])
			converted[output_validated]=result
		else:
			for curr_code in rates:
				if (curr_code != input_validated):
					result = converter(input_amount,rates[input_validated],base,rates[curr_code])
					converted[curr_code] = result
		output_data={"input": {"amount": input_amount,"currency": input_validated},"output": converted}
		print (json.dumps(output_data,sort_keys=True,indent=4))



if __name__ == "__main__":
	main(sys.argv[1:])
