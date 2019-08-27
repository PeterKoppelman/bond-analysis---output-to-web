import datetime

# The auth_key is the quandl key that is used to get data. You will need to
# sign up at quandl.com. The libraries that you will be using free. 
# Check on the free filter and the real estate asset class to get the first three libaraies. 
# You need the following data:
# 	1) Freddie Mac (30-Year Fixed Rate Mortgage Average in the United States). 
#	   Click on Libraries: Python
# 	2) Wells Fargo Home Mortgage Loans:
#		a) Home Mortgage Loans: Purchase Rate, Conforming Loan, 30-Year Fixed Rate, Interest Rate.
#		Click on libraries: Python
# 	3) Wells Fargo Home Mortgage Loans:
#		a) Home Mortgage Loans: Purchase Rate, Jumbo Loan (Amounts that exceed conforming loan limits), 30-Year Fixed Rate, Interest Rate
#		Click on libraries: Python
# For the last two libraries, we're going to get data from the Treasury Department. The asset class for this is
# Interest Rates and Futures. We want Treasury Yield Curve Rates. The library is Python. We'll get daily data
# and the delta (difference) between rates from one day to another. We get the differernce
# by using transform = diff when we grab the data.
auth_key = " "
if auth_key == " ":
	print('The quandl authentication key is blank. Please read the instructions in auth_token.py and get a key')
	exit()

# names of the  type of curve and the formal name of the quandl file.
sql_name = {'yield_curve' : "USTREASURY/YIELD", 'freddie' : "FMAC/30US", 'conforming' : "WFC/PR_CON_30YFIXED_IR",
			'jumbo' : "WFC/PR_JUMBO_30YFIXED_IR"}

# Names and percentage space for the dash datatable fields for the yield curve datatable
col_dict = {'Date': '12%', '1 MO': '8%', '3 MO': '8%', '6 MO': '8%',
            '1 YR': '8%', '2 YR': '8%', '3 YR': '8%', '5 YR': '8%', 
            '7 YR': '8%', '10 YR': '8%', '20 YR': '8%', '30 YR': '8%'}

# Name of the jumbo pickle file
last_pickle_file = 'jumbo.pickle'