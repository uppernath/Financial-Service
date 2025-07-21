# Fraud Detection Data Generator

This generator creates transaction data that closely mimics real-world financial transaction patterns, making it perfect for data engineering learning, model training, and fraud detection system development.

## 🎯 Purpose

This tool generates synthetic transaction data for:
- **Data Engineering Practice**: Building ETL pipelines, data transformations, and feature engineering
- **Machine Learning Training**: Creating labeled datasets for fraud detection models
- **System Testing**: Testing real-time fraud detection systems with realistic data patterns
- **Analytics Development**: Building dashboards and reporting systems

## 📊 Data Simulation Overview

### Core Philosophy
The generator creates realistic transaction patterns by simulating:
- **User Behavior**: Some users are more active than others (realistic distribution)
- **Business Patterns**: Higher transaction volumes during business hours
- **Merchant Categories**: Different spending patterns across merchant types
- **Fraud Indicators**: Realistic fraud patterns based on known risk factors

### Key Assumptions

1. **User Activity Distribution**: 
   - Users make an average of 8 transactions over the time period
   - Some users are much more active than others (following real-world patterns)

2. **Transaction Timing**:
   - 70% of transactions occur during business hours (8 AM - 10 PM)
   - 30% occur outside business hours (including potential fraud)

3. **Fraud Rate**: 
   - Target fraud rate of 2-3% (realistic for financial institutions)
   - Fraud is more likely with certain risk factors present

4. **Geographic Distribution**:
   - Global transactions across 11 countries
   - Includes both developed and developing markets

5. **Payment Methods**:
   - Credit cards: 45% (most common)
   - Debit cards: 35%
   - Digital wallets: 15%
   - Bank transfers: 5%

## 📋 Dataset Schema

The generator creates a CSV file with the following 15 columns:

### Core Transaction Identifiers
| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `transaction_id` | String (UUID) | Unique identifier for each transaction | `f47ac10b-58cc-4372-a567-0e02b2c3d479` |
| `user_id` | String (UUID) | Unique identifier for the customer | `e4b8c5d9-2a1f-4c3e-8f7a-1b2c3d4e5f6g` |
| `transaction_timestamp` | DateTime | Exact date and time of transaction | `2023-03-15 14:23:45` |

### Financial Details
| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `transaction_amount` | Float | Transaction amount in USD | `127.50` |
| `merchant_id` | String | Identifier for the merchant | `merchant_amazon` |
| `merchant_category` | String | Category of merchant business | `online`, `retail`, `restaurant` |
| `payment_method` | String | Payment method used | `credit_card`, `debit_card`, `digital_wallet` |

### Geographic & Device Context
| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `ip_address` | String | IP address of transaction origin | `192.168.1.10` or `73.245.12.8` |
| `geolocation` | String | Geographic location | `New York, NY, US` |
| `device_id` | String | Unique device identifier | `device_1234` |
| `device_type` | String | Type of device used | `mobile`, `desktop`, `tablet` |

### Transaction Metadata
| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `transaction_type` | String | Type of transaction | `purchase`, `withdrawal`, `transfer`, `refund` |
| `transaction_status` | String | Final status of transaction | `completed`, `failed`, `pending` |

### Risk Assessment
| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `is_fraud` | Boolean | Whether transaction is fraudulent | `True`, `False` |
| `risk_score` | Integer | Risk score from 0-100 | `85` |

## 🏪 Merchant Categories

The generator includes 12 realistic merchants across 7 categories:

### Merchant Distribution
| Category | Merchants | Typical Amount Range |
|----------|-----------|---------------------|
| **Online** | Amazon, Apple, Google, Microsoft | $15 - $300 |
| **Retail** | Walmart, Target | $10 - $500 |
| **Restaurant** | McDonald's, Starbucks | $5 - $150 |
| **Gas Station** | Shell | $20 - $100 |
| **Transport** | Uber | $10 - $80 |
| **Subscription** | Netflix | $5 - $50 |
| **Financial** | PayPal | $50 - $1,000 |

### Amount Distribution Logic
- **Small amounts are more common**: Most transactions are under $300
- **Large amounts are rarer**: Transactions over $300 occur only 30% of the time
- **Category-specific ranges**: Each merchant category has realistic spending patterns

## 🌍 Geographic Coverage

