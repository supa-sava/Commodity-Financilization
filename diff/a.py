def process_commodity(commodity_name, tbill_returns, df):

    """Process individual commodity futures data"""
    # Resample to end-of-month prices and handle missing data
    monthly = return_monthly(commodity_name, df)
    
    # # Calculate futures returns (percentage change)
    futures_returns = monthly.pct_change().to_frame('futures_return')
    # return futures_returns

    # Determine inclusion month (next month after first available data)
    inclusion_month = determine_inclusion_month(monthly)
    if inclusion_month is None:
        print(f"[WARN] No valid data for {commodity_name}. Skipping.")
        return pd.DataFrame()  # Skip if no valid data

    # Determine exclusion month (last month with valid data)
    exclusion_month = determine_exclusion_month(monthly)
    if exclusion_month:
        print(f"[INFO] for {commodity_name}: Exclusion month = {exclusion_month}")
    
    mask = (futures_returns.index >= inclusion_month) & (futures_returns.index <= exclusion_month)
    
    tbill_aligned = tbill_returns.set_index('observation_date')['monthly_return'].reindex(futures_returns.index)
    collateralized_return = pd.Series(index=futures_returns.index, dtype='float64') 
    
    for idx in futures_returns.index:
        if mask.loc[idx]:
            if not np.isnan(futures_returns.loc[idx]):
                collateralized_return.loc[idx] = futures_returns.loc[idx] + tbill_aligned.loc[idx]
            else:
                collateralized_return.loc[idx] = tbill_aligned.loc[idx]
        else:
            collateralized_return.loc[idx] = np.nan
    return collateralized_return.to_frame('return')