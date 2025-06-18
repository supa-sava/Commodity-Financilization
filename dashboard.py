# dashboard.py
import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import plotly.graph_objects as go


simple_explanation_1 = """
#### Commodity Universe Selection
First, we replicate the commodity universe of the 
<details>
<summary>Energy (4 commodities)</summary>

- `CRUDE OIL: Light Sweet Crude Oil (WTI) - NYMEX`
- `GASOLINE: RBOB Gasoline - NYMEX`
- `HEATING OIL: NY Harbor ULSD - NYMEX`
- `NATURAL GAS: Henry Hub Natural Gas - NYMEX`

</details>

<details>
<summary>Metals (5 commodities)</summary>

- `COPPER: Copper - COMEX`  
- `GOLD: Gold - COMEX`
- `PALLADIUM: Palladium - NYMEX`
- `PLATINUM: Platinum - NYMEX`
- `SILVER: Silver - COMEX`

</details>

<details>
<summary>Grains & Oilseeds (7 commodities)</summary>

- `CORN: Corn Composite - CBoT`
- `OATS: Oats - CBoT`
- `ROUGH RICE: Rough Rice - CBoT`
- `SOYBEANS: Soybeans - CBoT`
- `SOYBEAN MEAL: Soybean Meal - CBoT`
- `SOYBEAN OIL: Soybean Oil - CBoT`
- `WHEAT: Wheat - CBoT`

</details>

<details>
<summary>Softs (5 commodities)</summary>

- `COCOA: Cocoa - ICE-US`
- `COFFEE: Coffee C - ICE-US`
- `COTTON: Cotton No. 2 - ICE-US`
- `ORANGE JUICE: FCOJ-A - ICE-US`
- `SUGAR: Sugar No. 11 - ICE-US`

</details>

<details>
<summary>Animal Products (2)</summary>

- `LEAN HOGS: Lean Hogs - CME`
- `LIVE CATTLE: Live Cattle - CME`

</details>



## Index Return Calculation

[UNDER CONSTRUCTION: TODO - DATA READY - NEED TO ADJUST VISUALS]


#### Position Calculations

##### 1. Gross Position Formula
For each trader category (Commercial/Non-Commercial/Non-Reportable):
"""



simple_explanation_2 = """##### 2. Open Interest Normalization"""


simple_explanation_3 = """*Note: The ×2 multiplier accounts for Open Interest counting single contract sides (either long or short), while gross positions count both sides.*

#### Visualization Parameters

- **Commercials (Yellow)**  
  Physical hedgers (producers/consumers)

- **Non-Commercials (Lavender)**  
  Speculators (hedge funds, managed money)

- **Non-Reportables (Teal)**  
  Small traders below CFTC reporting thresholds

Weekly values represent commodity-average percentages of total open interest. Stacked areas show relative proportions of market participation over time."""




disaggregated_explanation_1 = """
#### CFTC Disaggregated Categories Analysis
This visualization uses the CFTC's more granular trader classification system. We maintain the same 27-commodity universe but break down positions into:

<details>
<summary>Trader Categories</summary>

- **Producer/Merchant/Processor/User (Blue)**  
  Physical market participants hedging commercial risks

- **Swap Dealers (Red)**  
  Financial intermediaries managing risk from OTC derivatives

- **Money Managers (Lavender)**  
  Institutional investors (hedge funds, CTAs, etc.)

- **Other Reportables (Yellow)**  
  Large traders not fitting other categories

- **Non-Reportables (Teal)**  
  Small traders below CFTC reporting thresholds
</details>

#### Position Calculations

##### 1. Gross Position Formulas
For each disaggregated category:
"""
# \text{Gross Position} = \text{Long} + \text{Short} + 2 \times \text{Spread}

disaggregated_explanation_2 = """*Applies to: Swap Dealers, Money Managers, Other Reportables*

For Producer/Merchants and Non-Reportables (no spread positions):
"""

# \text{Gross Position} = \text{Long} + \text{Short}



disaggregated_explanation_3 = """
##### 2. Open Interest Normalization
All categories are normalized against total market open interest:
"""
# \text{Category \%} = \frac{\text{Gross Position}}{2 \times \text{Open Interest}} \times 100

