SELECT Language
FROM country c,countrylanguage cl
WHERE c.Code = cl.CountryCode AND IsOfficial = 'T' AND Population > 1000000
GROUP BY Language
ORDER BY SUM(Population) DESC
LIMIT 10;