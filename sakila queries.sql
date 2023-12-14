USE sakila;

SELECT * FROM film;
SELECT * FROM film_actor;
SELECT * FROM inventory;
SELECT * FROM language;


SELECT title, 
CASE
	WHEN COUNT(CASE WHEN EXTRACT(YEAR_MONTH FROM rental_date)) = '200505' THEN 'TRUE'
	ELSE 'False'
END AS rented_in_may
FROM film AS f
JOIN inventory AS i
ON f.film_id = i.film_id
JOIN rental as r
ON i.inventory_id = r.inventory_id;


SELECT f.title,
       MAX(f.film_id) AS film_id,
       MAX(f.release_year) AS release_year,
       MAX(f.rental_duration) AS rental_duration,
       MAX(f.rental_rate) AS rental_rate,
       MAX(f.length) AS length,
       MAX(f.rating) AS rating,
       MAX(r.rental_date) AS rental_date,
       CASE
         WHEN COUNT(CASE WHEN EXTRACT(YEAR_MONTH FROM rental_date) = '200505' THEN 1 END) > 0
         THEN TRUE
         ELSE FALSE
       END AS rented_in_may
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.title;


SELECT f.film_id, c.name AS category FROM film_category AS f
JOIN category AS c ON f.category_id = c.category_id
ORDER BY film_id;





SELECT title, 
CASE
	WHEN year(r.rental_date) = '2005' THEN 'True'
    ELSE 'False'
END AS rented_in_may
FROM film AS f
RIGHT JOIN inventory AS i
ON f.film_id = i.film_id
LEFT JOIN rental as r
ON i.inventory_id = r.inventory_id;



SELECT * ,
CASE
	WHEN year(rental_date) = '2005' THEN 'True'
    ELSE 'False'
END AS rented_in_may
FROM rental;

SELECT * 
FROM film AS f
LEFT JOIN inventory AS i
ON f.film_id = i.film_id
LEFT JOIN rental as r
ON i.inventory_id = r.inventory_id;