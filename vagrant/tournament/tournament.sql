-- Table definitions for the tournament project.

-- Serge Nganou
-- Developer @HP
-- The purpose of creating extra feilds was to help 
-- create a simulation of an Instrumental Battle tournament. 


/* Create the tables for the tournament :
   This table contains the following data:
	- Tournament database: Consists of the Match(Battle) organizer
	- Matches database: consists of records matches(battles)
	- Players database: consists of an artist id, name, 
	  song(instrumental) entered in the contest, location
	- Results database: Consists of the result of a match(battle)
*/


DROP TABLE IF EXISTS T_TOURNAMENTS CASCADE;
CREATE TABLE T_TOURNAMENTS (
	ID_TOURN SERIAL PRIMARY KEY,
	TOURN_Title varchar(32),
	TOURN_Organizer varchar(32),
	Tourn_Start_Date Date,
	Tourn_End_Date Date,
	TOURN_Player_TOT INTEGER
);

-- Insert a Tournament
INSERT INTO T_TOURNAMENTS 
	(TOURN_Title, TOURN_Organizer, Tourn_Start_Date, Tourn_End_Date, TOURN_Player_TOT)
	VALUES('SoundFest 2015', 'SoundsCloud', to_date('10-05-2015', 'MM-DD-YYYY'), to_date('10-10-2015', 'MM-DD-YYYY'), 0);


-- Create Match table
DROP TABLE IF EXISTS T_MATCHES CASCADE;
CREATE TABLE T_MATCHES(
	ID_MATCH SERIAL PRIMARY KEY,
	id_tourn NUMERIC,
	Match_Winner NUMERIC,
	Match_Loser NUMERIC
);

-- Create Player table
DROP TABLE IF EXISTS T_PLAYERS CASCADE;
CREATE TABLE T_PLAYERS(
	ID_Player SERIAL PRIMARY KEY,
	Player_Name varchar(32),
	Player_Email varchar(32),
	Player_Song varchar(50),
	Player_City varchar(32),
	Player_State varchar(32)
);

-- Create Results table
DROP  TABLE IF EXISTS T_RESULTS CASCADE;
CREATE TABLE T_RESULTS(
	RESULT_Final NUMERIC,
	ID_TOURN INTEGER REFERENCES T_TOURNAMENTS (ID_TOURN) ON DELETE RESTRICT,
	ID_MATCH INTEGER REFERENCES T_MATCHES (ID_MATCH) ON DELETE RESTRICT,
	ID_Player INTEGER REFERENCES T_PLAYERS (ID_Player) ON DELETE RESTRICT,
	ID_WIN_LOSE CHAR,
	ID_ELIMIN BOOLEAN
);


