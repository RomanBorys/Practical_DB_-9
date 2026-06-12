from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4"
)

with engine.connect() as conn:
    print("OK:", conn.execute(text("SELECT NOW()")).scalar())

books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)

print("Книги:", books.shape)
print("Замовлення:", orders.shape)
print("Позиції замовлень:", orderitem.shape)

# Об'єднання таблиць

df = (orderitem
      .merge(orders, on='OrderID', how='left')
      .merge(books, on='BookID', how='left'))

df['Revenue'] = df['Quantity'] * df['UnitPrice']

print(df.head())

# Збереження у CSV

df.to_csv('sales_data.csv', index=False, encoding='utf-8')

print("Файл збережено: sales_data.csv")