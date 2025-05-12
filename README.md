** PROJECT DESCRIPTION **

This program allows the user to simulate a trading portfolio in the command line terminal.
Users can only trade stocks that are in a pre-defined list of 10 stocks.

The user begins by giving a name to their portfolio and specifying how much cash they want
to begin with. The cash entered by the user should be a maximum of $10,000.

The user can then enter one of nine commands to manage their portfolio, view specific data
and navigate through application. A description of each of the commands is provided below:

- BUY
Allows a user to specify the ticker symbol and quantity of the stock they would like buy. 
The stock will be purchased at the current market price. The user's cash balance should be 
sufficient to complete the purchase.

- SELL
Allows a user to specify the ticker symbol and quantity of the stock they would like to sell.
Only stocks currently held in the user's portfolio can be sold. Stocks are sold at the 
prevailing market price at the time of sale. The proceeds of the sale are added to the user's 
cash balance.

- VIEW PRICE
Allows a user to view the current price of a particular stock

- VIEW MARKET
Displays a list of all the stocks and their current market prices.

- VIEW PORTFOLIO
Displays the user's stock portfolio which includes the stock ticker, the quantity held, and 
the current market value for each stock. The total portfolio value is also displayed.

- VIEW TRADES
Displays details on the user's trades. Details include a timestamp, the ticker of the stock 
traded, the action (buy or sell), the quantity traded and the trade amount in $.

- VIEW CASH
Displays the user's current cash balance

- VIEW COMMANDS
Displays the list of commands

- VIEW BACK
Takes the user to the previous command prompt. If the user is at the base command prompt,
they cannot go back any further. 

- EXIT
Prints a goodbye message and the portfolio return. The program is then exited. 