The dataset includes transactions from 11 countries:
- **US**: United States
- **GB**: United Kingdom  
- **DE**: Germany
- **FR**: France
- **CA**: Canada
- **IN**: India
- **BR**: Brazil
- **ZA**: South Africa
- **NG**: Nigeria
- **CN**: China
- **RU**: Russia

## 🚨 Fraud Detection Logic

### Risk Factors
The fraud detection algorithm considers multiple risk factors:

| Risk Factor | Risk Score Increase | Reasoning |
|-------------|-------------------|-----------|
| **High Amount** (>$500) | +30 points | Large transactions are riskier |
| **Very High Amount** (>$1000) | +20 points | Additional risk for very large amounts |
| **Off-Hours** (11 PM - 6 AM) | +15 points | Unusual timing patterns |
| **Online Merchant** | +10 points | Online transactions have higher fraud rates |
| **Digital Wallet** | +5 points | Newer payment methods carry more risk |
| **Failed Transaction** | +25 points | Failed transactions often indicate fraud attempts |
| **Private IP** | +20 points | VPN/proxy usage is suspicious |

### Fraud Determination
- **Base risk score**: Calculated from risk factors above
- **Random variation**: ±5 to 10 points added for realism
- **Fraud threshold**: Risk score > 70 AND 30% probability
- **Target fraud rate**: ~2-3% of all transactions

## 🏗️ Technical Implementation

### Memory Optimization
The generator uses a streaming approach to handle large datasets:
- **Chunk-based processing**: Generates data in 50,000 record chunks
- **Direct CSV writing**: Streams directly to disk without loading all data in memory
- **Memory efficient**: Can generate millions of records without memory issues

### Performance Features
- **Reproducible results**: Fixed random seeds ensure consistent output
- **Progress tracking**: Real-time progress bars using tqdm
- **Fast execution**: Optimized for generating 500K records in under 5 minutes

## 🚀 Usage

### Basic Usage
```python
from fraud_data_generator import stream_to_csv

# Generate 500,000 records
stream_to_csv("fraud_data.csv", total_records=500_000)
```

### Custom Parameters
```python
# Generate 1 million records with smaller chunks
stream_to_csv("large_fraud_data.csv", 
              total_records=1_000_000, 
              chunk_size=25_000)
```

## 📁 Output

The generator creates a CSV file with:
- **Clean, consistent data**: No missing values or data quality issues
- **Realistic distributions**: Follows real-world transaction patterns
- **Proper data types**: Ready for immediate use in data pipelines
- **Fraud labels**: Perfect for supervised learning

### Sample Output
```csv
transaction_id,user_id,transaction_timestamp,transaction_amount,merchant_id,merchant_category,payment_method,ip_address,geolocation,device_id,device_type,transaction_type,transaction_status,is_fraud,risk_score
f47ac10b-58cc-4372-a567-0e02b2c3d479,e4b8c5d9-2a1f-4c3e-8f7a-1b2c3d4e5f6g,2023-03-15 14:23:45,127.50,merchant_amazon,online,credit_card,73.245.12.8,New York, NY, US,device_1234,mobile,purchase,completed,False,25
```

## 📊 Data Quality

### Validation Checks
After generation, verify your data has:
- **Correct fraud rate**: ~2-3% of transactions flagged as fraud
- **Realistic amounts**: Most transactions under $300
- **Time distribution**: More transactions during business hours
- **Geographic spread**: Transactions across all 11 countries

### Expected Statistics
- **Total records**: 500,000
- **Unique users**: ~62,500 (8 transactions per user average)
- **Fraud transactions**: ~10,000-15,000 (2-3%)
- **Date range**: Last 2 years from current date
- **Average transaction**: ~$150

## 🔧 Requirements

```bash
pip install pandas faker tqdm
```

## 🎯 Next Steps

This synthetic dataset is perfect for:
1. **ETL Pipeline Development**: Practice with dbt, Apache Airflow, or similar tools
2. **Feature Engineering**: Create time-based, amount-based, and behavioral features
3. **Model Training**: Build and train fraud detection models
4. **Real-time Systems**: Test streaming fraud detection systems
5. **Dashboard Creation**: Build monitoring and alerting dashboards

## 🤝 Contributing

Feel free to extend this generator with:
- Additional merchant categories
- More sophisticated fraud patterns
- Different geographic regions
- Enhanced risk scoring algorithms
- Additional transaction types

---

*This generator creates synthetic data only. No real financial information is used or generated.*