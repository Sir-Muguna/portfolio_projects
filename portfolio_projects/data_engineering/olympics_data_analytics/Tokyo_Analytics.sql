-- Count the number of athletes from each country:
SELECT Country, COUNT(*) AS TotalAthletes
FROM athletes
GROUP BY Country
ORDER BY TotalAthletes DESC;

-- Calculate the total medals won by each country:
SELECT Country,
SUM(Gold) Total_Gold,
SUM(Silver) Total_Silver,
SUM(Bronze) Total_Bronze
FROM medals
GROUP BY Country
ORDER BY Total_Gold DESC;

-- Average Number of entries by gender for each discipline
SELECT Discipline, 
AVG(Female) Average_Female_Entry, 
AVG(Male) Average_Male_Entry
FROM entriesgender
GROUP BY Discipline;

-- Top Discipline and Country with high number of gold medals
SELECT t.Discipline, 
t.Country, 
SUM(m.Gold) Total_Gold
FROM teams AS t 
INNER JOIN medals AS m ON
t.Country = m.Country
GROUP BY t.Discipline, t.Country
ORDER by SUM(m.Gold) DESC;
