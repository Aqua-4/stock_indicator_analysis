import pandas as pd
from tqdm import tqdm
import yaml
import os




def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")


def get_formatted_csv(file_name):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(f'../data/raw/{file_name}', parse_dates=True)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Set the 'datetime' column as the DataFrame index
    df.set_index('datetime', inplace=True)
    # only select OHLCV columns
    df = df[['open', 'high', 'low', 'close', 'volume']]
    # Create a new column 'action' and initialize it with 'hold'
    df['action'] = 'hold'
    return df


def mark_buy_sell_continous(df):
    # Find the index of the rows where the next close value is higher and update 'action' column to 'buy'
    buy_indices = df['close'].lt(df['close'].shift(-1))
    df.loc[buy_indices, 'action'] = 'buy'
    # Find the index of the rows where the next close value is lower and update 'action' column to 'sell'
    sell_indices = df['close'].gt(df['close'].shift(-1))
    df.loc[sell_indices, 'action'] = 'sell'
    return df


def mark_buy_sell(df):
    # Resample the DataFrame to daily frequency and get the lowest and highest prices for each day
    daily_prices = df.resample('D').agg(
        {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

    # Create an 'action' column with default value 'hold'
    daily_prices.dropna(inplace=True)
    # mark High as SELL & Low as BUy
    for daily_date in tqdm(daily_prices.index):
        one_day_rows = df[df.index.date == pd.to_datetime(daily_date).date()]
        day_min = one_day_rows['low'].min()
        day_max = one_day_rows['high'].max()

        one_day_rows.loc[one_day_rows['low'] == day_min, 'action'] = 'buy'
        one_day_rows.loc[one_day_rows['high'] == day_max, 'action'] = 'sell'
        # mark lowest price as buy
        for _datetime in one_day_rows[one_day_rows['low'] == day_min].index:
            df.loc[_datetime, 'action'] = 'strong_buy'
        # mark highest price as sell
        for _datetime in one_day_rows[one_day_rows['high'] == day_max].index:
            df.loc[_datetime, 'action'] = 'strong_sell'

    return df

def add_indicator_combination(df):
    # create combination of ADX, RSI, Bollinger Bands
    import pandas_ta as ta

    # COMBINATION 1------------------------------
    # Calculate ADX
    df.ta.adx(length=14, append=True)
    # Calculate RSI
    df.ta.rsi(length=14, append=True)
    # Calculate Bollinger Bands
    df.ta.bbands(length=20, append=True)
    # COMBINATION 1------------------------------

    # COMBINATION 2------------------------------
    df.ta.psar(append=True)
    df.ta.atr(append=True)
    df.ta.stoch(append=True)
    # COMBINATION 2------------------------------

    # COMBINATION 3------------------------------
    df.ta.macd(append=True)
    df.ta.supertrend(append=True)
    df.ta.vwap(append=True)
    # COMBINATION 3------------------------------
    # df.dropna(axis=1, how='all', inplace=True)
    # df.dropna(how='all', inplace=True)
    # df = df.fillna(method='ffill', axis=0)
    return df

# file_name='tmp.csv'
# folder = file_name.replace(".csv", "")


# create_folder_if_not_exists(f'../data/output/{folder}')
# create_folder_if_not_exists(f'../data/output/{folder}/labelled')
# create_folder_if_not_exists(f'../data/output/{folder}/trained')
# create_folder_if_not_exists(f'../data/output/{folder}/predicted')
# create_folder_if_not_exists(f'../data/output/{folder}/model')

# df = get_formatted_csv()
# # df = mark_buy_sell_continous(df)
# df = mark_buy_sell(df)
# df = add_indicator_combination(df)

# # df.dropna(inplace=True)

# # Display the DataFrame with the 'action' column
# print(df.head())

# print(f"Exporting csv with {len(df)} rows")
# # Save the updated DataFrame back to a new CSV file
# df.to_csv(f'../data/output/{folder}/labelled/{file_name}')
