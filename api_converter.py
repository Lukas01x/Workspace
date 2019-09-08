#!/usr/bin/env python3.6

import json
import requests
import flask
from flask import request, jsonify
from convert_functions import *

app = flask.Flask(__name__)
app.config["DEBUG"] = False


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
