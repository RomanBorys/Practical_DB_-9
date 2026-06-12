from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt



engine = create_engine("mysql+pymysql://root:root12345@localhost:3306/publishing?charset=utf8mb4")


with engine.connect() as conn:
    result = conn.execute(text("SELECT NOW();"))
    print("Підключення успішне! Поточна дата MySQL:", result.scalar())


books = pd.read_sql("SELECT * FROM Books", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)
orderitem = pd.read_sql("SELECT * FROM OrderItem", engine)


print(f"Книги: {books.shape}, Замовлення: {orders.shape}, Позиції замовлень: {orderitem.shape}")


df = (orderitem
      .merge(orders, on='OrderID', how='left')
      .merge(books, on='BookID', how='left'))


df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["OrderDate"] = pd.to_datetime(df["OrderDate"])


print("\nПерші рядки аналітичної таблиці:")
print(df.head())


kpi = {
    "total_orders": df["OrderID"].nunique(),                     
    "total_units": int(df["Quantity"].sum()),                    
    "total_revenue": float(df["Revenue"].sum()),                
    "avg_order_value": float(df.groupby("OrderID")["Revenue"].sum().mean())  
}


kpi_series = pd.Series(kpi, name="Value")
kpi_series.to_csv("kpi.csv")


print("\nKPI (ключові показники):")
print(kpi_series)


sales_by_date = (df.groupby("OrderDate")["Revenue"]
                   .sum()
                   .reset_index()
                   .sort_values("OrderDate"))


plt.figure(figsize=(8,5))
plt.plot(sales_by_date["OrderDate"], sales_by_date["Revenue"],
         marker="o", color="teal", linewidth=2)
plt.title("Динаміка продажів за датами", fontsize=14)
plt.xlabel("Дата замовлення")
plt.ylabel("Виручка (CHF)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
