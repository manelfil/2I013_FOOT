from SocceriaMK import *
from SocceriaMK.Supertool import Attaquant_Strategy
from soccersimulator import Simulation, show_simu

team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

 #Add players
  #Random strategy
team1.add("F1",Fonceur_Strategy()) 
team2.add("F2",Fonceur_Strategy())
team2.add("D1",Defenseur_Strategy()) 
team1.add("A1",Attaquant_Strategy()) 
#team2.add("D2",Defenseur_Strategy())
 #Create a match
simu = Simulation(team1, team2)
#Simulate and display the match
show_simu(simu) 