Console utilities:
1. Main:- show data from PrivatBankAPI about exchange rate for 0-10 days.
In cmd - python main.py 'days' GBF CHF ...- 
0<days<10, 'GBP'- currency. 
Available currencies : 'USD', 'EUR', 'CHF', 'GBP', 'PLN', 'SEK', 'XAU', 'CAD' , CZK, CHF
For example: 'python main.py 3 GBP CZK PLN CHF'
2. Server chat - allow to show exchange rate for request 
For chat request about exchange rate should be entered in the form: 
"exchange 2", 
where 2 - quantity days for request , it is number between 0 and 10 