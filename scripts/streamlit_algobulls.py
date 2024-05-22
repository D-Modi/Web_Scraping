import pandas as pd
import numpy as np
import streamlit as st
from stratrgy_analysis import StatergyAnalysis
import matplotlib as plt
import time
import re
import glob

path = "/home/dhruvi/Downloads/StrategyBacktestingPLBook-*.csv"
print("\nUsing glob.iglob()")
Files = []
# Prints all types of txt files present in a Path
for file in glob.glob(path, recursive=True):
    found = re.search('StrategyBacktestingPLBook(.+?)csv', str(file)).group(1)[1:-1]
    Files.append(found)

# Using "with" notation
with st.sidebar:
    option = st.radio(
        "Choose a Stratergy Code",
        ("***" + x + "***" for x in Files)
    )
    option = option[3:-3]
    st.write ("Choose Display Options")
    Daily = st.checkbox("Daily Analysis.", True)
    Monthly = st.checkbox("Monthly Analysis", False)
    Yearly = st.checkbox("Yearly Analysis", False)
    Weekly = st.checkbox("Weekly Analysis", False)
    Day = st.checkbox("Analysis based on day of week", False)

  

st.title(f"Analyis Of Stratrergy ***{option}***")

def daisply(daily_returns, Quant):
    if Quant == "Day":
        st.header("Daily Analysis")
    else:
        st.header(f"{Quant}ly Analysis")
    
    days_hist, days_tab = Alanyze.compare_hist(daily_returns, [1000, 2000, 3000, 4000, 5000], Quant)
    st.subheader(f"Number of {Quant} of profit/loss above a threshold") 
    st.pyplot(days_hist)
    with st.expander("More information"):
        st.write(f"Number of trading {Quant}s: {Alanyze.trading_num(daily_returns)}")
        st.write(f"Number of Profitable {Quant}s: {Alanyze.num_profit(daily_returns)} {Quant}")
        st.write(f"Number of Loss Making {Quant}s: {Alanyze.num_loss(daily_returns)} {Quant} ")
        st.write(f"Most Profitable {Quant}: {Alanyze.max_profit(daily_returns)}")
        st.write(f"Least Profitable {Quant}: {Alanyze.min_profit(daily_returns)}")

    st.subheader(f"Profit/Loss Data per {Quant}")
    st.bar_chart(daily_returns, y=['pnl_absolute'] )
    if 'cum_pnl' in daily_returns.columns:
        st.subheader("Cumulative Profit and loss")
        st.line_chart(daily_returns, y=['cum_pnl'])
    st.divider()

def display(weekday_returns):
    st.subheader(f"Profit/Loss Data per Day of Week")
    st.bar_chart(weekday_returns, y=['pnl_absolute'] )
    st.write(f"Most Profitable Day of the week: {Alanyze.max_profit(weekday_returns)}")
    st.write(f"Least Profitable Day of the week: {Alanyze.min_profit(weekday_returns)}")



csv = f"/home/dhruvi/Downloads/StrategyBacktestingPLBook-{option}.csv"
Alanyze = StatergyAnalysis(csv)

daily_returns, monthly_returns, weekday_returns, weekly_returns, yearly_returns = Alanyze.analysis()

if Daily:
    daisply(daily_returns, "Day")
if Monthly:
    daisply(monthly_returns, "Month")
if Yearly:
    daisply(yearly_returns, "Year")
if Weekly:
    daisply(weekly_returns, "Week")
if Day:
    display(weekday_returns)







