-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
\c tournament;
DROP TABLE IF EXISTS players;
CREATE TABLE players(
	id SERIAL,
	name TEXT,
	wins INTEGER,
	matches INTEGER,
	score INTEGER
	);
DROP TABLE IF EXISTS matches;
CREATE TABLE matches(
	player1 INTEGER,
	player2 INTEGER
	);
