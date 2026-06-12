from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


engine = create_engine("mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4")


with engine.connect() as conn:
    print("Підключення успішне:", conn.execute(text("SELECT NOW()")).scalar())


books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)


print(f"Завантажено: Books={books.shape}, Orders={orders.shape}, OrderItem={orderitem.shape}")


df = (orderitem
      .merge(orders, on="OrderID", how="left")
      .merge(books, on="BookID", how="left"))


df["Revenue"] = df["Quantity"] * df["UnitPrice"]


print("\nПерші рядки об’єднаної таблиці:")
print(df.head())


pivot = (df.groupby(["Genre", "PublishYear"])["Revenue"]
           .sum()
           .unstack(fill_value=0))


print("\nЗведена таблиця жанр × рік видання:")
print(pivot)


plt.figure(figsize=(8,5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Жанр × Рік видання (виручка)", fontsize=14)
plt.xlabel("Рік видання")
plt.ylabel("Жанр")
plt.tight_layout()
plt.show()


pivot.to_csv("genre_year_heatmap.csv")
print("\nРезультати збережено у файл genre_year_heatmap.csv")
