def process_commodity(commodity_name, tbill_returns, df):
    monthly = return_monthly(commodity_name, df)
    # Compute monthly futures return
    futures_returns = monthly.pct_change()
    # Determine index range for inclusion/exclusion
    inclusion_month = determine_inclusion_month(monthly)
    if inclusion_month is None:
        print(f"[WARN] No valid data for {commodity_name}. Skipping.")
        return pd.DataFrame()
    exclusion_month = determine_exclusion_month(monthly)
    if exclusion_month:
        print(f"[INFO] for {commodity_name}: Exclusion month = {exclusion_month}")
    mask = (futures_returns.index >= inclusion_month) & (futures_returns.index <= exclusion_month)
    # Reindex tbill returns to match futures return index
    tbill_aligned = tbill_returns.set_index('observation_date')['monthly_return'].reindex(futures_returns.index)
    # Initialize output series
    collateralized_return = pd.Series(index=futures_returns.index, dtype='float64')
    # For included periods: futures return + tbill; if futures return is nan, use tbill only
    for idx in futures_returns.index:
        if mask.loc[idx]:
            if not np.isnan(futures_returns.loc[idx]):
                collateralized_return.loc[idx] = futures_returns.loc[idx] + tbill_aligned.loc[idx]
            else:
                collateralized_return.loc[idx] = tbill_aligned.loc[idx]
        else:
            collateralized_return.loc[idx] = np.nan
    return collateralized_return.to_frame('return')
