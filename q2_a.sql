SELECT city.Name,city.Population 
FROM city WHERE city.CountryCode IN 
(SELECT code 
FROM country 
WHERE Name = 'United States') 
ORDER BY Population DESC 
LIMIT 10;
