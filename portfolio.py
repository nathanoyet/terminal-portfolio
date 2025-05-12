"""
This python file includes the Portfolio class which is used to create and modify a user's portfolio
This file also contains global functions that are used in project.py
"""

from datetime import datetime
import time
import random
import csv

class Portfolio:
    def __init__(self, cash, port_file):
        """This function initialises a 2 dictionaries that will store a portfolio of 
        stocks and all trades made. The starting cash balance provided by the user is
        also stored
        """
        self.cash = cash
        self.portfolio_value = 0

    def buy(self, ticker, quantity, price, port_file):
        """
        This function adds a newly purchased stock to the portfolio or increases its
        quantity if the stock is already in the portfolio
        """
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        buy_amount = quantity * price
        if (buy_amount > self.cash):
            return False
        else:
            #check whether the ticker is in the portfolio
            ticker_present = False
            temp = []
            with open(port_file, "r") as port_csv:
                port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
                for row in port_dict:
                    if row["ticker"] == ticker:
                        ticker_present = True
                        row["quantity"] = int(row["quantity"]) + quantity
                    temp.append(row)

            if ticker_present:
                #re-open the csv in write mode to overwrite it with the updated quantity
                with open(port_file, "w", newline='') as port_csv:
                    port_dict = csv.DictWriter(port_csv, fieldnames = ["ticker", "quantity"])
                    port_dict.writerows(temp)
            else:
                #re-open the csv in append mode to insert the new ticker and its quantity
                with open(port_file, "a") as port_csv:
                    port_dict = csv.DictWriter(port_csv, fieldnames = ["ticker", "quantity"])
                    port_dict.writerow({"ticker" : ticker, "quantity" : quantity})
            
            #reduce the cash balance by the order value
            self.cash -= buy_amount

            #record the trade in trades.csv
            with open("trades.csv", "a") as trades_csv:
                trades_dict = csv.DictWriter(trades_csv, fieldnames = ["timestamp", "ticker", "action", "quantity", "amount"])
                trades_dict.writerow({"timestamp":timestamp, "ticker":ticker, "action":"BUY", "quantity":quantity, "amount":buy_amount})
            self.trades[timestamp] = [ticker, quantity, buy_amount, "BUY"]
            return True

    def sell(self, ticker, quantity, price, port_file):
        """
        This function reduces the quantity of a stock when sold, and adds to the 
        cash balance
        """
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        sell_amount = quantity * price

        #clone the csv data and modify the quantity
        temp = []
        with open(port_file, "r") as port_csv:
            port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
            for row in port_dict:
                if row["ticker"] == ticker:
                    row["quantity"] = int(row["quantity"]) - quantity
                temp.append(row)

        #re-open the csv in write mode and overwrite it with the updated quantity
        with open(port_file, "w", newline='') as port_csv:
            port_dict = csv.DictWriter(port_csv, fieldnames = ["ticker", "quantity"])
            port_dict.writerows(temp)

        #add the proceeds from the sale to the cash balance
        self.cash += sell_amount
        
        #delete stock from portfolio csv if its quantity becomes zero
        temp = []
        with open(port_file, "r") as port_csv:
            port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
            for row in port_dict:
                if row["quantity"] != 0:
                    temp.append(row)
        with open(port_file, "w", newline='') as port_csv:
            port_dict = csv.DictWriter(port_csv, fieldnames=["ticker", "quantity"])
            port_dict.writerows(temp)

        #record the sell in trades.csv
        with open("trades.csv", "a") as trades_csv:
            trades_dict = csv.DictWriter(trades_csv, fieldnames = ["timestamp", "ticker", "action", "quantity", "amount"])
            trades_dict.writerow({"timestamp":timestamp, "ticker":ticker, "action":"SELL", "quantity":quantity, "amount":sell_amount})

    def get_cash(self):
        """
        This function returns the cash balance
        """
        return self.cash
    
    def calculate_portfolio_value(self, market, port_file):
        """
        This function calculates the total value of all stocks in the portfolio
        """
        portfolio_value = 0
        with open(port_file, "r") as port_csv:
            port_dict = csv.DictReader(port_csv, fieldnames=["ticker", "quantity"])
            for row in port_dict:
                portfolio_value += (market[row["ticker"]]) * int(row["quantity"])
        self.portfolio_value = portfolio_value

    def display_portfolio_value(self, market, port_file):
        """
        This function prints the portfolio value
        """
        self.calculate_portfolio_value(market, port_file)
        print()
        print(" " * 18, "-" * 38)
        print(" " * 20, end="")
        print("Portfolio Value", " " * 10, end="")
        print(f"${self.portfolio_value:.2f}".rjust(10))
        print(" " * 18, "-" * 38)
    
    def view_portfolio(self, market, port_file):
        """
        This function displays the current portfolio
        """
        position_index = 1
        print(" " * 18, "-" * 38)
        print(" " * 20, end="")
        print("Ticker", " " * 5, end="")
        print("Quantity", " " * 4, end="")
        print("Market Value")
        print(" " * 18, "-" * 38)

        with open(port_file, "r") as port_csv:
            port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
            for row in port_dict:
                if int(row["quantity"]) > 0:
                    print(" " * 20, end="")
                    print(f"{position_index}. ", end="")
                    print(f"{row["ticker"]}", end="")
                    print(f"{row["quantity"]}".rjust(10), end="")
                    print(" " * 9, end="")
                    print(f"${(market[row["ticker"]] * int(row["quantity"])):.2f}".rjust(10))
                    position_index += 1
        self.display_portfolio_value(market, port_file)

    def view_trades(self):
        """
        This function displays all trades made
        """
        print(" " * 2, "-" * 74)
        print(" " * 3, end="")
        print("Timestamp", " " * 15, end="")
        print("Ticker", " " * 5, end="")
        print("Action", " " * 5, end="")
        print("Quantity", " " * 4, end="")
        print("Trade Amount")
        print(" " * 2, "-" * 74)
        #copy the trades from trades.csv into a list
        trades = []
        with open("trades.csv", "r") as trades_csv:
            trades_dict = csv.DictReader(trades_csv, fieldnames = ["timestamp", "ticker", "action", "quantity", "amount"])
            for row in trades_dict:
                trades.append(row)
        for trade in trades:   
            print(" " * 3, end="")
            print(f"{trade["timestamp"]}", " " * 6, end="")
            print(f"{trade["ticker"]}", " " * 5, end="")
            print(f"{trade["action"]}".center(8), end="")
            print(f"{trade["quantity"]}".rjust(10), " " * 8, end="")
            print(f"${float(trade["amount"]):.2f}".rjust(10))


