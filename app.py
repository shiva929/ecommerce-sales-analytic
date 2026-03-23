import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="E-commerce Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

@st.cache_data
def load_data():
    revenue    = pd.read_parquet("data/processed/revenue_trend.parquet")
    categories = pd.read_parquet("data/processed/top_categories.parquet")
    rfm        = pd.read_parquet("data/processed/rfm_segments.parquet")
    delivery   = pd.read_parquet("data/processed/delivery_performance.parquet")
    reviews    = pd.read_parquet("data/processed/reviews_by_category.parquet")
    return revenue, categories, rfm, delivery, reviews

revenue, categories, rfm, delivery, reviews = load_data()

# Header
st.title("🛒 E-commerce Sales Analytics Dashboard")
st.caption("SQL analytics on 99,441 orders · Olist dataset · Techniques applicable to Rakuten and Mercari")
st.divider()

# KPI metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total orders",    f"{revenue['total_orders'].sum():,}")
col2.metric("Total revenue",   f"${revenue['total_revenue'].sum():,.0f}")
col3.metric("Avg order value", f"${revenue['avg_order_value'].mean():.2f}")
col4.metric("Champion customers", f"{(rfm['segment']=='Champions').sum():,}")

st.divider()

# Row 1 — Revenue trend + Top categories
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly revenue trend")
    fig = px.line(
        revenue, x='month', y='total_revenue',
        markers=True,
        labels={'total_revenue': 'Revenue ($)', 'month': 'Month'}
    )
    fig.update_traces(line_color='steelblue', line_width=2)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 categories by revenue")
    fig = px.bar(
        categories.sort_values('total_revenue'),
        x='total_revenue', y='category',
        orientation='h',
        labels={'total_revenue': 'Revenue ($)', 'category': ''},
        color='avg_review',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# Row 2 — RFM segments + Delivery performance
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer RFM segmentation")
    segment_counts = rfm['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    colors = {
        'Champions': '#4caf7d',
        'Loyal customers': '#2196F3',
        'At risk': '#FF9800',
        'Lost': '#e05c5c'
    }
    fig = px.pie(
        segment_counts, values='count', names='segment',
        color='segment',
        color_discrete_map=colors,
        hole=0.4
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Delivery performance over time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=delivery['month'], y=delivery['avg_delivery_days'],
        name='Avg delivery days', line=dict(color='steelblue', width=2)
    ))
    fig.add_trace(go.Bar(
        x=delivery['month'], y=delivery['late_pct'],
        name='Late deliveries %', yaxis='y2',
        marker_color='rgba(224, 92, 92, 0.4)'
    ))
    fig.update_layout(
        height=350,
        yaxis=dict(title='Avg delivery days'),
        yaxis2=dict(title='Late %', overlaying='y', side='right'),
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

# Row 3 — Reviews by category + RFM scatter
col1, col2 = st.columns(2)

with col1:
    st.subheader("Review scores by category")
    fig = px.bar(
        reviews.sort_values('avg_review'),
        x='avg_review', y='category',
        orientation='h',
        labels={'avg_review': 'Avg review score', 'category': ''},
        color='avg_review',
        color_continuous_scale='Greens',
        range_x=[3.5, 5.0]
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("RFM — Recency vs Monetary value")
    fig = px.scatter(
        rfm.sample(5000, random_state=42),
        x='recency_days', y='monetary',
        color='segment',
        color_discrete_map=colors,
        labels={
            'recency_days': 'Recency (days since last order)',
            'monetary': 'Total spend ($)'
        },
        opacity=0.6
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# SQL queries expander
with st.expander("View SQL queries used"):
    st.markdown("""
    **Monthly revenue trend**
```sql
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) as month,
        COUNT(DISTINCT o.order_id) as total_orders,
        ROUND(SUM(op.payment_value), 2) as total_revenue,
        ROUND(AVG(op.payment_value), 2) as avg_order_value
    FROM orders o
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
    ORDER BY month
```

    **Top categories by revenue**
```sql
    SELECT 
        COALESCE(ct.product_category_name_english, 
                 p.product_category_name, 'unknown') as category,
        COUNT(DISTINCT oi.order_id) as total_orders,
        ROUND(SUM(oi.price), 2) as total_revenue,
        ROUND(AVG(oi.price), 2) as avg_price,
        ROUND(AVG(r.review_score), 2) as avg_review
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct 
        ON p.product_category_name = ct.product_category_name
    LEFT JOIN order_reviews r ON oi.order_id = r.order_id
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 10
```

    **RFM customer segmentation**
```sql
    SELECT
        o.customer_id,
        MAX(o.order_purchase_timestamp) as last_purchase,
        COUNT(DISTINCT o.order_id) as frequency,
        ROUND(SUM(op.payment_value), 2) as monetary
    FROM orders o
    JOIN order_payments op ON o.order_id = op.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
```
    """)

with st.expander("About this project"):
    st.markdown("""
    **Dataset:** Olist Brazilian E-commerce (99,441 orders, 9 related tables)  
    **Analysis:** SQL queries on SQLite database, Python post-processing  
    **Techniques:** Revenue analysis, RFM segmentation, delivery KPIs, review analytics  

    SQL and RFM segmentation techniques used here are directly applicable 
    to Japanese e-commerce platforms like Rakuten, Mercari, and Amazon JP.
    """)
```

---

### requirements.txt
```
streamlit
plotly
pandas
pyarrow
