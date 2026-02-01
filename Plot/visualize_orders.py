import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Set style for better aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

FILE_PATH = "/home/caocchinh/Downloads/Bitcoin/Margin orders.csv"

def parse_currency_string(value_str):
    """
    Parses a string like '100USDT' or '0.5BTC' into a numeric value and currency symbol.
    Returns (value, currency) tuple.
    """
    if pd.isna(value_str):
        return 0.0, None
    
    value_str = str(value_str).strip()
    match = re.match(r"([0-9.]+)([a-zA-Z]+)", value_str)
    if match:
        try:
            return float(match.group(1)), match.group(2)
        except ValueError:
            return 0.0, None
    
    # Try parsing just as float if no regex match (maybe just a number)
    try:
        return float(value_str), None
    except ValueError:
        return 0.0, None

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print("Error: File not found.")
        return None

    # Date Conversion
    df['Date(UTC)'] = pd.to_datetime(df['Date(UTC)'])
    
    # Numeric Extraction
    # We are interested mainly in 'Trading total' for volume analysis (usually in Quote currency like USDT)
    # and 'Order Amount' / 'Executed' for base currency volume.
    
    # Extract numeric values from 'Trading total'
    df['Total_Value'], df['Quote_Currency'] = zip(*df['Trading total'].map(parse_currency_string))
    
    # Extract numeric values from 'Order Amount'
    df['Amount_Value'], df['Base_Currency'] = zip(*df['Order Amount'].map(parse_currency_string))
    
    # Extract numeric values from 'Executed'
    df['Executed_Value'], _ = zip(*df['Executed'].map(parse_currency_string))

    return df

def plot_overview(df, dataset_name):
    """Generates an overview dashboard figure."""
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle(f'{dataset_name} Trading Overview', fontsize=20)

    # 1. Trading Volume over Time (Aggregated by Day)
    filled_df = df[df['Status'] == 'FILLED'].copy()
    if filled_df.empty:
        print(f"No FILLED orders found for {dataset_name}")
        return fig
        
    filled_df.set_index('Date(UTC)', inplace=True)
    daily_vol = filled_df['Total_Value'].resample('D').sum()
    
    sns.lineplot(x=daily_vol.index, y=daily_vol.values, ax=axes[0, 0], marker='o')
    axes[0, 0].set_title(f'Daily Trading Volume ({dataset_name})')
    axes[0, 0].set_ylabel('Volume (Quote Currency)')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. Order Status Distribution
    status_counts = df['Status'].value_counts()
    sns.barplot(x=status_counts.index, y=status_counts.values, ax=axes[0, 1], palette='viridis')
    axes[0, 1].set_title(f'{dataset_name} Order Status Distribution')
    axes[0, 1].set_ylabel('Count')

    # 3. Buy vs Sell Distribution (Filled Orders)
    if 'Side' in df.columns:
        side_counts = filled_df['Side'].value_counts()
        if not side_counts.empty:
            axes[1, 0].pie(side_counts, labels=side_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
            axes[1, 0].set_title(f'Buy vs Sell Ratio ({dataset_name})')
        else:
             axes[1, 0].text(0.5, 0.5, 'No filled orders to analyze side', ha='center')
    else:
        axes[1, 0].text(0.5, 0.5, 'Side column not found', ha='center')

    # 4. Top 10 Pairs by Volume
    pair_vol = filled_df.groupby('Pair')['Total_Value'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=pair_vol.values, y=pair_vol.index, ax=axes[1, 1], palette='magma')
    axes[1, 1].set_title(f'Top 10 Pairs by Volume ({dataset_name})')
    axes[1, 1].set_xlabel('Total Value')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

def plot_heatmap(df, dataset_name):
    """Generates a heatmap of trading activity."""
    df = df.copy()
    df['Hour'] = df['Date(UTC)'].dt.hour
    df['DayOfWeek'] = df['Date(UTC)'].dt.day_name()
    
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=days_order, ordered=True)
    
    pivot_table = df.pivot_table(index='DayOfWeek', columns='Hour', values='OrderNo', aggfunc='count', fill_value=0)
    
    plt.figure(figsize=(16, 6))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt="d")
    plt.title(f'{dataset_name} Trading Activity Heatmap (Order Count)')
    plt.xlabel('Hour of Day (UTC)')
    plt.ylabel('Day of Week')
    return plt.gcf()

