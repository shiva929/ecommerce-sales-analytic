# 🛒 E-commerce Sales Analytics Dashboard

SQL-powered analytics dashboard built on 99,441 e-commerce orders.
Demonstrates data analysis techniques directly applicable to Japanese 
e-commerce platforms like Rakuten, Mercari, and Amazon JP.

## 🔗 Links
- **Live demo:**(https://ecommerce-sales-analytic.streamlit.app/)


## 💡 Problem statement
E-commerce platforms need to understand:
- Which product categories drive the most revenue
- Which customers are loyal vs at risk of churning
- Whether delivery performance is improving over time
- Which categories have the highest customer satisfaction

This dashboard answers all four questions using SQL analytics 
on a real transactional database with 9 related tables.

## 📊 Dataset
- **Source:** Olist Brazilian E-commerce Public Dataset (Kaggle)
- **Size:** 99,441 orders across 9 related tables
- **Period:** October 2016 — August 2018
- **Tables:** orders, order_items, order_payments, order_reviews, 
  customers, products, sellers, geolocation, category_translation

## 🗄️ Database schema
```
orders ──────────── order_items ──── products ──── category_translation
  │                      │
  ├── order_payments      └── order_reviews
  │
  └── customers ──── geolocation
```

## 🔍 SQL analyses

### 1. Monthly revenue trend
Tracks order volume, total revenue, and average order value month 
by month — reveals 10x revenue growth from Oct 2016 to mid-2018.

### 2. Top 10 categories by revenue
Multi-table JOIN across order_items, products, category_translation, 
and order_reviews — identifies health_beauty ($1.26M) and 
watches_gifts ($1.2M) as top performers.

### 3. RFM customer segmentation
Segments 99,441 customers by Recency, Frequency, and Monetary value:

| Segment | Count | Description |
|---------|-------|-------------|
| Champions | 7,867 | Recent, frequent, high spend |
| Loyal customers | 33,115 | Regular buyers |
| At risk | 39,798 | Haven't bought recently |
| Lost | 15,697 | No recent activity |

### 4. Delivery performance
Tracks average delivery days and late delivery % over time — 
average delivery time improved from 54 days (Sept 2016) to 
11 days (mid-2017) as the platform scaled.

### 5. Review scores by category
Identifies highest and lowest rated categories — books_general_interest 
leads with 4.45 avg score across 549 reviews.

## 📈 Key findings
- Health & beauty is the top revenue category at $1.26M
- 40% of customers are at risk — significant retention opportunity
- Delivery times improved 78% from platform launch to maturity
- All top categories maintain avg review score above 4.0
- Watches & gifts has highest avg order value ($200) despite 
  fewer total orders

## 🛠️ Tech stack
- Python, Pandas, SQLite
- SQL — JOINs, aggregations, window functions, CASE statements
- Plotly for interactive visualisations
- Streamlit for deployment

## 📁 Project structure
```
├── app.py                          ← Streamlit dashboard
├── requirements.txt
└── data/
    └── processed/
        ├── revenue_trend.parquet
        ├── top_categories.parquet
        ├── rfm_segments.parquet
        ├── delivery_performance.parquet
        └── reviews_by_category.parquet
```

## 🚀 How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ⚠️ Known limitations
- Dataset covers Brazilian e-commerce (2016–2018) — used to 
  demonstrate SQL techniques applicable to any e-commerce platform
- RFM segmentation uses equal quintile scoring — could be improved 
  with business-specific thresholds
- Future improvement: add customer lifetime value (CLV) prediction 
  using the RFM features

## 📚 Data source
- [Olist Brazilian E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
