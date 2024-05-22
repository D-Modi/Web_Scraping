import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import datetime as dt
class StatergyAnalysis:

    def __init__(self, csv_filepath):
        self.csv_data = self.get_csv(csv_filepath)


    def get_csv(self, filepath):

        try:
            data = pd.read_csv(filepath, parse_dates=['entry_timestamp'])

            data['Day'] = pd.to_datetime(data.entry_timestamp,format = '%Y-%m')
            data['Week'] = pd.to_datetime(data.entry_timestamp,format = '%dd-%m')
            data['Month'] = pd.to_datetime(data.entry_timestamp,format = '%Y-%m')
            data['Year'] = pd.to_datetime(data.entry_timestamp,format = '%Y-%m')
            data['weekday'] = pd.to_datetime(data.entry_timestamp,format = '%a')\
            
            data['Day'] = data['Day'].dt.strftime('%Y-%m-%d')
            data['Week'] = data['Week'].dt.strftime('%Y-%U')
            data['Month'] = data['Month'].dt.strftime('%Y-%m')
            data['Year'] = data['Year'].dt.strftime('%Y')
            data['weekday'] = data['weekday'].dt.strftime('%a')
        except Exception as e:
            data = pd.read_csv(filepath, parse_dates=['EN_TIME'])

            data['Day'] = pd.to_datetime(data.EN_TIME,format = '%Y-%m')
            data['Week'] = pd.to_datetime(data.EN_TIME,format = '%dd-%m')
            data['Month'] = pd.to_datetime(data.EN_TIME,format = '%Y-%m')
            data['Year'] = pd.to_datetime(data.EN_TIME,format = '%Y-%m')
            data['weekday'] = pd.to_datetime(data.EN_TIME,format = '%a')
            
            data['Day'] = data['Day'].dt.strftime('%Y-%m-%d')
            data['Week'] = data['Week'].dt.strftime('%Y-%m-%d')
            data['Month'] = data['Month'].dt.strftime('%Y-%m')
            data['Year'] = data['Year'].dt.strftime('%Y')
            data['weekday'] = data['weekday'].dt.strftime('%a')
        
        if 'P&L' in data.columns:
            data.rename(columns={'P&L': 'pnl_absolute'}, inplace=True)

        return data

    def analysis(self):
        daily_returns = self.csv_data.groupby('Day').sum(numeric_only = True)
        daily_returns['cum_pnl'] = daily_returns['pnl_absolute'].cumsum()
        daily_analysis = daily_returns[['pnl_absolute', 'cum_pnl']]

        Monthly_returns = self.csv_data.groupby('Month').sum(numeric_only = True)
        Monthly_returns['cum_pnl'] = Monthly_returns['pnl_absolute'].cumsum()
        monthly_analysis = Monthly_returns[['pnl_absolute', 'cum_pnl']]

        weekday_returns = self.csv_data.groupby('weekday').sum(numeric_only = True)
        weekday_returns['cum_pnl'] = weekday_returns['pnl_absolute'].cumsum()
        weekday_returns[['pnl_absolute','cum_pnl']]

        weekly_returns = self.csv_data.groupby('Week').sum(numeric_only = True)
        weekly_returns['cum_pnl'] = weekly_returns['pnl_absolute'].cumsum()
        weekly_returns[['pnl_absolute','cum_pnl']]

        yearly_returns = self.csv_data.groupby('Year').sum(numeric_only = True)
        yearly_returns['pnl_absolute']

        return daily_analysis, monthly_analysis, weekday_returns, weekly_returns, yearly_returns 

    def max_profit(self, returns):
        max_profitable_day = returns['pnl_absolute'].max()
        return max_profitable_day

    def min_profit(self, returns):
        min_profitable_day = returns['pnl_absolute'].min()
        return min_profitable_day 


    def daily_returns_hist(self, daily_returns):
        plt.hist(daily_returns['pnl_absolute'])
        plt.savefig("histogram")
        plt.show()

        plt.plot(daily_returns['cum_pnl'])
        plt.savefig('histogram')
        plt.show()

    def roi(self, monthly_returns):
        ROI = monthly_returns[['cum P&L']].iloc[-1]
        ROI_perct = round((ROI/150000)*100,2)
        return ROI, ROI_perct

    def num_profit(self, returns):
        return sum(returns['pnl_absolute'] > 0)

    def num_loss(self, returns):
        return sum(returns['pnl_absolute'] < 0)

    def trading_num(self, returns):
        return len(returns)

    def compare_hist(self, returns, num, Quant):

        df = pd.DataFrame()
        df["Value"] = num
        profit = []
        loss = []
        for value in num:
            profit.append(sum(returns['pnl_absolute'] > value))
            loss.append((sum(returns['pnl_absolute'] < -1 * value))) 

        df["Profit"] = profit
        df["Loss"] = loss

        n= len(num)
        r = np.arange(n) 
        width = 0.25

        fig, ax = plt.subplots()
               
        ax.bar(r, profit, color = 'b', width = width, label='Profit')
        ax.bar(r + width, loss, color = 'r', width = width, label='Loss') 
        
        ax.set_xlabel("Value") 
        ax.set_ylabel(f"Number of {Quant}") 

        ax.set_xticks(r + width / 2)
        ax.set_xticklabels(num)
        ax.legend() 
    
        df.set_index('Value', inplace=True)
        return fig, df

    def HIT(self, prfit, total):
        return round((prfit/total*100, 1))

def main():

    file_path = "/home/dhruvi/Downloads/StrategyBacktestingPLBook-STAB736.csv"
    obj = StatergyAnalysis(file_path)
    csv = obj.get_csv(file_path)
    print(csv.info())
    daily_returns, monthly_returns, weekday_returns, weekly_returns, yearly_returns = obj.analysis(csv)

    profitable_days = obj.num_profit(daily_returns)
    loss_days = obj.num_loss(daily_returns)

    profitable_months = obj.num_profit(monthly_returns)
    loss_months = obj.num_loss(monthly_returns)

    max_profitable_day = obj.max_profit(daily_returns)
    min_profitable_day = obj.min_profit(daily_returns)

    max_profitable_month = obj.max_profit(monthly_returns)
    min_profitable_month = obj.min_profit(monthly_returns)

    max_profitable_week = obj.max_profit(weekly_returns)
    min_profitable_week = obj.min_profit(weekly_returns)

    trading_days = obj.trading_num(daily_returns)
    trading_months = obj.trading_num(monthly_returns)

    profit, loss = obj.compare(daily_returns, 1000) 
    HIT_ratio = obj.HIT(profitable_days, trading_days)
    ROI, ROI_percent = obj.roi(monthly_returns)