disaggregated_explanation_4 = """
*Note: The ×2 multiplier maintains consistency with the CFTC's methodology where Open Interest counts single contract sides.*

#### Key Differences from Non-Disaggregated Data
1. **Commercials are split** into physical hedgers (Producers) and financial intermediaries (Swap Dealers)
2. **Non-Commercials are divided** into Money Managers (institutional) and Other Reportables
3. **Spread positions** are only counted for financial participants
4. **Timeline**: The disaggregated data is available from 2006 onwards, while the non-disaggregated data is available from 1996 onwards.
"""


def load_data():
    return pd.read_csv('COT/trader_composition_data.csv', parse_dates=['Report_Date_as_MM_DD_YYYY'])

def load_simple_data():
    return pd.read_csv('COT_Simple/trader_composition_simple.csv', parse_dates=['Report_Date_as_MM_DD_YYYY'])
def create_simple_plot(df):
    categories = [
        ('Non-Commercial', '#bebada', 'NonComm_Pct'),
        ('Commercial', '#ffffb3', 'Comm_Pct'),
        ('Non-Reportables', '#8dd3c7', 'NonRept_Pct')
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
        title='Commodity Futures Trader Composition - Source CFTC Non-Disaggregated Futures Only Reports',
        xaxis_title='Date',
        yaxis_title='Percentage of Open Interest',
        hovermode='x unified',
        height=600,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100])
    )
    return fig

def create_plot(df):
    categories = [
        ('Producer/Merchant/Processor/User', '#80b1d3', 'Prod_Merc_Pct'),
        ('Swap Dealers', '#fb8072', 'Swap_Pct'),
        ('Money Managers', '#bebada', 'Money_Manager_Pct'),
        ('Other Reportables', '#ffffb3', 'Other_Rept_Pct'),
        ('Non-Reportables', '#8dd3c7', 'NonRept_Pct')
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
        title='Commodity Futures Trader Composition - Source CFTC Disaggregated Futures Only Reports',
        xaxis_title='Date',
        yaxis_title='Percentage of Open Interest',
        hovermode='x unified',
        height=600,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100])
    )
    return fig

def compute_changes(df, categories, date_col):
    """Compute absolute and percentage change for each category between start and end of selected period."""
    start_row = df[df[date_col] == df[date_col].min()].iloc[0]
    end_row = df[df[date_col] == df[date_col].max()].iloc[0]
    results = []
    for name, _, col in categories:
        start_val = start_row[col] * 100
        end_val = end_row[col] * 100
        abs_change = end_val - start_val
        pct_change = (abs_change / start_val * 100) if start_val != 0 else float('nan')
        results.append({
            "Group": name,
            "Start (%)": round(start_val, 2),
            "End (%)": round(end_val, 2),
            "Change (pp)": round(abs_change, 2),
            "Change (%)": round(pct_change, 2)
        })
    # Total change
    start_total = sum([start_row[col] for _, _, col in categories]) * 100
    end_total = sum([end_row[col] for _, _, col in categories]) * 100
    abs_total = end_total - start_total
    pct_total = (abs_total / start_total * 100) if start_total != 0 else float('nan')
    results.append({
        "Group": "Total",
        "Start (%)": round(start_total, 2),
        "End (%)": round(end_total, 2),
        "Change (pp)": round(abs_total, 2),
        "Change (%)": round(pct_total, 2)
    })
    return pd.DataFrame(results)