def refresh_prices(market):
    """
    This transaction randomises changes in the market prices of each stock to simulate
    fluctuations in stock prices
    """
    for stock in market:
        price_change = random.uniform(0.01, 0.10)
        change_direction = random.randint(1, 2)
        if change_direction == 1:
            market[stock] = market[stock] * (1 + price_change)
        else:
            market[stock] = market[stock] * (1 - price_change)


def view_market(market):
    """ 
    This function displays the stocks available for trading along with their market 
    prices
    """
    print(" " * 20, "-" * 30)
    print(" " * 21, "Stock", " " * 9, end="")
    print("Current Price")
    print(" " * 20, "-" * 30)
    for stock in market:
        time.sleep(0.05)
        print(" " * 22, end="")
        print(f"{stock}", end="")
        print(" " * 12, end="")
        print(f"${market[stock]:.2f}".rjust(10))


def list_commands(portfolio_name):
    """
    This function list all the commands that can be executed 
    """
    print(f"\nManage your {portfolio_name} portfolio by entering one of the following commands:\n")
    time.sleep(0.05)
    print("1.  BUY              -> Buy a stock at the market price")
    time.sleep(0.05)
    print("2.  SELL             -> Sell a stock at a given price")
    time.sleep(0.05)
    print("3.  VIEW PRICE       -> View the current price of a particular stock")
    time.sleep(0.05)
    print("4.  VIEW MARKET      -> View the current prices of all available stocks")
    time.sleep(0.05)
    print("5.  VIEW PORTFOLIO   -> View the stocks in your portfolio")
    time.sleep(0.05)
    print("6.  VIEW TRADES      -> View your trading history")
    time.sleep(0.05)
    print("7.  VIEW CASH        -> View your available cash balance")
    time.sleep(0.05)
    print("8.  VIEW COMMANDS    -> View the list of available commands")
    time.sleep(0.05)
    print("9.  BACK             -> Go back to the previous command prompt")
    time.sleep(0.05)
    print("10. EXIT             -> Exit the program\n")


if __name__ == "__main__":
    pass