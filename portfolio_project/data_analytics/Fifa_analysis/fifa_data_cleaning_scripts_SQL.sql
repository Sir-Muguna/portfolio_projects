/* Create a Database */
CREATE DATABASE IF NOT EXISTS Fifa_database;
-- -----------------------------------------------
USE Fifa_database;
-- -----------------------------------------------
/* Create a table schema based on the following Details
Name		Data Type
---------------------
Home		string,
Away		string,
Stage		string,
Scorer		string,
ScoringTeam	string,
Type		string */
-- Structure to create table `match_details`
CREATE TABLE IF NOT EXISTS `match_details` (
  `ID` varchar(50) NOT NULL,
  `Home` varchar(255) NOT NULL,
  `Away` varchar(255) NOT NULL,
  `Stage` varchar(255) NOT NULL,
  `Scorer` varchar(255) NOT NULL,
  `ScoringTeam` varchar(255) NOT NULL,
  `Type` varchar(255) NOT NULL
) ;
-- ------------------------------------------------
/* Import the csv file into match_details table using table with table data import wizard 
1. Right click on the table name in the left hand side navigator in MySQL workbench
2. Follow the on-screen prompts and map the field and data types*/

/*How do we read / extract / query the data imported in match_details table?

SELECT <columns separated by comma> 
FROM <table name>
WHERE <conditions to filter the rows, if any>
Limit <restrict the number of rows to extract>;

*/
/* show the top 10 rows of the match_details table */
SELECT 
    *
FROM
    match_details
LIMIT 10;
-- ------------------------------------------------
/* Remove Duplicated rows */
/* First check which rows are duplicated using ID column */
select ID, count(ID)
from match_details
group by ID
HAVING count(ID) > 1;


select ID, count(ID) as cnt 
from match_details group by ID Having cnt>1;

/* Now there are several methods to remove duplicated rows in SQL. 
We'll go through one of the simplest methods.*/

select DISTINCT *
from match_details;

/* First we'll create a table with non duplicated rows */
CREATE TABLE non_dup_data 
SELECT Distinct * 
FROM match_details;

select * from non_dup_data limit 10;

/* delete the original table */
drop table match_details;


/* Finally alter the non duplicated table name to the original table name*/
alter table non_dup_data rename match_details;

select * from match_details;

select ID, Count(ID)
from match_details
group by ID
having count(ID) > 1;
 
-- ------------------------------------------------
/* show the Scorer name and how many goals they have scored 
then store that data into another table called scorer */

select scorer, count(ID) as goals
from match_details
group by Scorer;

create table IF NOT EXISTS scorer
select scorer, count(ID) as goals
from match_details
group by Scorer;

CREATE TABLE IF NOT EXISTS scoring 
select Scorer, count(*) as Goals 
from match_details group by Scorer;
-- ------------------------------------------------
/* Check scoring table. Show the scorer with the most goals first*/
select * 
from scorer
order by Goals DESC;

select Scorer, count(*) as Goals 
from match_details group by Scorer;