def plot_advanced_analysis(df, dataset_name):
    """Generates advanced visualizations: Top Pair Price Trend, Trade Size Dist, Daily Count."""
    fig, axes = plt.subplots(3, 1, figsize=(16, 18))
    fig.suptitle(f'{dataset_name} Advanced Analysis', fontsize=20)
    
    filled_df = df[df['Status'] == 'FILLED'].copy()
    if filled_df.empty:
         return fig

    # 1. Price Trend of Top Pair
    top_pair = filled_df.groupby('Pair')['Total_Value'].sum().idxmax()
    top_pair_data = filled_df[filled_df['Pair'] == top_pair].sort_values('Date(UTC)')
    
    # Clean Average Price - it might be string or float inside csv
    # Our parse_currency_string handles suffixes, but Average Price usually is just a number string or float
    # Let's ensure it's numeric
    def clean_price(x):
        try:
            return float(str(x).replace(',', ''))
        except:
            return None
            
    top_pair_data['Numeric_Price'] = top_pair_data['Average Price'].apply(clean_price)
    
    sns.lineplot(data=top_pair_data, x='Date(UTC)', y='Numeric_Price', ax=axes[0], marker='.', linestyle='-')
    axes[0].set_title(f'Price Trend for Most Traded Pair: {top_pair} ({dataset_name})')
    axes[0].set_ylabel('Price')

    # 2. Trade Size Distribution (Log Scale)
    sns.histplot(filled_df['Total_Value'], kde=True, ax=axes[1], bins=50, log_scale=True)
    axes[1].set_title(f'Distribution of Trade Sizes (Log Scale) - {dataset_name}')
    axes[1].set_xlabel('Trade Value (Approx Quote Currency)')

    # 3. Daily Trade Count Over Time
    filled_df['Date_Day'] = filled_df['Date(UTC)'].dt.date
    daily_counts = filled_df.groupby('Date_Day').size()
    
    sns.barplot(x=daily_counts.index, y=daily_counts.values, ax=axes[2], color='skyblue')
    axes[2].set_title(f'Daily Number of Trades - {dataset_name}')
    axes[2].set_ylabel('Count of Trades')
    axes[2].tick_params(axis='x', rotation=45)
    # Reduce number of x-ticks to avoid clutter
    import matplotlib.ticker as ticker
    axes[2].xaxis.set_major_locator(ticker.MaxNLocator(nbins=20))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

import numpy as np

