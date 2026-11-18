-- 1. Total delivered revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_orders WHERE order_status = 'Delivered';

-- 2. Monthly revenue
SELECT order_month, ROUND(SUM(revenue), 2) AS revenue
FROM fact_orders WHERE order_status = 'Delivered'
GROUP BY order_month ORDER BY order_month;

-- 3. Top products
SELECT p.product_name, ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_orders f JOIN dim_products p ON f.product_id = p.product_id
WHERE f.order_status = 'Delivered'
GROUP BY p.product_name ORDER BY revenue DESC;

-- 4. Revenue by city
SELECT c.customer_city, ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_orders f JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE f.order_status = 'Delivered'
GROUP BY c.customer_city ORDER BY revenue DESC;

-- 5. Customer lifetime value proxy
SELECT customer_id, ROUND(SUM(revenue), 2) AS lifetime_revenue
FROM fact_orders WHERE order_status = 'Delivered'
GROUP BY customer_id ORDER BY lifetime_revenue DESC LIMIT 20;

-- 6. Order status distribution
SELECT order_status, COUNT(*) AS orders
FROM fact_orders GROUP BY order_status;

-- 7. Average order value
SELECT ROUND(AVG(revenue), 2) AS average_order_value
FROM fact_orders WHERE order_status = 'Delivered';

-- 8. Payment method usage
SELECT payment_method, COUNT(*) AS orders
FROM fact_orders GROUP BY payment_method ORDER BY orders DESC;

-- 9. Category performance
SELECT p.category, ROUND(SUM(f.revenue), 2) AS revenue
FROM fact_orders f JOIN dim_products p ON f.product_id = p.product_id
WHERE f.order_status = 'Delivered'
GROUP BY p.category ORDER BY revenue DESC;

-- 10. Monthly order ranking using a window function
SELECT order_month, order_id, revenue,
       DENSE_RANK() OVER (PARTITION BY order_month ORDER BY revenue DESC) AS rank_in_month
FROM fact_orders;
