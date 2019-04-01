from SocceriaMK.Supertool import RandomStrategy,Fonceur_Strategy,Defenseur2_Strategy,Defenseur1_Strategy,Attaquant2_Strategy,Fonceur2_Strategy
from soccersimulator import SoccerTeam

def get_team(nb_players):
    team= SoccerTeam(name="KhadijaManel's Team")
    if(nb_players==1):
        print("team created")
        team.add("Striker",Fonceur_Strategy())
    if(nb_players==2):
        team.add("defenseur",Defenseur2_Strategy())
        team.add("Striker",Fonceur_Strategy())
    if(nb_players==4):
        team.add("def1",Defenseur1_Strategy())
        team.add("attq",Attaquant2_Strategy())
        team.add("fncr",Fonceur2_Strategy())
        team.add("def2",Defenseur2_Strategy())
        

    return team