USE world;
DROP VIEW IF EXISTS LangCnt;
CREATE  VIEW LangCnt 
AS
SELECT CountryCode,COUNT(Language) CNT
FROM countrylanguage
GROUP BY CountryCode
ORDER BY COUNT(Language) DESC;

SELECT Name 
FROM Country 
WHERE Code IN (SELECT CountryCode FROM LangCnt
WHERE CNT = (SELECT max(CNT) FROM LangCnt));