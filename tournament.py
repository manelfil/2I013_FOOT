from SocceriaMK import get_team
from soccersimulator import Simulation, show_simu
    

team1= get_team(1)
team2= get_team(2)

simu = Simulation( team1, team2)
show_simu(simu)