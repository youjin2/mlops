# from google.protobuf.duration_pb2 import Duration
from feast import Entity, Field, FeatureView
from feast import FileSource
from feast.types import Int64


# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
token_features = FileSource(
    path="./data/features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="create_timestamp",
    timestamp_field="event_timestamp",
)

driver = Entity(
    name="token",
    description="token id",
)

hourly_view_features_token = FeatureView(
    name="token_hourly_features",
    source=token_features,
    schema=[
        Field(name="prev_1days", dtype=Int64),
        Field(name="prev_2days", dtype=Int64),
        Field(name="prev_3days", dtype=Int64),
        Field(name="prev_4days", dtype=Int64),
        Field(name="prev_5days", dtype=Int64),
        Field(name="prev_6days", dtype=Int64),
        Field(name="prev_7days", dtype=Int64),
        Field(name="prev_8days", dtype=Int64),
        Field(name="prev_9days", dtype=Int64),
        Field(name="prev_10days", dtype=Int64),
        Field(name="prev_11days", dtype=Int64),
        Field(name="prev_12days", dtype=Int64),
        Field(name="prev_13days", dtype=Int64)
    ],
    entities=[driver],
    # ttl=Duration(seconds=3600 * 1),
    ttl=None,
    online=True,
    tags={},
)
