#Imports
from bs4 import BeautifulSoup
from colorama import Fore as F
from time import sleep
import requests
import webbrowser
import pandas
import functools
import subprocess
import geoip2.database
#Uses Maxmind GeoLite2-City Database for IP Location

#Compatible with most *nix systems only.  Please leave feedback if compatability for Windows is wanted.
#Should I make a function to check internet connection or just let an error arise?
#Beginning of program messages
print("""
 \033[32m /$$$$$$ 
 /$$__  $$
| $$  \__/
|  $$$$$$ \033[34m_____             ______         
 \033[32m\____  $$\033[34m__  /________________  /_________
 \033[32m/$$  \ $$\033[34m_  __/  __ \_  __ \_  //_/_  ___/
\033[32m|  $$$$$$/\033[34m/ /_ / /_/ /  / / /  ,<  _(__  )
 \033[32m\______/ \033[34m\__/ \____//_/ /_//_/|_| /____/

    """)
print(F.BLUE + "[!]Enlarge window as much as possible for easier observations" + F.RESET)
sleep(2)

subprocess.run("clear")
#Variables
stock_chart = {"Value": False, "Data": False}
#Functions
def internet_test():
    try:
        requests.get("https://google.com") #Python 3.x
        return True
    except:
        return False


def display(df):
    formatters = {}
    for li in list(df.columns):
        max = df[li].str.len().max()
        form = "{{:<{}s}}".format(max)
        formatters[li] = functools.partial(str.format, form)
    print(F.LIGHTGREEN_EX + df.to_string(formatters=formatters,
                                         index=False,
                                         justify="left"))


def search_df(search_str: str, df: pandas.DataFrame) -> pandas.DataFrame:
    symbol_search = df[df["Symbol"].str.contains(search_str.upper())]
    company_search = df[df["Company"].str.contains(search_str, case=False)]
    results = pandas.concat([symbol_search, company_search])
    return results



#Function for fetching stocks, returns pandas.DataFrame object containing stock info
#Stocks pulled from https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap
def stocks():
    #Set pandas options
    pandas.set_option("display.max_rows", 1000)
    pandas.set_option("display.max_columns", 1000)
    pandas.set_option("display.width", 1000)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
               " Chrome/80.0.3987.149 Safari/537.36"}

    #Make Request to site
    site = requests.get("https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap", headers)

    #BeautifulSoup Object
    soup = BeautifulSoup(site.content, "html.parser")

    #Process to go achieve a list of stocks !!!SUGGESTIONS FOR EFICIENCY!!!
    html = list(soup.children)[3]
    body = list(html.children)[3]
    div = list(body.children)[5]
    div2 = list(div.children)[9]
    div3 = list(div2.children)[1]
    div4 = list(div3.children)[3]
    div5 = list(div4.children)[1]
    div6 = list(div5.children)[3]
    div7 = list(div6.children)[3]
    div8 = list(div7.children)[1]
    table = list(div8.children)[1]
    tbody = list(table.children)[3]
    stocks = tbody.find_all("tr")
    chart = {"Symbol": [], "Company": [], "Price Per Share": [], "Change(%)": [], "Change(Points)": []}

    #Find each component of stock and put it into a chart
    for stock in stocks:
        symbol = list(stock.find("td").find("div").find("div"))[1].get_text()
        name = stock.find("td").find("div").find("div").find("span").get_text().strip()
        last_price = "$" + stock.find_all("td")[1].get_text()
        change_percent = stock.find_all("td")[2].get_text()
        change_points = stock.find_all("td")[3].get_text()
        chart["Symbol"].append(symbol)
        chart["Company"].append(name)
        chart["Price Per Share"].append(last_price)
        chart["Change(%)"].append(change_percent)
        chart["Change(Points)"].append(change_points)

    panda_chart = pandas.DataFrame(chart)
    return panda_chart


def ip_info(ip):
    if input():
        pass
    try:
        reader = geoip2.database.Reader("GeoLite2-City.mmdb")
        print(F.GREEN + "[√]Database Loaded")
    except FileNotFoundError:
        print(F.RED + "[!]Could not open database; Exiting application")
        exit(1)
    #subprocess.run("clear")
    response = reader.city(ip)
    print(F.LIGHTBLUE_EX + """
    ISO Code: {iso}
    Country Name: {country}
    State: {state}
    City: {city}
    Postal Code: {post}
    Latitude: {lat}
    Longitude: {long}
    Network: {net}""".format(iso=response.country.iso_code, country=response.country.name,
                             state=response.subdivisions.most_specific.name, city=response.city.name,
                             post=response.postal.code, lat=response.location.latitude, long=response.location.longitude,
                             net=response.traits.network))
    print("\n\nEnter \"q\" to go back to menu or \"op\" to open predicted location in Google Maps.", end="\n\n\n\n\n\n")
    while True:
        inp = input()
        if inp == "q":
            break
        elif inp == "op":
            webbrowser.open(f"https://www.google.com/maps/search/{response.location.latitude},{response.location.longitude}", new=0)
            break

#Main
def main():
    try:
        global stock_chart
        print("""\033[33mOptions:
        
          \033[94m[1] - Display a chart of popular stocks
          [2] - Search a chart of popular stocks
          [3] - Locate an Internet Protocol (IP) Address
        """)
        while True:
            choice = input(F.YELLOW + "Enter Option Number[1-3]> " + F.WHITE)
            if choice in ["1", "2", "3"]:
                break
            print(F.RED + "[!]Option invalid")
        if choice in ["1", "2"]:
            if internet_test():
                pass
            else:
                print(F.RED + "[!]Internet not found, exiting..." + F.RESET)
                exit(1)
            if not stock_chart["Value"]:
                stock_chart["Value"] = True
                stock_chart["Data"] = stocks()
            if choice == "1":
                display(stock_chart["Data"])
            else:
                search = input(F.LIGHTBLUE_EX + "Enter name to search for> ")
                display(search_df(search, stock_chart["Data"]))

        else:
            print(F.YELLOW + "[!]IP information is approximate.  Please use IPv6 for more accurate results.")
            print(F.CYAN + "Press enter to continue...")
            if input():
                pass
            ip_addr = input(F.GREEN + "Enter an Internet Protocol (IP) Address[IPv4 or IPv6]> ")
            try:
                ip_info(ip_addr)
            except ValueError:
                print(F.RED + "IP Address invalid")
                sleep(1)
        main()
    except KeyboardInterrupt:
        print(F.RED + "\n[!]Exiting..." + F.RESET)



if __name__ == "__main__":
    main()







