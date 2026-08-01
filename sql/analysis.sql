-- Total Sales
SELECT ROUND(SUM(Sales),2) AS Total_Sales
FROM sales;

-- Total Profit
SELECT ROUND(SUM(Profit),2) AS Total_Profit
FROM sales;

-- Total Orders
SELECT COUNT(*) AS Total_Orders
FROM sales;

-- Top 10 Products
SELECT
    Product,
    ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Product
ORDER BY Revenue DESC
LIMIT 10;

-- Sales by Category
SELECT
    Category,
    ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Category
ORDER BY Revenue DESC;

-- Sales by Region
SELECT
    Region,
    ROUND(SUM(Sales),2) AS Revenue
FROM sales
GROUP BY Region
ORDER BY Revenue DESC;

-- Payment Mode Analysis
SELECT
    PaymentMode,
    COUNT(*) AS Orders
FROM sales
GROUP BY PaymentMode
ORDER BY Orders DESC;
