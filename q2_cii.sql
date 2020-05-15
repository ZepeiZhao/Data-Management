SELECT Name
FROM country c left outer join countrylanguage cl ON c.Code = cl.CountryCode
WHERE cl.Language is NULL;