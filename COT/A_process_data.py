# process_data.py
import pandas as pd
from pathlib import Path

def load_filtered_data(file_path):
    """Load and filter raw data file"""
    try:
        df = pd.read_excel(file_path)
        
        # Filter by CFTC Commodity Codes (original paper's 27 commodities)
        CFTC_Commodity_Codes = [
            67, 22, 111, 23, 85, 84, 88, 76, 75, 1, 2, 5, 7, 26, 4, 39,
            57, 54, 61, 52, 33, 40, 58, 73, 83, 80
        ]
        return df[df['CFTC_Commodity_Code'].isin(CFTC_Commodity_Codes)]
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

def calculate_percentages(df):
    """Calculate trader category percentages"""
    # Calculate gross positions
    df['Prod_Merc_Gross'] = df['Prod_Merc_Positions_Long_ALL'] + df['Prod_Merc_Positions_Short_ALL']
    df['Swap_Gross'] = (df['Swap_Positions_Long_All'] + 
                       df['Swap__Positions_Short_All'] + 
                       2 * df['Swap__Positions_Spread_All'])
    df['Money_Manager_Gross'] = (df['M_Money_Positions_Long_ALL'] + 
                                df['M_Money_Positions_Short_ALL'] + 
                                2 * df['M_Money_Positions_Spread_ALL'])
    df['Other_Rept_Gross'] = (df['Other_Rept_Positions_Long_ALL'] + 
                             df['Other_Rept_Positions_Short_ALL'] + 
                             2 * df['Other_Rept_Positions_Spread_ALL'])
    df['NonRept_Gross'] = df['NonRept_Positions_Long_All'] + df['NonRept_Positions_Short_All']

    # Calculate percentages
    df['Prod_Merc_Pct'] = df['Prod_Merc_Gross'] / (2 * df['Open_Interest_All'])
    df['Swap_Pct'] = df['Swap_Gross'] / (2 * df['Open_Interest_All'])
    df['Money_Manager_Pct'] = df['Money_Manager_Gross'] / (2 * df['Open_Interest_All'])
    df['Other_Rept_Pct'] = df['Other_Rept_Gross'] / (2 * df['Open_Interest_All'])
    df['NonRept_Pct'] = df['NonRept_Gross'] / (2 * df['Open_Interest_All'])
    
    return df

def main():
    # Input directory configuration
    data_dir = Path("COT/data")
    output_file = "COT/trader_composition_data.csv"
    
    # List of data files (modify as needed)
    file_paths = [
        data_dir / "2006-2015.xls",
        data_dir / "2016.xls",
        data_dir / "2017.xls",
        data_dir / "2018.xls",
        data_dir / "2019.xls",
        data_dir / "2020.xls",
        data_dir / "2021.xls",
        data_dir / "2022.xls",
        data_dir / "2023.xls",
        data_dir / "2024.xls",
        data_dir / "2025.xls"
    ]

    # Load and concatenate all data
    print("Loading and processing data files...")
    dfs = [load_filtered_data(fp) for fp in file_paths]
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Filter to approved contracts (original paper's list)
    approved_contracts = [
        # Energy (4)
        'CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE',
        'NO. 2 HEATING OIL, N.Y. HARBOR - NEW YORK MERCANTILE EXCHANGE',
        'NATURAL GAS - NEW YORK MERCANTILE EXCHANGE',
        'GASOLINE BLENDSTOCK (RBOB) - NEW YORK MERCANTILE EXCHANGE',
        
        # Metals (5)
        'GOLD - COMMODITY EXCHANGE INC.',
        'SILVER - COMMODITY EXCHANGE INC.',
        'COPPER-GRADE #1 - COMMODITY EXCHANGE INC.',
        'PLATINUM - NEW YORK MERCANTILE EXCHANGE',
        'PALLADIUM - NEW YORK MERCANTILE EXCHANGE',
        
        # Grains (7)
        'CORN - CHICAGO BOARD OF TRADE',
        'WHEAT - CHICAGO BOARD OF TRADE',
        'SOYBEANS - CHICAGO BOARD OF TRADE',
        'SOYBEAN OIL - CHICAGO BOARD OF TRADE',
        'SOYBEAN MEAL - CHICAGO BOARD OF TRADE',
        'OATS - CHICAGO BOARD OF TRADE',
        'ROUGH RICE - CHICAGO BOARD OF TRADE',
        
        # Livestock (3)
        'LIVE CATTLE - CHICAGO MERCANTILE EXCHANGE',
        'LEAN HOGS - CHICAGO MERCANTILE EXCHANGE',
        'FEEDER CATTLE - CHICAGO MERCANTILE EXCHANGE',
        
        # Softs (5)
        'COTTON NO. 2 - NEW YORK BOARD OF TRADE',
        'COFFEE C - NEW YORK BOARD OF TRADE',
        'SUGAR NO. 11 - NEW YORK BOARD OF TRADE',
        'COCOA - NEW YORK BOARD OF TRADE',
        'FRZN CONCENTRATED ORANGE JUICE - ICE FUTURES U.S.',
        
        # Other (1)
        'MILK, Class III - CHICAGO MERCANTILE EXCHANGE'
    ]
    
    print("Filtering to approved contracts...")
    filtered_df = combined_df[combined_df['Market_and_Exchange_Names'].isin(approved_contracts)]
    
    # Process dates
    filtered_df['Report_Date_as_MM_DD_YYYY'] = pd.to_datetime(
        filtered_df['Report_Date_as_MM_DD_YYYY'],
        errors='coerce'
    )
    filtered_df = filtered_df.dropna(subset=['Report_Date_as_MM_DD_YYYY'])
    
    # Calculate percentages
    print("Calculating trader percentages...")
    processed_df = calculate_percentages(filtered_df)
    
    # Aggregate data by date
    print("Aggregating data...")
    agg_df = processed_df.groupby('Report_Date_as_MM_DD_YYYY').agg({
        'Prod_Merc_Pct': 'mean',
        'Swap_Pct': 'mean',
        'Money_Manager_Pct': 'mean',
        'Other_Rept_Pct': 'mean',
        'NonRept_Pct': 'mean'
    }).reset_index()
    
    # Save results
    print(f"Saving results to {output_file}...")
    agg_df.to_csv(output_file, index=False)
    print("Processing complete!")

if __name__ == "__main__":
    main()