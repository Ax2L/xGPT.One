import pandas as pd
import phoenix as px

# Perform A/B analysis on your training and production datasets
train_df = pd.read_parquet(
    "http://storage.googleapis.com/arize-assets/phoenix/datasets/structured/credit-card-fraud/credit_card_fraud_train.parquet",
)
prod_df = pd.read_parquet(
    "http://storage.googleapis.com/arize-assets/phoenix/datasets/structured/credit-card-fraud/credit_card_fraud_production.parquet",
)

# Describe the data for analysis
schema = px.Schema(
    prediction_id_column_name="prediction_id",
    prediction_label_column_name="predicted_label",
    prediction_score_column_name="predicted_score",
    actual_label_column_name="actual_label",
    timestamp_column_name="prediction_timestamp",
    feature_column_names=feature_column_names,
    tag_column_names=["age"],
)

# Define your production and training datasets.
prod_ds = px.Dataset(dataframe=prod_df, schema=schema, name="production")
train_ds = px.Dataset(dataframe=train_df, schema=schema, name="training")

# Launch Phoenix for analysis
session = px.launch_app(primary=prod_ds, reference=train_ds)