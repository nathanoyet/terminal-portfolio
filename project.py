"""
This is the main python file of the project. It contains all the application logic
in main() that utilises the Portfolio class and functions defined in portfolio.py

This is the main file that should be run via "python3 project.py"
"""

import portfolio
import csv

def main():
    #initialise the list of tradeable stocks and their market prices
    market = {
        "AAPL" : 30,
        "AMZN" : 13,
        "GOOG" : 17,
        "NFLX" : 19,
        "TSLA" : 8,
        "NVDA" : 29,
        "META" : 11,
        "MSFT" : 6,
        "ADBE" : 21,
        "COST" : 4
    }

    #print welcome message and prompt the user for a valid portfolio name
    print("-" * 80)
    print(" " * 20 + "Welcome to the Terminal Portfolio Simulator")
    print("-" * 80)
    print()
    while True:
        user_status = input(">> Are you a new user [YES|NO]: ").upper()
        new_user = True
        if user_status == "YES":
            while True:
                portfolio_name = input("\n>> What would you like to name your portfolio? ")
                if len(portfolio_name.split()) < 1:
                    print("\n! Please enter a valid portfolio name !\n")
                    continue
                if (portfolio_name.isalpha() == False):
                    print("\n! Please enter only alphabetical characters with no spaces !")
                else:
                    break
            port_file = f"{portfolio_name}" + ".csv"
            with open(port_file, "w", newline='') as port_csv:
                port_dict = csv.DictWriter(port_csv, fieldnames = ["ticker", "quantity"])
                break
        elif user_status == "NO":
            new_user = False
            while True:
                portfolio_name = input("\n>> Please enter your portfolio name: ").lower()
                if len(portfolio_name.split()) < 1:
                    print("\n! Please enter a valid portfolio name !")
                else:
                    port_file = f"{portfolio_name}" + ".csv"
                    try:
                        with open(port_file, "r") as port_csv:
                            break
                    except FileNotFoundError:
                        print(f"\n! {portfolio_name} does not exist. Please enter your correct portfolio name !")
            break
        else:
            print("\n! Invalid Command - Please Try Again !\n")

    if new_user:
        while True:
            #prompt user for the starting cash balance
            cash = input("\n>> Enter starting cash ($): ")
            if (cash.isdigit() == False):
                print("\n! Invalid Cash Amount Entered - Please Try Again !")
                continue
            if float(cash) <= 0:
                print("\n! Invalid Cash Amount Entered - Please Try Again !")
                continue
            if float(cash) > 10000:
                print("\n! Max starting cash allowed is $10,000 !")
                continue
            else:
                cash = float(cash)
                #store the new user's cash balance in cash.csv
                with open("cash.csv", "w") as cash_csv:
                    cash_dict = csv.DictWriter(cash_csv, fieldnames = ["balance"])
                    cash_dict.writerow({"balance" : cash})
                #create a trades.csv file to store trade history
                with open("trades.csv", "w", newline='') as trades_csv:
                    pass
                break
    else:
        try:
            #retrieve the returning user's cash balance from the cash.csv
            with open("cash.csv", "r") as cash_csv:
                cash_dict = csv.DictReader(cash_csv, fieldnames = ["balance"])
                for row in cash_dict:
                    cash = float(row["balance"])
            #print a welcome back message
            print()
            print(f"> Welcome back to your {portfolio_name} portfolio <".center(80, "-"))
        except FileNotFoundError:
            #alert the user that their cash balance cannot be found
            print("\n! Your cash balance cannot be found !")
            #proceed to prompt them for a starting cash balance
            while True:
                cash = input("\n>> Enter starting cash ($): ")
                if (cash.isdigit() == False):
                    print("\n! Invalid Cash Amount Entered - Please Try Again !")
                    continue
                if float(cash) <= 0:
                    print("\n! Invalid Cash Amount Entered - Please Try Again !")
                    continue
                if float(cash) > 10000:
                    print("\n! Max starting cash allowed is $10,000 !")
                    continue
                else:
                    cash = float(cash)
                    #store the new user's cash balance in cash.csv
                    with open("cash.csv", "w") as cash_csv:
                        cash_dict = csv.DictWriter(cash_csv, fieldnames = ["balance"])
                        cash_dict.writerow({"balance" : cash})
                    break
            #print a welcome back message
            print()
            print(f"> Welcome back to your {portfolio_name} portfolio <".center(80, "-"))

    #create the portfolio project
    port = portfolio.Portfolio(cash, port_file)

    #display available stocks
    print("\nBelow is the list of stocks available for trading:\n")
    portfolio.view_market(market)
    portfolio.list_commands(portfolio_name)

    #main program loop
    while True:
        portfolio.refresh_prices(market)
        command = input(">> Enter a command: ")
        command = command.upper()
        print()
        if command == "BUY":
            go_back = False
            while True:
                #prompt user for valid ticker of stock to be bought
                buy_ticker = input(">> Enter the ticker of the stock you would like to buy: ").upper()
                if buy_ticker in market:
                    break
                else:
                    #check if user wants to go back to the previous command prompt
                    if buy_ticker == "BACK":
                        go_back = True
                        print()
                        break
                    print("\n! Please enter a valid ticker !\n")
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            while True:
                #prompt user for quantity to be bought
                buy_quantity = input(f"\n>> How many shares of {buy_ticker} would you like to buy: ")
                #check if user wants to go back to the previous command prompt
                if (buy_quantity.upper() == "BACK"):
                    go_back = True
                    print()
                    break
                #validate quantity
                if (buy_quantity.isdigit() == False):
                    print("\n! Please enter a valid quantity !")
                    continue
                if (int(buy_quantity) <= 0):
                    print("\n! Please enter a valid quantity !")
                else:
                    buy_quantity = int(buy_quantity)
                    break
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            #if the cash balance is sufficient, buy the stock. Print a success message and the cash balance
            if (port.buy(buy_ticker, buy_quantity, market[buy_ticker], port_file)):
                print()
                print(f"> {buy_quantity} shares of {buy_ticker} successfully purchased for ${(buy_quantity * market[buy_ticker]):.2f} <".center(80, "-"))
                print()
                print(f"Your cash balance is ${port.get_cash():.2f}\n".center(80))
            else:
                print(f"\n! Unfortunately, you have insufficient funds to buy {buy_quantity} shares of {buy_ticker} !\n")
        elif command == "SELL":
            go_back = False
            while True:
                #prompt user for ticker of stock to be sold and verify that its in the portfolio
                sell_ticker = input(">> Enter the ticker of the stock you would like to sell: ").upper()
                ticker_present = False
                with open(port_file, "r") as port_csv:
                    port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
                    for row in port_dict:
                        if row["ticker"] == sell_ticker:
                            ticker_present = True
                            break
                if ticker_present:
                    break
                #check if user wants to go back to the previous command prompt
                if (sell_ticker == "BACK"):
                    go_back = True
                    print()
                    break
                #validate ticker
                if (sell_ticker.isdigit() == True or len(sell_ticker.split()) != 1):
                    print(f"\n! Please provide a valid ticker !\n")
                else:
                    print(f"\n! You don't own any {sell_ticker} !\n")
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            while True:
                #prompt user for quantity to be sold
                sell_quantity = input(f"\n>> How many shares of {sell_ticker} would you like to sell: ")
                #check if user wants to go back to the previous command prompt
                if (sell_quantity.upper() == "BACK"):
                    go_back = True
                    print()
                    break
                #validate quantity
                if (sell_quantity.isdigit() == False):
                    print("\n! Please enter a valid quantity !")
                    continue
                if (int(sell_quantity) <= 0):
                    print("\n! Please enter a valid quantity !")
                    continue
                #check if portfolio holds adequate stock to sell
                with open(port_file, "r") as port_csv:
                    port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
                    for row in port_dict:
                        if row["ticker"] == sell_ticker:
                            current_quantity = int(row["quantity"])
                            break
                if (int(sell_quantity) > current_quantity): 
                    print(f"\n! You only have {current_quantity} shares of {sell_ticker} to sell !")
                else:
                    sell_quantity = int(sell_quantity)
                    break
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            #sell the given quantity of the stock. Print a success message and the cash balance
            port.sell(sell_ticker, sell_quantity, market[sell_ticker], port_file)
            print()
            print(f"> {sell_quantity} shares of {sell_ticker} successfully sold for ${sell_quantity * market[sell_ticker]:.2f} <".center(80, "-"))
            print()
            print(f"Your cash balance is ${port.get_cash():.2f}\n".center(80))
        elif command == "VIEW PRICE":
            go_back = False
            while True:
                #prompt user for valid ticker of stock
                view_ticker = input(">> Enter stock ticker: ").upper()
                if view_ticker in market:
                    break
                else:
                    #check if user wants to go back to the previous command prompt
                    if view_ticker == "BACK":
                        go_back = True
                        print()
                        break
                    print("\n! Please enter a valid ticker !\n")
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            #display the stock ticker's current price
            print()
            print(f"> {view_ticker}'s current stock price is ${market[view_ticker]:.2f} <".center(80, "-"))
            print()
        elif command == "VIEW MARKET":
            #display the stocks available to be traded
            portfolio.view_market(market)
            print()
            print("> Market prices are updated after a command is entered <".center(80, "-"))
            print()
        elif command == "VIEW PORTFOLIO":
            #display the user's portfolio
            portfolio_quantity = 0
            with open(port_file, "r") as port_csv:
                port_dict = csv.DictReader(port_csv, fieldnames = ["ticker", "quantity"])
                for row in port_dict:
                    portfolio_quantity += int(row["quantity"])
            if portfolio_quantity == 0:
                print("You have no stocks in your portfolio")
            else:
                port.view_portfolio(market, port_file)
            print()
        elif command == "VIEW TRADES":
            #display the user's trades
            trades = []
            with open("trades.csv", "r") as trades_csv:
                trades_dict = csv.DictReader(trades_csv, fieldnames = ["timestamp", "ticker", "action", "quantity", "amount"])
                for row in trades_dict:
                    trades.append(row)
            if len(trades) == 0:
                print("You have no trades")
            else:
                port.view_trades()
            print()
        elif command == "VIEW CASH":
            #display the user's cash balance
            print(f"> Your cash balance is ${port.get_cash():.2f} <".center(80, "-"))
            print()
        elif command == "VIEW COMMANDS":
            #display the list of valild program commands
            portfolio.list_commands(portfolio_name)
        elif command == "BACK":
            print("! You are already at the base command prompt !\n")
        elif command == "EXIT":
            #store the user's cash balance in cash.csv
            with open("cash.csv", "w") as cash_csv:
                cash_dict = csv.DictWriter(cash_csv, fieldnames=["balance"])
                cash_dict.writerow({"balance" : port.cash})
            #exit the program after printing a goodbye message and the portfolio return
            port.calculate_portfolio_value(market, port_file)
            portfolio_return = (((port.portfolio_value + port.get_cash()) - cash) / cash) * 100
            print("> Thank you for using the Terminal Portfolio Simulator <".center(80, "-"))
            print()
            print(f"Your {portfolio_name} portfolio returned {portfolio_return:.2f}%".center(80))
            quit()
        else:
            print("! Invalid Command - Please Try Again !\n")


if __name__ == "__main__":
    main()