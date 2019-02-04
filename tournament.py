from socceria import StrikeStrategy, RandomStrategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
	team= SoccerTeam(name="KhadijaManel's Team")
	if(nb_players === 1):
		team.add("Striker", StrikeStrategy())
	if(nb_players === 2):
 		team.add("Striker", StrikeStrategy())
		
		team.add("Random", RandomStrategy())

	return team


if __name__ == ' __main__':
	from soccersimulator import Simulation, show_simu

	
	team1= get_team(1)
	team2= get_team(2)

	simu= Simulation(team1,team2)

	show_simu(simu)
