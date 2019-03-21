from SocceriaMK import *
from SocceriaMK.Supertool import Attaquant_Strategy
from SocceriaMK.Supertool import Defenseur2_Strategy
from SocceriaMK.Supertool import Defenseur1_Strategy
from SocceriaMK.Supertool import Fonceur2_Strategy
from soccersimulator import Simulation, show_simu

team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

 #Add players

team1.add("F1",Fonceur_Strategy()) 
#team1.add("D1-1",Defenseur1_Strategy()) 
team1.add("D1-2",Defenseur2_Strategy()) 
team1.add("A1",Attaquant_Strategy()) 

#team2.add("F2",Fonceur_Strategy())
team2.add("D2-1",Defenseur1_Strategy()) 
team2.add("D2-2",Defenseur2_Strategy()) 
#team2.add("A2",Attaquant_Strategy()) 
#team2.add("F2-1",Fonceur2_Strategy())


 #Create a match
simu = Simulation(team1, team2)
#Simulate and display the match
show_simu(simu) 