import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

yf.pdr_override()

# API_KEY = "1863639806:AAEN1kQeraH2NYkDXSbdiaq-1w9V1ome-xM"
# bot = telegram.Bot(API_KEY)
# updater = Updater(token=API_KEY, use_context=True)
# dispatcher = updater.dispatcher
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

startyear = 2020
startmonth = 1
startday = 1

start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

 # "amd", "gme", "amc", "dbx"

payload = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
first_table = payload[0]
second_table = payload[1]

# first_table = first_table.head()

stock_list = first_table["Symbol"].values.tolist()
# stock_list = stock_list[:100]
export_list = []

def stocksearch(stock):
    for stock in stock:
        try:
            df = pdr.get_data_yahoo(stock, start, now)

            # ema_used = [12, 26]

            df[f"Ema_{12}"] = round(df.iloc[:, 3].ewm(span=12, adjust=False).mean(), 3)
            df[f"Ema_{26}"] = round(df.iloc[:, 3].ewm(span=26, adjust=False).mean(), 3)
            df["MACD"] = df["Ema_12"] - df["Ema_26"]
            df["Signal_line"] = round(df.iloc[:, 8].ewm(span=9, adjust=False).mean(), 3)
            df[f"SMA_{21}"] = round(df.iloc[:, 3].rolling(window=21).mean(), 3)
            df[f"SMA_{50}"] = round(df.iloc[:, 3].rolling(window=50).mean(), 3)
            df[f"SMA_{150}"] = round(df.iloc[:, 3].rolling(window=150).mean(), 3)
            df[f"SMA_{200}"] = round(df.iloc[:, 3].rolling(window=200).mean(), 3)

            print(stock)
            currentclose = df["Adj Close"][-1]
            macd = df["MACD"][-1]
            signal_line = df["Signal_line"][-1]
            MA21 = df["SMA_21"][-1]
            MA50 = df["SMA_50"][-1]
            MA150 = df["SMA_150"][-1]
            MA200 = df["SMA_200"][-1]

                # condition 1: MACD > Signal Line
            if macd > signal_line and (macd and signal_line) <= 0:
                cond_1 = True
            else:
                cond_1 = False

            # condition 2:50 SMA > 200 SMA
            # if currentclose > MA50 > MA200:
            #     cond_2 = True
            # else:
            #     cond_2 = False

            if cond_1:
                export_list.append(stock)


        except Exception:
            print(f"No data on {stock}")

stocksearch(stock_list)

print(export_list)
print(len(export_list))

# def start(update, context):
#     context.bot.send_message(chat_id= update.effective_chat.id, text="Hi! How is your day?")
# #command handler recognizes a command and the command is the "start" and then the other parameter called start is the function where the handler runs the function
# start_handler = CommandHandler("start", start)
# dispatcher.add_handler(start_handler)
#
# #function will send the same message back to the person where update.message.text refers to the latest message sent
# def echo(update, context):
#     context.bot.send_message(chat_id= update.effective_chat.id, text=export_list)
# #message handler dk what is filter etc but then it will call the function echo after processing
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher.add_handler(echo_handler)
#
# updater.start_polling()

# print("All Done")
# print(export_list)

# newfile = os.path.dirname(file_path) + "/ScreenerOutput.xlsx"
# writer = ExcelWriter(newfile)
# export_list.to_excel(writer, "Sheet 1")
# writer.save()
