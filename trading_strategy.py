import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def moving_average_strategy(csv_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Ensure data is sorted by date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate moving averages
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()
    
    # Generate signals
    df['signal'] = 0
    df.loc[df['MA50'] > df['MA200'], 'signal'] = 1  # Buy signal
    
    # Calculate daily returns
    df['returns'] = df['close'].pct_change()
    
    # Calculate strategy returns
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    
    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['returns']).cumprod()
    df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod()
    
    # Generate buy/sell signals for reporting
    df['buy_signal'] = ((df['signal'] == 1) & (df['signal'].shift(1) == 0))
    df['sell_signal'] = ((df['signal'] == 0) & (df['signal'].shift(1) == 1))
    
    # Generate report
    buy_signals = df[df['buy_signal']]
    sell_signals = df[df['sell_signal']]
    
    # Calculate total profit/loss
    total_return = df['cumulative_strategy_returns'].iloc[-1] - 1 if len(df) > 0 else 0
    
    # Create report
    report = {
        'total_return': round(total_return * 100, 2),
        'buy_signals': buy_signals[['date', 'close']].rename(columns={'close': 'price'}).to_dict('records'),
        'sell_signals': sell_signals[['date', 'close']].rename(columns={'close': 'price'}).to_dict('records'),
    }
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['cumulative_returns'], label='Buy and Hold')
    plt.plot(df['date'], df['cumulative_strategy_returns'], label='MA Strategy')
    plt.scatter(buy_signals['date'], buy_signals['cumulative_strategy_returns'], marker='^', color='g', label='Buy')
    plt.scatter(sell_signals['date'], sell_signals['cumulative_strategy_returns'], marker='v', color='r', label='Sell')
    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()
    plt.savefig('strategy_performance.png')
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        report = moving_average_strategy(csv_file)
        print(f"Strategy Report:")
        print(f"Total Return: {report['total_return']}%")
        print(f"Buy Signals: {len(report['buy_signals'])}")
        print(f"Sell Signals: {len(report['sell_signals'])}")
    else:
        print("Please provide a CSV file path")