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


book_revenue = (df.groupby("Title")["Revenue"]
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index())


book_revenue["CumulativeRevenue"] = book_revenue["Revenue"].cumsum()
book_revenue["CumulativePercent"] = 100 * book_revenue["CumulativeRevenue"] / book_revenue["Revenue"].sum()


print("\nТоп-книги з накопичувальним % доходу:")
print(book_revenue)


fig, ax1 = plt.subplots(figsize=(8,5))


ax1.bar(book_revenue["Title"], book_revenue["Revenue"], color="skyblue")
ax1.set_xlabel("Назва книги")
ax1.set_ylabel("Виручка (CHF)", color="navy")


ax2 = ax1.twinx()
ax2.plot(book_revenue["Title"], book_revenue["CumulativePercent"], color="orange", marker="o")
ax2.set_ylabel("Накопичувальний відсоток доходу (%)", color="darkorange")
ax2.axhline(80, color="red", linestyle="--", linewidth=1.5, label="80% межа")


plt.title("Аналіз топ-книг (Pareto 80/20)", fontsize=14)
ax1.tick_params(axis='x', rotation=30, labelsize=9)
ax1.grid(axis='y', linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


book_revenue.to_csv("book_pareto.csv", index=False)
print("\nРезультати збережено у файл book_pareto.csv")
