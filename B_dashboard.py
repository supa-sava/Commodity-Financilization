# dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data():
    return pd.read_csv('COT/trader_composition_data.csv', parse_dates=['Report_Date_as_MM_DD_YYYY'])

def create_plot(df):
    categories = [
        ('Producer/Merchant/Processor/User', '#e5ebf9', 'Prod_Merc_Pct'),
        ('Swap Dealers', '#b9cb8c', 'Swap_Pct'),
        ('Money Managers', '#7a9ed6', 'Money_Manager_Pct'),
        ('Other Reportables', '#e5ebf9', 'Other_Rept_Pct'),
        ('Non-Reportables', '#e3c76f', 'NonRept_Pct')
    ]

    fig = go.Figure()
    for name, color, col_name in categories:
        fig.add_trace(go.Scatter(
            x=df['Report_Date_as_MM_DD_YYYY'],
            y=df[col_name] * 100,
            mode='lines',
            stackgroup='one',
            name=name,
            line=dict(width=0.5, color=color),
            hoverinfo='x+y+name',
            fill='tonexty'
        ))

    fig.update_layout(
        title='Commodity Futures Trader Composition',
        xaxis_title='Date',
        yaxis_title='Percentage of Open Interest',
        hovermode='x unified',
        height=600,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100])
    )
    return fig

def main():
    st.set_page_config(page_title="Trader Composition", layout="wide")
    
    st.title("Commodity Futures Trader Composition Analysis")
    st.markdown("""
    Interactive visualization of trader positions across major commodity futures markets
    """)

    # Load data
    df = load_data()
    
    # Date range selector
    min_date = df['Report_Date_as_MM_DD_YYYY'].min()
    max_date = df['Report_Date_as_MM_DD_YYYY'].max()
    
    with st.sidebar:
        st.header("Filters")
        start_date, end_date = st.date_input(
            "Select date range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Filter data
    filtered_df = df[
        (df['Report_Date_as_MM_DD_YYYY'].dt.date >= start_date) &
        (df['Report_Date_as_MM_DD_YYYY'].dt.date <= end_date)
    ]

    # Show plot
    st.plotly_chart(create_plot(filtered_df), use_container_width=True)

    # Data summary
    st.subheader("Data Summary")
    st.dataframe(filtered_df.tail(10), use_container_width=True)

if __name__ == "__main__":
    main()