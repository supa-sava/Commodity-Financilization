# dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


simple_explanation_1 = """
#### Commodity Universe Selection
We replicate Gorton & Rouwenhorst's (2006) 27-commodity universe using CFTC reports, filtering for these specific contracts:

<details>
<summary>Energy (4 contracts)</summary>

- `CRUDE OIL, LIGHT SWEET - NYMEX`  
- `NO. 2 HEATING OIL, N.Y. HARBOR - NYMEX`  
- `NATURAL GAS - NYMEX`  
- `GASOLINE BLENDSTOCK (RBOB) - NYMEX`
</details>

<details>
<summary>Metals (5 contracts)</summary>

- `GOLD - COMEX`  
- `SILVER - COMEX`  
- `COPPER-GRADE #1 - COMEX`  
- `PLATINUM - NYMEX`  
- `PALLADIUM - NYMEX`
</details>

<details>
<summary>Grains (7 contracts)</summary>

- `CORN - CBOT`  
- `WHEAT - CBOT`  
- `SOYBEANS - CBOT`  
- `SOYBEAN OIL - CBOT`  
- `SOYBEAN MEAL - CBOT`  
- `OATS - CBOT`  
- `ROUGH RICE - CBOT`
</details>

<details>
<summary>Livestock (3 contracts)</summary>

- `LIVE CATTLE - CME`  
- `LEAN HOGS - CME`  
- `FEEDER CATTLE - CME`
</details>

<details>
<summary>Softs (5 contracts)</summary>

- `COTTON NO. 2 - NYBOT`  
- `COFFEE C - NYBOT`  
- `SUGAR NO. 11 - NYBOT`  
- `COCOA - NYBOT`  
- `FRZN CONCENTRATED ORANGE JUICE - ICE`
</details>

<details>
<summary>Other (1 contract)</summary>

- `MILK, Class III - CME`
</details>

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

def main():
    st.set_page_config(page_title="Trader Composition", layout="wide")
    
    st.title("Commodity Futures Trader Composition Analysis")
    st.markdown("""
    Interactive visualization of trader positions across major commodity futures markets
    """)

    # Load data
    df = load_data()
    simple_df = load_simple_data()

    # Date range selector
    min_date = df['Report_Date_as_MM_DD_YYYY'].min()
    max_date = df['Report_Date_as_MM_DD_YYYY'].max()
    
    min_date_simple = simple_df['Report_Date_as_MM_DD_YYYY'].min()
    max_date_simple = simple_df['Report_Date_as_MM_DD_YYYY'].max()

    with st.sidebar:
        st.header("Filters")
        start_date_simple, end_date_simple = st.date_input(
            "Select date range for Fig. 1 CFTC Non-Disaggregated data:",
            value=(min_date_simple, max_date_simple),
            min_value=min_date_simple,
            max_value=max_date_simple
        )


        start_date, end_date = st.date_input(
            "Select date range for Fig. 2 CFTC Disaggregated DAta:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
    
    # Filter data
    filtered_df = df[
        (df['Report_Date_as_MM_DD_YYYY'].dt.date >= start_date) &
        (df['Report_Date_as_MM_DD_YYYY'].dt.date <= end_date)
    ]

    filtered_simple_df = simple_df[
        (simple_df['Report_Date_as_MM_DD_YYYY'].dt.date >= start_date_simple) &
        (simple_df['Report_Date_as_MM_DD_YYYY'].dt.date <= end_date_simple)
    ]
    
    # Show simple plot
    st.subheader("CFTC Non-Disaggregated Futures Only Reports")
    st.markdown(simple_explanation_1, unsafe_allow_html=True)
    st.latex(r"\text{Gross Position} \text{Long} + \text{Short} + 2 \times \text{Spread}") # need  \text{Gross Position} = \text{Long} + \text{Short} + 2 \times \text{Spread}
    st.markdown(simple_explanation_2, unsafe_allow_html=True)
    st.latex(r"\text{Category \%} = \frac{\text{Gross Position}}{2 \times \text{Open Interest}} \times 100")
    st.markdown(simple_explanation_3, unsafe_allow_html=True)
    st.plotly_chart(create_simple_plot(filtered_simple_df), use_container_width=True)

    st.subheader("CFTC Disaggregated Futures Only Reports")
    # Show plot
    st.markdown(disaggregated_explanation_1, unsafe_allow_html=True)
    st.latex(r"\text{Gross Position} = \text{Long} + \text{Short} + 2 \times \text{Spread}")
    st.markdown(disaggregated_explanation_2, unsafe_allow_html=True)
    st.latex(r"\text{Gross Position} = \text{Long} + \text{Short}")
    st.markdown(disaggregated_explanation_3, unsafe_allow_html=True)
    st.latex(r"\text{Category \%} = \frac{\text{Gross Position}}{2 \times \text{Open Interest}} \times 100")
    st.markdown(disaggregated_explanation_4, unsafe_allow_html=True)

    st.plotly_chart(create_plot(filtered_df), use_container_width=True)




    # Data summary
    # st.subheader("Data Summary")
    # st.dataframe(filtered_df.tail(10), use_container_width=True)

if __name__ == "__main__":
    main()