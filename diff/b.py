def process_commodity(commodity_name, df, tbill_returns):
    """
    Calculates the fully collateralized monthly return for a single commodity.

    Args:
        commodity_name (str): The name of the commodity column.
        df (pd.DataFrame): The main DataFrame with daily futures data.
        tbill_returns (pd.DataFrame): DataFrame with monthly T-bill returns.

    Returns:
        pd.DataFrame: A DataFrame with the collateralized monthly returns.
    """
    # 1. Get monthly closing prices using your existing function
    monthly_prices = return_monthly(commodity_name, df)
    
    # 2. Calculate futures price return (excess return)
    futures_returns = monthly_prices.pct_change().to_frame('futures_return')
    
    # 3. Determine inclusion and exclusion months using your functions
    inclusion_month = determine_inclusion_month(monthly_prices)
    if inclusion_month is None:
        print(f"[WARN] No valid data for {commodity_name}. Skipping.")
        return pd.DataFrame()
        
    exclusion_month = determine_exclusion_month(monthly_prices)
    
    # 4. Create an inclusion mask
    mask = (futures_returns.index >= inclusion_month) & (futures_returns.index <= exclusion_month)
    futures_returns['included'] = mask
    
    # 5. Join with T-bill returns
    # This aligns the T-bill return for each month with the futures return
    combined_returns = futures_returns.join(tbill_returns)
    
    # 6. Calculate the collateralized return
    # If a price is missing during an included period, fillna(0) makes its return 0.
    # Then, add the T-bill return for that month.
    collateralized_return = combined_returns['futures_return'].fillna(0) + combined_returns['monthly_return']
    
    # 7. Finalize returns: only apply returns to months where the commodity is included
    final_returns = pd.DataFrame(index=combined_returns.index)
    final_returns['return'] = np.where(
        combined_returns['included'],
        collateralized_return,
        np.nan  # Set to NaN for months outside the inclusion period
    )
    
    return final_returns