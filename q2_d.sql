SELECT Name 
FROM country c LEFT OUTER JOIN countrylanguage cl ON c.Code = cl.CountryCode
WHERE IsOfficial = 'F' 
GROUP BY CountryCode 
HAVING COUNT(Language)>=10 
ORDER BY COUNT(Language) DESC;
