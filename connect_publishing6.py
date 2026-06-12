from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt


engine = create_engine("mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4")


with engine.connect() as conn:
    print("Підключення успішне:", conn.execute(text("SELECT NOW()")).scalar())


books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)


print(f"Таблиці завантажено: Books={books.shape}, Orders={orders.shape}, OrderItem={orderitem.shape}")


df = (orderitem
      .merge(orders, on='OrderID', how='left')
      .merge(books, on='BookID', how='left'))


df["Revenue"] = df["Quantity"] * df["UnitPrice"]


print("\nПерші рядки аналітичної таблиці:")
print(df.head())


genre_revenue = (df.groupby("Genre")["Revenue"]
                   .sum()
                   .sort_values(ascending=False)
                   .reset_index())


print("\nТоп жанри за виручкою:")
print(genre_revenue)


plt.figure(figsize=(8,5))
plt.barh(genre_revenue["Genre"], genre_revenue["Revenue"], color="cornflowerblue")
plt.title("Топ-жанри за виручкою", fontsize=14)
plt.xlabel("Виручка (CHF)")
plt.ylabel("Жанр")
plt.gca().invert_yaxis() 
plt.grid(axis='x', linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


genre_revenue.to_csv("genre_revenue.csv", index=False)
print("\nРезультат збережено у файл genre_revenue.csv")
