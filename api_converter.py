#!/usr/bin/env python3.6

import flask
from flask import request, jsonify
from convert_functions import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Mapping/routing URL to function api_id
@app.route('/currency_converter', methods=['GET'])
def api_id():
	#Initialise argument variables
	currency_parameters = request.args
	
	#Check if given amount argument is float
	try:
		input_amount=round(float(currency_parameters.get('amount')),2)
	except:
		return ("input_amount-ERROR-bad input format")

	#Get rates dictionary and set base
	rates = getRates('https://api.exchangeratesapi.io/latest')
	base = rates["EUR"]

	#Validate input arguments- returns 3 letters country code or error 
	input_currency = inputvalidation(currency_parameters.get('input_currency'),rates)
	output_currency = inputvalidation(currency_parameters.get('output_currency'),rates)

	#Initialise dictionary for output data
	converted = {}

	#Check if there is an error in input arguments
	#If error occurs print an error
	if ("ERROR" in input_currency):
		return ("input_currency-" + input_currency)
	elif (input_currency == ''):
		return ("input_currency-ERROR-bad input format")
	else:
		#Check if output currency argument is empty or not
		#If output currency argument is empty then convert it to given currency
		#If output currency argument is NOT empty then convert it to all available currencies
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
		#Build an output and print it		
		output_data={"input": {"amount": input_amount,"currency": input_currency},"output": converted}
		return jsonify(output_data)


app.run()
