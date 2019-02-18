from SocceriaMK.Supertool import RandomStrategy,Fonceur_Strategy,Defenseur_Strategy
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