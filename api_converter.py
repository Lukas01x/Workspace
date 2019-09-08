#!/usr/bin/env python3.6

import sys
import getopt
import json
import requests
import flask
from babel import Locale
from babel.numbers import *

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
		if((input_currency == '') | (input_currency == 'None')):
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
	amount=float(amount)
	result = ((output_currency / base) / input_currency) * amount
	return round(float(result),2)



@app.route('/currency_converter', methods=['GET'])
def api_id():
	
	currency_parameters = request.args

	rates = getRates('https://api.exchangeratesapi.io/latest')
	base = rates["EUR"]
	input_amountt = str(currency_parameters.get('amount'))
	if ((input_amountt != 'None') & (input_amountt != '')):
		input_amount = round(float(input_amountt),2)
	else:
		return ("input_amount-ERROR-bad input format")
	input_currency = inputvalidation(currency_parameters.get('input_currency'),rates)
	output_currency = inputvalidation(currency_parameters.get('output_currency'),rates)

	
	converted = {}
	if ("ERROR" in input_currency):
		return ("input_currency-" + input_currency)
	elif (input_currency == ''):
		return ("input_currency-ERROR-bad input format")
	else:
		if (output_currency != '') & ("ERROR" not in output_currency):
			result = converter(input_amount, rates[input_currency], base, rates[output_currency])
			converted[output_currency]=result
		elif ("ERROR" in output_currency):
			return ("output_currency-" + output_currency)
		else:
			for curr_code in rates:
				if (curr_code != input_currency):
					result = converter(input_amount,rates[input_currency],base,rates[curr_code])
					converted[curr_code] = result
		output_data={"input": {"amount": input_amount,"currency": input_currency},"output": converted}
		return jsonify(output_data)


app.run()
