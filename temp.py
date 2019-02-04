# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math 
from Supertool import SuperState
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu


class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

class OOStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "OO")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
 
        if(SuperState.player.distance(SuperState.ball)<PLAYER_RADIUS+BALL_RADIUS):
            return SoccerAction(shoot=SuperState.goal-SuperState.player)
        else:
            return SoccerAction(acceleration=SuperState.ball-SuperState.player)
   
    
    
    
    #Vector2D(angle=0, norm=0.01)
        
          #  act2= SoccerAction(Vector2D(angle=0, norm=0.2), #vitesse
              #                 Vector2D(angle=0,norm=0.2)) #shoot

       

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
 # Random strategy
team1.add("Random", OOStrategy()) 
# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
