wave_comp
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

tournament.sql:

Creates the tables for the tournament and consists of:
	- Tournament database: Consists of the Match(battle) organizer's Informations
	- Matches database: consists of matches(battles), winner and loser.
	- Players database: consists of an artist id, name, song(instrumental) entered in the contest, location
	- Results database: Consists of the result of a match(battle), the winner, status of match in win/lose/draw

tournament.py


1. Install Vagrant and VirtualBox

2. Clone the wave_comp repository

3. Launch the Vagrant VM by runninc the commands
	a. vagrant up
	b. vagrant ssh

=======================
 Run the Application
=======================


1. cd /vagrant/tournament
2.  ./tournament_test.py
