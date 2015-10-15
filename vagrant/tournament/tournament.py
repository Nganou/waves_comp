#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# 
# Serge Nganou
# Developer @HP

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

    """Remove all the match records from the database."""

def View_Tournament():
    conn = connect()
    c = conn.cursor()
    view_all_q = """SELECT * FROM T_TOURNAMENTS;"""
    c.execute(view_all_q)

    for val in c.fetchall():
        print val

    conn.commit()
    conn.close()

def View_Matches():
    conn = connect()
    c = conn.cursor()
    view_all_q = """SELECT * FROM T_MATCHES;"""
    c.execute(view_all_q)

    for val in c.fetchall():
        print val

    conn.commit()
    conn.close()

def View_Players():
    conn = connect()
    c = conn.cursor()
    view_all_q = """SELECT * FROM T_PLAYERS;"""
    c.execute(view_all_q)

    for val in c.fetchall():
        print val

    conn.commit()
    conn.close()

def View_Results():
    conn = connect()
    c = conn.cursor()
    view_all_q = """SELECT * FROM T_RESULTS;"""
    c.execute(view_all_q)

    for val in c.fetchall():
        print val

    conn.commit()
    conn.close()


def deleteMatches():
    conn = connect()
    c = conn.cursor()
    delete_all = """DELETE FROM T_MATCHES; DELETE FROM T_RESULTS;"""
    c.execute(delete_all)

    conn.commit()
    conn.close()

    """Remove all the player records from the database."""
def deletePlayers():
    conn = connect()
    c = conn.cursor()
    delete_all = """DELETE FROM T_PLAYERS; DELETE FROM T_RESULTS;"""
    c.execute(delete_all)
    conn.commit()
    conn.close()


    """Returns the number of players currently registered."""
def countPlayers(ID_TOURN):
    conn = connect()
    c = conn.cursor()
    Count_Players = "SELECT COUNT(ID_Player) AS Player_TOT FROM T_RESULTS WHERE ID_TOURN = %s;"
    Insert_TOT = """UPDATE T_TOURNAMENTS SET TOURN_Player_TOT = %s WHERE ID_TOURN= %s;"""
    c.execute(Count_Players, (ID_TOURN,))
    Player_TOT = c.fetchone()[0]
    c.execute(Insert_TOT, (Player_TOT, ID_TOURN))
    conn.commit()
    conn.close()
    return Player_TOT

def registerPlayer(player_name, id_tourn):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      player_name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    Insert_Player = "INSERT INTO T_PLAYERS (Player_Name,Player_Email, Player_Song, Player_City, Player_State) VALUES(%s,%s,%s,%s,%s) RETURNING ID_PLAYER;"
    Insert_result = "INSERT INTO T_RESULTS (RESULT_FINAL, ID_TOURN, ID_MATCH, ID_PLAYER, ID_WIN_LOSE, ID_ELIMIN) VALUES(%s,%s,%s,%s,%s,%s);"
    Insert_plyr_tot = """UPDATE T_TOURNAMENTS SET TOURN_Player_TOT = %s WHERE ID_TOURN = %s"""
    player_tot = countPlayers(id_tourn)

    c.execute(Insert_Player, (player_name,0,0,0,0,))
    id_player = c.fetchone()[0]
    c.execute(Insert_result, (0,id_tourn, 0, id_player,' ', False,))
    c.execute(Insert_plyr_tot, (player_tot,id_tourn,))


    conn.commit()
    conn.close()


def playerStandings(id_tourn):
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
    conn = connect()
    c = conn.cursor()

    Standing_List = """
        SELECT a.ID_PLAYER, b.Player_Name,
            (SELECT SUM(c.RESULT_Final)
             FROM T_RESULTS  AS c
             WHERE c.ID_WIN_LOSE IN  ('L','W',' ') AND c.ID_TOURN = %s AND a.ID_PLAYER = c.ID_Player
            )AS  Wins,
            (SELECT SUM(d.ID_MATCH)
                FROM T_RESULTS AS d
                WHERE d.ID_PLAYER = a.ID_PLAYER AND
                ID_TOURN = %s
            ) AS matches
        FROM T_RESULTS a
        INNER JOIN T_PLAYERS AS b on b.ID_PLAYER = a.ID_PLAYER
        WHERE ID_TOURN = %s
        ORDER BY Wins Desc;
    """
    c.execute(Standing_List, (id_tourn,id_tourn, id_tourn,))

    Standings = []

    for val in c.fetchall():
        Standings.append(val)
    
    conn.commit()
    conn.close()
    return Standings

def reportMatch(match_winner, match_loser, id_tourn):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw:   the id number of the players who drew
    """
    conn = connect()
    c = conn.cursor()

    check_draw = """SELECT ID_WIN_LOSE FROM T_RESULTS WHERE id_player = %s"""
    c.execute(check_draw, (match_winner,))
    draw = c.fetchone()[0]

    if draw == 'D':
        winner = 1
        loser = 1
    else:
        winner = 3
        loser  = 0

    Add_Score = """ INSERT INTO
                    T_MATCHES(Match_Tourn, Match_Winner, Match_Loser)
                    VALUES (%s,%s,%s);
    """ 
    Add_Win   = """ UPDATE T_RESULTS 
                    SET RESULT_Final = (RESULT_Final+%s), ID_MATCH = (ID_MATCH+1), ID_WIN_LOSE = 'W'
                    WHERE ID_PLAYER = %s and ID_TOURN = %s;               
    """
    Add_Loss  = """ UPDATE T_RESULTS
                    SET RESULT_Final = (RESULT_Final+%s), ID_MATCH = (ID_MATCH+1), ID_WIN_LOSE = 'L' 
                    WHERE ID_PLAYER = %s and ID_TOURN = %s; 
    """

    c.execute(Add_Score, (id_tourn, match_winner, match_loser,))
    c.execute(Add_Win,   (winner, match_winner,id_tourn,))
    c.execute(Add_Loss,  (loser, match_loser,id_tourn,))
    
    conn.commit()
    conn.close()

def Elimination( id_tourn, id_player):
    """ Sets the Elimination falg to True

        Assuming that the player lost the last game, and is the last player on standing list
    """
    conn = connect()
    c = conn.cursor()

    Elimin = "UPDATE T_RESULTS SET ID_ELIMIN = TRUE WHERE ID_PLAYER = %s AND ID_TOURN = %s"

    c.execute(Elimin, (id_player, id_tourn))
    conn.commit()
    conn.close()

def swissPairings(id_tourn):
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
    conn = connect()
    c = conn.cursor()

    Standing_list = playerStandings(id_tourn)

    Matchs = []

    # Check if even number of players
    player_tot = countPlayers(id_tourn)
    if (player_tot % 2) != 0:
        Elimin = Standing_list.popitem()
        Elimination(id_tourn, Elimin[0])

    while len(Standing_list) >= 2:
        artist_1 = Standing_list.pop()
        artist_2 = Standing_list.pop()
        Matchs.append((artist_1[0], artist_1[1], artist_2[0], artist_2[1]))

    conn.commit()
    View_Tournament()
    View_Results()
    View_Matches()
    View_Players()
    conn.close()

    return Matchs

    




