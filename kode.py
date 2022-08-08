import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# Streamlit page configuration 
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache #using cache to load data from axcel
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

st.dataframe(df) # view dataframe on page

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = (
#     df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
# )
# fig_product_sales = px.bar(
#     sales_by_product_line,
#     x="Total",
#     y=sales_by_product_line.index,
#     orientation="h",
#     title="<b>Sales by Product Line</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )

# st.plotly_chart(fig_product_sales, use_container_width=True)

# SALES BY CITY [BAR CHART]
# sales_by_city = (
#     df_selection.groupby(by=["City"]).sum()[["Total"]].sort_values(by="Total")
# )
# fig_product_sales = px.bar(
#     sales_by_city,
#     x="Total",
#     y=sales_by_city.index,
#     orientation="h",
#     title="<b>Sales by City</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_city),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )

# st.plotly_chart(fig_product_sales, use_container_width=True)

# SALES BY PAYMENT [BAR CHART]
# sales_by_payment = (
#     df_selection.groupby(by=["Payment"]).sum()[["Total"]].sort_values(by="Total")
# )
# fig_product_sales = px.bar(
#     sales_by_payment,
#     x="Total",
#     y=sales_by_payment.index,
#     orientation="h",
#     title="<b>Sales by Payment</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_payment),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )

# st.plotly_chart(fig_product_sales, use_container_width=True)


# SALES BY RATING [BAR CHART]
sales_by_rating = (
    df_selection.groupby(by=["Rating"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.line(
    sales_by_rating,
    x="Total",
    y=sales_by_rating.index,
    
    orientation="h",
    title="<b>Rating</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_rating),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales, use_container_width=True)

