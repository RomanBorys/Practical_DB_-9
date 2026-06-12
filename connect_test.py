from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mysql+pymysql://root:root12345@localhost/publishing"
)

query = "SELECT * FROM Authors"

df = pd.read_sql(query, engine)

print(df)