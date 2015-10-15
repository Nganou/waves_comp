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


Install Vagrant and VirtualBox
Clone the wave_comp repository
Launch the Vagrant VM

=======================
 Run the Application
=======================

1. vagrant up
2. vagrant ssh
3. cd /vagrant/tournament
4. ./tournament_test.py