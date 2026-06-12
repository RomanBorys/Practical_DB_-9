from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt


engine = create_engine("mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4")


with engine.connect() as conn:
    print("OK:", conn.execute(text("SELECT NOW()")).scalar())


books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)


df = (orderitem
      .merge(orders, on='OrderID', how='left')
      .merge(books, on='BookID', how='left'))


df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["OrderDate"] = pd.to_datetime(df["OrderDate"])


print(df.head())


sales_by_date = (df.groupby("OrderDate")["Revenue"]
                   .sum()
                   .reset_index()
                   .sort_values("OrderDate"))


print(sales_by_date)


plt.figure(figsize=(8,5))
plt.plot(sales_by_date["OrderDate"], sales_by_date["Revenue"], marker="o", color="teal", linewidth=2)
plt.title("Динаміка продажів за датами", fontsize=14)
plt.xlabel("Дата замовлення")
plt.ylabel("Виручка (CHF)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


plt.savefig('revenue_by_month.png', dpi=200)
print("Графік збережено: revenue_by_month.png")
