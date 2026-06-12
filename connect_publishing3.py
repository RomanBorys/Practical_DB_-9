from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt


engine = create_engine("mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4")


with engine.connect() as conn:
    res = conn.execute(text("SELECT NOW()"))
    print("OK:", res.scalar())


books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)


print("Книги:", books.shape)
print("Замовлення:", orders.shape)
print("Позиції замовлень:", orderitem.shape)


df = (orderitem
      .merge(orders, on='OrderID', how='left')
      .merge(books, on='BookID', how='left'))


df['Revenue'] = df['Quantity'] * df['UnitPrice']
print(df.head())


df.to_csv("sales_data.csv", index=False)
print("Файл збережено: sales_data.csv")


top_books = (df.groupby("Title")["Revenue"]
               .sum()
               .sort_values(ascending=False)
               .reset_index())


plt.figure(figsize=(8,5))
plt.bar(top_books["Title"], top_books["Revenue"], color="skyblue")
plt.title("Дохід по книгах", fontsize=14)
plt.xlabel("Назва книги")
plt.ylabel("Дохід (CHF)")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()
