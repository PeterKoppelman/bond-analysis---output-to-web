# bond-analysis---output-to-web
Bond analysis with output to the web using Plotly dash


This system gets financial data from quandl, crunches some numbers and outputs data to the web using Plotly dash.

The data that is inputted from quandl is the following:
Freddie Mac (30-Year Fixed Rate Mortgage Average in the United States).
Wells Fargo Home Mortgage Loans: 
  a) Home Mortgage Loans: Purchase Rate, Conforming Loan, 30-Year Fixed Rate, Interest Rate. 
  b) Home Mortgage Loans: Purchase Rate, Jumbo Loan (Amounts that exceed conforming loan limits), 30-Year Fixed Rate, Interest Rate
Treasury Department Interest Rates and Futures. We want Treasury Yield Curve Rates.

You'll need a quandl authentication key for this. Instructions for this are in the auth_token.py file.

Once we have the data, numbers are crunched and output to the web.

This is the second set of programs using financial data from quandl. Each set of programs outputs data differently. The first 
set uses openpyxl to output data to Excel and code to send the excel workbooks to a distribution list. This uses Plotly dash to output to the web. These represent experiments in the best way to distribute data to the business/user community. While powerful tools exist in python, most of them do not dealwith data distribution.

If you have any questions or ideas on how to improve the code, please reach out to me. 
