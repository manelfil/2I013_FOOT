from socceria.Supertool import RandomStrategy,Fonceur_Strategy,Defenseur_Strategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
    team= SoccerTeam(name="KhadijaManel's Team")
    if(nb_players==1):
        print("team created")
        team.add("Striker",Fonceur_Strategy())
    if(nb_players==2):
        team.add("Striker",Fonceur_Strategy())
        team.add("Random",Defenseur_Strategy())

    return team


if __name__ == '__main__':
    from soccersimulator import Simulation, show_simu
    print("iii")
	
    team1= get_team(1)
    team2= get_team(2)

    simu= Simulation(team1,team2)

    show_simu(simu)
