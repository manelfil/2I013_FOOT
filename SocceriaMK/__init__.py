from SocceriaMK.Supertool import RandomStrategy,Fonceur_Strategy,Defenseur2_Strategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
    team= SoccerTeam(name="KhadijaManel's Team")
    if(nb_players==1):
        print("team created")
        team.add("Striker",Fonceur_Strategy())
    if(nb_players==2):
        team.add("Random",Defenseur2_Strategy())
        team.add("Striker",Fonceur_Strategy())
        

    return team