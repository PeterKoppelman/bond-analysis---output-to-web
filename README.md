# bond-analysis---output-to-web
Bond analysis with output to the web using Plotly dash

The following python libraries are being used:
certifi              2019.11.28
chardet              3.0.4
click                7.1.1
cycler               0.10.0
dash                 1.9.1
dash-core-components 1.8.1
dash-html-components 1.0.2
dash-renderer        1.2.4
dash-table           4.6.1
et-xmlfile           1.0.1
Flask                1.1.1
Flask-Compress       1.4.0
future               0.18.2
idna                 2.9
inflection           0.3.1
itsdangerous         1.1.0
jdcal                1.4.1
Jinja2               2.11.1
kiwisolver           1.1.0
MarkupSafe           1.1.1
matplotlib           3.2.1
more-itertools       8.2.0
numpy                1.18.1
openpyxl             3.0.3
pandas               1.0.1
pip                  20.0.2
plotly               4.5.4
pyparsing            2.4.6
python-dateutil      2.8.1
pytz                 2019.3
pywin32              227
Quandl               3.5.0
requests             2.23.0
retrying             1.3.3
scipy                1.4.1
seaborn              0.10.0
setuptools           41.2.0
six                  1.14.0
urllib3              1.25.8
Werkzeug             1.0.0


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
