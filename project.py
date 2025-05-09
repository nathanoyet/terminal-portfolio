"""
This is the main python file of the project that contains all the application 
logic in main() using the Portfolio class and functions defined in portfolio.py
"""

import portfolio

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
        portfolio_name = input(">> What would you like to name your portfolio: ")
        if len(portfolio_name.split()) < 1:
            print("\n! Please enter a valid portfolio name !\n")
        else:
            break

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
            break

    #create the portfolio project
    port = portfolio.Portfolio(cash)

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
            if (port.buy(buy_ticker, buy_quantity, market[buy_ticker])):
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
                if sell_ticker in port.portfolio:
                    break
                else:
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
                if (int(sell_quantity) > port.portfolio[sell_ticker]):
                    print(f"\n! You only have {port.portfolio[sell_ticker]} shares of {sell_ticker} to sell !")
                else:
                    sell_quantity = int(sell_quantity)
                    break
            #go back to the previous command prompt if specified by the user
            if go_back:
                continue
            #sell the given quantity of the stock. Print a success message and the cash balance
            port.sell(sell_ticker, sell_quantity, market[sell_ticker])
            print()
            print(f"> {sell_quantity} shares of {sell_ticker} successfully sold for ${sell_quantity * market[sell_ticker]:.2f} <".center(80, "-"))
            print()
            print(f"Your cash balance is ${port.get_cash():.2f}\n".center(80))
        elif command == "VIEW MARKET":
            #display the stocks available to be traded
            portfolio.view_market(market)
            print()
            print("> Market prices are updated after a command is entered <".center(80, "-"))
            print()
        elif command == "VIEW PORTFOLIO":
            #display the user's portfolio
            if len(port.portfolio) == 0:
                print("You have no stocks in your portfolio")
            else:
                port.view_portfolio(market)
            print()
        elif command == "VIEW TRADES":
            #display the user's trades
            if len(port.trades) == 0:
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
            #exit the program after printing a goodbye message and the portfolio return
            port.calculate_portfolio_value(market)
            portfolio_return = (((port.portfolio_value + port.get_cash()) - cash) / cash) * 100
            print("> Thank you for using the Terminal Portfolio Simulator <".center(80, "-"))
            print()
            print(f"Your {portfolio_name} portfolio returned {portfolio_return:.2f}%".center(80))
            quit()
        else:
            print("! Invalid Command - Please Try Again !\n")


if __name__ == "__main__":
    main()