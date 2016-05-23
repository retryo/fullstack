#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("DELETE FROM matches")
    c.execute("UPDATE players SET matches=0, wins=0, score=0")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("DELETE FROM players")
    c.execute("ALTER SEQUENCE players_id_seq RESTART WITH 1")
   
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB =psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("SELECT count(*) FROM players")
    playercount,=c.fetchone()
    DB.close()

    return playercount


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB=psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    # c.execute("INSERT INTO players VALUES (default,'{0}',0,0,0)".format(name))
    c.execute("INSERT INTO players VALUES (default,'{0}',0,0,0)".format(name))
    DB.commit()
    DB.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB=psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("SELECT * FROM players ORDER BY wins DESC, score DESC")
    rank=c.fetchall()
    DB.close()
    return rank


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB=psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("UPDATE players SET wins = wins+1, matches = matches+1, score = (score + 2^matches) where id={0}".format(winner))
    c.execute("UPDATE players SET matches = matches+1 where id={0}".format(loser))
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB=psycopg2.connect("dbname=tournament")
    c=DB.cursor()
    c.execute("SELECT id, name FROM players ORDER BY score")
    players= c.fetchall()
    pairs=[]
    for i in range(0,len(players),2):
        pairs.append((players[i][0],players[i][1],players[i+1][0],players[i+1][1]))
    DB.close()
    
    return pairs



