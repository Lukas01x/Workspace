#!/usr/bin/env python3.6

import sys
import getopt
from convert_functions import *


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
