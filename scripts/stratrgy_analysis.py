import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta

class StatergyAnalysis:

    def __init__(self, csv_filepath):
        self.csv_data = self.get_csv(csv_filepath)
        self.daily_returnts = None
        self.equity_curve_value = self.csv_data['equity_curve'].tolist()
        self.risk_free_rate = 0.02
        #self.initial_investment = self.equity_curve_value[-1]
        self.initial_investment = 150000
        self.equity_PctChange = None
        self.annual_std = 0
        self.annual_mean = 0
        self.drawdown_max, self.drawdown_pct = self.drawdown()
        self.daily_equity_Curve()
        self.num_wins = self.num_profit(self.csv_data)
        self.numTrades = len(self.csv_data)

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
        
        if 'Equity Curve' in data.columns:
            data.rename(columns={'Equity Curve': 'equity_curve'}, inplace=True)

        if 'EN_TT' in data.columns:
            data.rename(columns={'EN_TT': 'entry_transaction_type'}, inplace=True)
        
        return data
    
    def daily_equity_Curve(self):
        daily_equity_curve = self.csv_data.groupby('Day')['equity_curve'].last()
        self.equity_PctChange = daily_equity_curve.pct_change().dropna()
        self.annual_mean = self.equity_PctChange.mean() * 252   
        self.annual_std = self.equity_PctChange.std() * 252   
    
    def get_last_equity_curve(self, group):
        return group['equity_curve'].iloc[0]

    def analysis(self):
        daily_returns = self.csv_data.groupby('Day').sum(numeric_only = True)
        daily_returns['equity_curve'] = self.csv_data.groupby('Day').apply(self.get_last_equity_curve)
        daily_returns['cum_pnl'] = daily_returns['pnl_absolute'].cumsum()
        daily_analysis = daily_returns[['pnl_absolute', 'cum_pnl', 'equity_curve']]
        self.daily_returnts = daily_analysis

        Monthly_returns = self.csv_data.groupby('Month').sum(numeric_only = True)
        Monthly_returns['cum_pnl'] = Monthly_returns['pnl_absolute'].cumsum()
        Monthly_returns['roi'] = round((Monthly_returns['cum_pnl']/self.initial_investment)*100,2)
        monthly_analysis = Monthly_returns[['pnl_absolute', 'cum_pnl', 'roi']]

        weekday_returns = self.csv_data.groupby('weekday').sum(numeric_only = True)
        weekday_returns['cum_pnl'] = weekday_returns['pnl_absolute'].cumsum()
        weekday_returns[['pnl_absolute','cum_pnl']]

        weekly_returns = self.csv_data.groupby('Week').sum(numeric_only = True)
        weekly_returns['cum_pnl'] = weekly_returns['pnl_absolute'].cumsum()
        weekly_returns[['pnl_absolute','cum_pnl']]

        yearly_returns = self.csv_data.groupby('Year').sum(numeric_only = True)
        yearly_returns['cum_pnl'] = yearly_returns['pnl_absolute'].cumsum()
        yearly_returns['equity_curve'] = self.csv_data.groupby('Year').apply(self.get_last_equity_curve)
        yearly_returns[['pnl_absolute', 'cum_pnl']]

        return daily_analysis, monthly_analysis, weekday_returns, weekly_returns, yearly_returns 

    def max_profit(self, returns):
        max_profits = returns['pnl_absolute'].max()
        max_profitable_day = returns['pnl_absolute'].idxmax()
        maxi = [max_profits, max_profitable_day]
        return maxi

    def min_profit(self, returns):
        min_profitable_day = returns['pnl_absolute'].min()
        min_profit_day =  returns['pnl_absolute'].idxmin()
        return [min_profitable_day, min_profit_day] 
    
    def Sharpe(self):
        sharpe_ratio = (self.annual_mean - self.risk_free_rate) / self.annual_std
        print(sharpe_ratio)
        return sharpe_ratio
    
    def Calmar(self):
        calmar_ratio = self.annual_mean / self.drawdown_pct
        print(calmar_ratio)
        return calmar_ratio
    
    def Sortino(self):
        downside_returns = self.equity_PctChange[self.equity_PctChange < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252)
        sortino_ratio = (self.annual_mean - self.risk_free_rate) / downside_deviation
        print(sortino_ratio)
        return sortino_ratio
    
    def max_consecutive(self, quant):
  
        if quant ==1:
            positive_mask = self.csv_data['pnl_absolute'] > 0
        else:
            positive_mask = self.csv_data['pnl_absolute']  < 0
        
        grouped = (positive_mask != positive_mask.shift()).cumsum()
        positive_counts = positive_mask.groupby(grouped).cumsum()
        return positive_counts.max()
    
    def win_rate(self, daily_returns):
        wins = daily_returns[daily_returns['pnl_absolute']>=0]
        total_prof = sum(wins['pnl_absolute'])
        print(total_prof/len(wins))
        return len(wins)/len(daily_returns)*100

    def winCount(self, daily_returns, i):
        wins = daily_returns[daily_returns['pnl_absolute']>=0]
        if i >0:
            return len(wins)
        else:
            return len(daily_returns) - len(wins)
        
    def Treturns(self, t):
        cum_pnl = self.daily_returnts['cum_pnl'].tolist()
        cum_pnl = cum_pnl[-1*t:]
        ret = cum_pnl[-1] - cum_pnl[0]
        print(ret*100/self.initial_investment)
        return ret, ret*100/self.initial_investment
    
    def Last_returns(self, diff):
        daily_pnl = self.daily_returnts['cum_pnl'].tolist()
        dayt_amt = daily_pnl[-1]
        dayt = self.daily_returnts.index[-1]
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(dayt, date_format)
        one_year_prior = date_obj - diff
        value = self.daily_returnts.loc[one_year_prior, 'cum_pnl']
        ret = dayt_amt - value
        print(ret*100/self.initial_investment)
        return ret, ret*100/self.initial_investment   

    def avgReturns(self, daily_returns):
        daily_returns['returns'] = daily_returns['cum_pnl']/self.initial_investment *100
        avg_returns = daily_returns['cum_pnl'].mean()
        avg_returns_pct = daily_returns['returns'].mean()
        return avg_returns, avg_returns_pct
    
    def drawdown(self):
        self.csv_data['cum_max'] = self.csv_data['equity_curve'].cummax()
        self.csv_data['drawdown'] = self.csv_data['equity_curve'] - self.csv_data['cum_max']
        self.csv_data['drawdown_pct'] = (self.csv_data['drawdown']/self.csv_data['cum_max'])*100
    
        return self.csv_data['drawdown'].min(), self.csv_data['drawdown_pct'].min()
    
    def daily_returns_hist(self, daily_returns):
        plt.hist(daily_returns['pnl_absolute'])
        plt.savefig("histogram")
        plt.show()

        plt.plot(daily_returns['cum_pnl'])
        plt.savefig('histogram')
        plt.show()

    def roi(self, monthly_returns):
        ROI = monthly_returns[['cum_pnl']].iloc[-1]
        ROI_perct = round((ROI.values[0]/150000)*100,2)
        return ROI.values[0], ROI_perct

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

    def HIT(self):
        return round((self.num_wins/self.numTrades*100), 1)
    
    def num_tradeType(self, quant):
        i = -1
        if quant == "short":
            i = 1
        elif quant == "long":
            i = 0
        else :
            return None
        
        trad = self.csv_data[self.csv_data['entry_transaction_type'] == i]
        return len(trad)
            
    def avgTrades(self, daily_returns):
        return len(self.csv_data)/len(daily_returns)
    
    def ProfitFactor(self):
        positive_values = self.csv_data[self.csv_data['pnl_absolute'] > 0]
        neg_values = self.csv_data[self.csv_data['pnl_absolute'] < 0]
        profit = positive_values['pnl_absolute'].sum()
        loss = neg_values['pnl_absolute'].sum()
        return profit/loss
    