def main():
    
    
    st.set_page_config(page_title="Commodity Futures Trader Dynamics: A dive into CFTC Data", layout="wide")


    # Embed KnightLab Timeline
    components.iframe(
        "https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=v2%3A2PACX-1vQlwoP4XJabMnq5UPcMta4ZD4B47S6RPOtOtkU8TmpjrUvLYgMKkPEKbai2XFulfk46tOKJHGZ80iqE&font=Default&lang=en&initial_zoom=0&width=100%25&height=650",
        height=650
        )

    st.title("Commodity Futures Trader Market Composition Dynamics: A dive into CFTC Data")
    st.markdown("""
    Interactive visualization of trader positions across major commodity futures markets
    """)



    # Load data
    df = load_data()
    simple_df = load_simple_data()

    # Date range selector for Non-Disaggregated data
    st.subheader("CFTC Non-Disaggregated Futures Only Reports")
    with st.container():
        st.markdown(simple_explanation_1, unsafe_allow_html=True)
        st.latex(r"\text{Gross Position} = \text{Long} + \text{Short} + 2 \times \text{Spread}")
        st.markdown(simple_explanation_2, unsafe_allow_html=True)
        st.latex(r"\text{Category \%} = \frac{\text{Gross Position}}{2 \times \text{Open Interest}} \times 100")
        st.markdown(simple_explanation_3, unsafe_allow_html=True)

        # Date range filter
        min_date_simple = simple_df['Report_Date_as_MM_DD_YYYY'].min()
        max_date_simple = simple_df['Report_Date_as_MM_DD_YYYY'].max()

        allowed_dates = [
            pd.to_datetime("1991-01-01"),
            pd.to_datetime("2004-01-01"),
            pd.to_datetime("2015-01-01"),
            pd.to_datetime("2025-03-01"),
        ]

        start_date_simple = st.selectbox(
            "Select START date for Non-Disaggregated data:",
            options=allowed_dates,
            format_func=lambda d: d.strftime("%Y-%m-%d"),
            index=0,
            key="start_date_simple"
        )
        end_date_simple = st.selectbox(
            "Select END date for Non-Disaggregated data:",
            options=allowed_dates,
            format_func=lambda d: d.strftime("%Y-%m-%d"),
            index=len(allowed_dates) - 1,
            key="end_date_simple"
        )

        # Ensure start_date_simple <= end_date_simple
        if start_date_simple > end_date_simple:
            st.warning("Start date must be before or equal to end date.")

        

        # Filter data
        filtered_simple_df = simple_df[
            (simple_df['Report_Date_as_MM_DD_YYYY'] >= pd.Timestamp(start_date_simple)) &
            (simple_df['Report_Date_as_MM_DD_YYYY'] <= pd.Timestamp((end_date_simple)))
        ]

        # Plot
        st.plotly_chart(create_simple_plot(filtered_simple_df), use_container_width=True)

    # Date range selector for Disaggregated data
    st.subheader("CFTC Disaggregated Futures Only Reports")
    with st.container():
        st.markdown(disaggregated_explanation_1, unsafe_allow_html=True)
        st.latex(r"\text{Gross Position} = \text{Long} + \text{Short} + 2 \times \text{Spread}")
        st.markdown(disaggregated_explanation_2, unsafe_allow_html=True)
        st.latex(r"\text{Gross Position} = \text{Long} + \text{Short}")
        st.markdown(disaggregated_explanation_3, unsafe_allow_html=True)
        st.latex(r"\text{Category \%} = \frac{\text{Gross Position}}{2 \times \text{Open Interest}} \times 100")
        st.markdown(disaggregated_explanation_4, unsafe_allow_html=True)

        # Date range filter
        min_date = df['Report_Date_as_MM_DD_YYYY'].min()
        max_date = df['Report_Date_as_MM_DD_YYYY'].max()

        allowed_dates = [
            pd.to_datetime("1991-01-01"),
            pd.to_datetime("2004-01-01"),
            pd.to_datetime("2015-01-01"),
            pd.to_datetime("2025-03-01"),
        ]

        # data range selector:
        start_date = st.selectbox(
            "Select START date for Non-Disaggregated data:",
            options=allowed_dates,
            format_func=lambda d: d.strftime("%Y-%m-%d"),
            index=0,
            key="start_date_disagg"

        )
        end_date = st.selectbox(
            "Select END date for Non-Disaggregated data:",
            options=allowed_dates,
            format_func=lambda d: d.strftime("%Y-%m-%d"),
            index=len(allowed_dates) - 1,
            key="end_date_disagg"
        )

        # Ensure start_date_simple <= end_date_simple
        if start_date > end_date:
            st.warning("Start date must be before or equal to end date.")

        # start_date, end_date = st.date_input(
        #     "Select date range for Disaggregated data:",
        #     value=(min_date, max_date),
        #     min_value=min_date,
        #     max_value=max_date
        # )

        # Filter data
        filtered_df = df[
            (df['Report_Date_as_MM_DD_YYYY'] >= pd.Timestamp((start_date))) &
            (df['Report_Date_as_MM_DD_YYYY'] <= pd.Timestamp((end_date)))
        ]

        # Plot
        st.plotly_chart(create_plot(filtered_df), use_container_width=True)

if __name__ == "__main__":
    main()