# Stock Indicator
A program that uses the help of Yahoo Finance Package to scape current financial data from Yahoo Finance.
It helps to find the stocks that satisfy "buy" condition of the popular Moving Average Convergence Divergence(MACD) technical trading strategy.

The default start date of the testing strategy is set to be 1st January 2021.
To run the code, simply run it on any IDE of choice.
The program will begin scraping the Yahoo Finance page for the S&P 500 companies and return the companies that satisfy the conditions.
The original program is meant to work in conjunction with a Telegram bot such that the Telegram Bot provides the interactive interface to return the stocks. However,
as it is a private API key, I have removed it. The program should still run on the IDE less the use of a Telegram Bot.