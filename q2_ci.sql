SELECT Name 
FROM country
WHERE Code NOT IN (
SELECT CountryCode 
FROM countrylanguage )
