
# Define a function to check for crossovers
def crossover(series1, series2):
    # Find where series1 crosses above series2
    cross_above = (series1.shift(1) < series2.shift(1)) & (series1 > series2)
    # Find where series1 crosses below series2
    cross_below = (series1.shift(1) > series2.shift(1)) & (series1 < series2)
    return cross_above, cross_below


def plot_backtest(close_series, entries, exits, freq='1H'):
    import vectorbt as vbt

    portfolio = vbt.Portfolio.from_signals(
        close=close_series,
        entries=entries,
        exits=exits,
        freq=freq
    )

    portfolio.plot().show()
    _stats = portfolio.stats()
    print(_stats)
    return _stats


def print_final_stats(strategy_stats, hyper_params_keys, hyper_params_values):
    print(f"Total Trades= {strategy_stats.get('Total Trades')}")
    print(f"Win Rate [%]= {strategy_stats.get('Win Rate [%]')}")
    print(f"Total Return [%]= {strategy_stats.get('Total Return [%]')}")
    print('-'*40)
    print_hyper_params(hyper_params_keys, hyper_params_values)


def print_hyper_params(hyper_params_keys, hyper_params_values):
    print('Hyper Params:')
    if type(hyper_params_values) != tuple:
        hyper_params_values = [hyper_params_values]
    mapped_hyper_params = zip(hyper_params_keys, hyper_params_values)
    for k, v in set(mapped_hyper_params):
        print(f"{k} = {v}")

def get_valid_datetime(df):
    import pandas as pd
    # valid_index =(df.index.time != pd.to_datetime('09:15:00').time())
    valid_index =(df.index.time != pd.to_datetime('09:15:00').time()) & (df.index.time != pd.to_datetime('15:15:00').time())
    return valid_index
