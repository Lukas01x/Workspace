#!/usr/bin/env python3.6

import sys
import getopt
from convert_functions import *

#Main function: 
#Usage in cli- ./cli_converter --amount <float> --input_currency <currency symbol or 3 letter currency code> --output_currency (optional argument) <currency symbol or 3 letter currency code>
def main(argv):
	#Initialise agrument variables	
	input_amount=""
	input_cur=""
	output_cur=""
	#Get given arguments and assign them to variables
	#Wrong format of command or not giving arguments stops the process and print usage of command
	try:
		opts, args = getopt.getopt(argv,"ha:i:o:",["amount=","input_currency=","output_currency="])
	except getopt.GetoptError:
		print ('Usage of script:\ncurrconv.py -a <amount> -i <input currency> -o <output currency>\ncurrconv.py --amount <amount> --input_currency <input currency> --output_currency <output currency>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('currconv.py -a <amount> -i <input currency> -o <output currency>\ncurrconv.py --amount <amount> --input_currency <input currency> --output_currency <output currency>')
			sys.exit()
		elif opt in ("-a", "--amount"):
			try:
				input_amount = round(float(arg)	,2)
			except:
				print ('Usage of script:currconv.py -a <amount> -i <input currency> -o <output currency>\ncurrconv.py --amount <amount> --input_currency <input currency> --output_currency <output currency>')
				sys.exit(2)	
		elif opt in ("-i", "--input_currency"):
			input_cur = arg
		elif opt in ("-o", "--output_currency"):
			output_cur = arg

	#Get rates dictionary and set base
	rates = getRates('https://api.exchangeratesapi.io/latest')
	base = rates["EUR"]
	
	#Initialise dictionary for output data
	converted={}
	
	#Validate input arguments- returns 3 letters country code or error 
	input_validated = inputvalidation(input_cur,rates)
	output_validated = inputvalidation(output_cur, rates)

	#Check if there is an error in input arguments
	#If error occurs print an error
	if (("ERROR" in input_validated) | (input_validated == '')):
		print ("Input value-" + input_validated)
	elif ("ERROR" in output_validated):
		print ("Output value-" + output_validated)
	else:
		#Check if output currency argument is empty or not
		#If output currency argument is empty then convert it to given currency
		#If output currency argument is NOT empty then convert it to all available currencies
		if (output_validated != '') & (output_validated is not None):
			result = converter(input_amount, rates[input_validated], base, rates[output_validated])
			converted[output_validated]=result
		else:
			for curr_code in rates:
				if (curr_code != input_validated):
					result = converter(input_amount,rates[input_validated],base,rates[curr_code])
					converted[curr_code] = result
		#Build an output and print it
		output_data={"input": {"amount": input_amount,"currency": input_validated},"output": converted}
		print (json.dumps(output_data,sort_keys=True,indent=4))


#Execute main function
if __name__ == "__main__":
	main(sys.argv[1:])
