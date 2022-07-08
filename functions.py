import pandas as pd

def remove_duplicates(df):
    """Remove duplicate datetime and item

    Args:
        input: pandas dataframe

    Returns:
            Pandas dataframe with duplicates removed
    """    

    # drop duplicates of date and item id
    df.drop_duplicates(subset=['datetime', 'item'], inplace=True)

    return df

def calculate_price_usd(df):
    """Calculate new USD prices

    Args:
        input: pandas dataframe

    Returns:
            Pandas dataframe with new price column
    """    

    # convert cad to usd
    df['price_usd'] = df['price_cad'] * 0.9

    return df

def calculate_mean_price():
    """Load local data into pandas dataframe and summarize stats

    Returns:
            Pandas dataframe
    """    

    # load data - could be Azure endpoint
    df = pd.read_csv('example_data.csv', parse_dates=['datetime'])

    # calculate mean
    avg_price = df.price_cad.mean()

    return avg_price