def plot_whale_watch(df, dataset_name):
    """
    Generates a 'Whale Watch' Bubble Plot.
    X: Time, Y: Price (Top Pair), Bubble Size: Volume, Color: Side.
    """
    filled_df = df[df['Status'] == 'FILLED'].copy()
    if filled_df.empty:
        return None
        
    # Focus on the most traded pair for a clean price chart
    top_pair = filled_df.groupby('Pair')['Total_Value'].sum().idxmax()
    pair_data = filled_df[filled_df['Pair'] == top_pair].copy()
    
    if pair_data.empty:
        return None

    # Ensure numeric price
    def clean_price(x):
        try:
            return float(str(x).replace(',', ''))
        except:
            return None
    pair_data['Numeric_Price'] = pair_data['Average Price'].apply(clean_price)
    
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.suptitle(f'{dataset_name} "Whale Watch": {top_pair} Trades', fontsize=20)
    
    # Scale bubble sizes (Total_Value) for visibility
    # Min size 20, Max size 1000
    sizes = pair_data['Total_Value']
    if sizes.max() > sizes.min():
        sizes = 20 + (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 1000
    else:
        sizes = 100
        
    sns.scatterplot(
        data=pair_data, 
        x='Date(UTC)', 
        y='Numeric_Price', 
        size='Total_Value', 
        hue='Side', 
        palette={'BUY': 'green', 'SELL': 'red'}, 
        sizes=(20, 1000), 
        alpha=0.6,
        ax=ax
    )
    
    ax.set_title(f'Trades over time taking Place for {top_pair} (Bubble Size = Trade Value)', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Execution Price')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

def plot_technical_analysis(df, dataset_name):
    """
    Generates a Technical Analysis Dashboard for the top pair.
    Includes Moving Averages and Rolling Volatility.
    """
    filled_df = df[df['Status'] == 'FILLED'].copy()
    if filled_df.empty: return None

    top_pair = filled_df.groupby('Pair')['Total_Value'].sum().idxmax()
    pair_data = filled_df[filled_df['Pair'] == top_pair].sort_values('Date(UTC)').copy()
    
    # Ensure numeric price
    def clean_price(x):
        try:
            return float(str(x).replace(',', ''))
        except:
            return np.nan
    pair_data['Numeric_Price'] = pair_data['Average Price'].apply(clean_price)
    pair_data.dropna(subset=['Numeric_Price'], inplace=True)
    
    # Resample to daily close prices for smoother MA
    pair_data.set_index('Date(UTC)', inplace=True)
    daily_close = pair_data['Numeric_Price'].resample('D').last().fillna(method='ffill')
    
    # Calculate Indicators
    sma_7 = daily_close.rolling(window=7).mean()
    sma_30 = daily_close.rolling(window=30).mean()
    volatility = daily_close.pct_change().rolling(window=7).std()

    fig, axes = plt.subplots(2, 1, figsize=(16, 12), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f'{dataset_name} Technical Analysis: {top_pair}', fontsize=20)

    # Price & SMA
    axes[0].plot(daily_close.index, daily_close, label='Daily Close', color='black', alpha=0.5)
    axes[0].plot(sma_7.index, sma_7, label='7-Day SMA', color='orange', linewidth=2)
    axes[0].plot(sma_30.index, sma_30, label='30-Day SMA', color='blue', linewidth=2)
    axes[0].set_title('Price Trend with Moving Averages')
    axes[0].set_ylabel('Price')
    axes[0].legend()
    axes[0].grid(True)

    # Volatility
    axes[1].fill_between(volatility.index, volatility, color='purple', alpha=0.3)
    axes[1].plot(volatility.index, volatility, color='purple', linewidth=1)
    axes[1].set_title('7-Day Rolling Volatility (Standard Deviation of Returns)')
    axes[1].set_ylabel('Volatility')
    axes[1].set_xlabel('Date')
    axes[1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


def process_dataset(name, filepath):
    print(f"\n--- Processing {name} Orders ---")
    df = load_and_clean_data(filepath)
    if df is not None:
        print(f"{name} Data loaded successfully. Shape: {df.shape}")
        
        # 1. Overview
        try:
            fig1 = plot_overview(df, name)
            output_path1 = f"/home/caocchinh/Downloads/Bitcoin/Plot/{name.lower().replace(' ', '_')}_overview.png"
            fig1.savefig(output_path1)
            print(f"Saved {output_path1}")
            plt.close(fig1)
        except Exception as e:
            print(f"Error plotting overview for {name}: {e}")

        # 2. Heatmap
        try:
            fig2 = plot_heatmap(df, name)
            output_path2 = f"/home/caocchinh/Downloads/Bitcoin/Plot/{name.lower().replace(' ', '_')}_heatmap.png"
            fig2.savefig(output_path2)
            print(f"Saved {output_path2}")
            plt.close(fig2)
        except Exception as e:
            print(f"Error plotting heatmap for {name}: {e}")

        # 3. Advanced Analysis
        try:
            fig3 = plot_advanced_analysis(df, name)
            output_path3 = f"/home/caocchinh/Downloads/Bitcoin/Plot/{name.lower().replace(' ', '_')}_advanced.png"
            fig3.savefig(output_path3)
            print(f"Saved {output_path3}")
            plt.close(fig3)
        except Exception as e:
            print(f"Error plotting advanced analysis for {name}: {e}")

        # 4. Whale Watch (Professor Special 1)
        try:
            fig4 = plot_whale_watch(df, name)
            if fig4:
                 output_path4 = f"/home/caocchinh/Downloads/Bitcoin/Plot/{name.lower().replace(' ', '_')}_whale_watch.png"
                 fig4.savefig(output_path4)
                 print(f"Saved {output_path4}")
                 plt.close(fig4)
        except Exception as e:
            print(f"Error plotting whale watch for {name}: {e}")

        # 5. Technical Analysis (Professor Special 2)
        try:
            fig5 = plot_technical_analysis(df, name)
            if fig5:
                output_path5 = f"/home/caocchinh/Downloads/Bitcoin/Plot/{name.lower().replace(' ', '_')}_tech_analysis.png"
                fig5.savefig(output_path5)
                print(f"Saved {output_path5}")
                plt.close(fig5)
        except Exception as e:
             print(f"Error plotting tech analysis for {name}: {e}")



def main():
    datasets = [
        ("Margin Data", "/home/caocchinh/Downloads/Bitcoin/Margin orders.csv"),
        ("Spot Data", "/home/caocchinh/Downloads/Bitcoin/Spot orders.csv")
    ]
    
    for name, path in datasets:
        process_dataset(name, path)

if __name__ == "__main__":
    main()
