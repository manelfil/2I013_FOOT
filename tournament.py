from SocceriaMK import get_team
from soccersimulator import Simulation, show_simu
    

team1= get_team(4)
team2= get_team(2)
team3= get_team(4)

simu = Simulation( team1,team3)
show_simu(simu)