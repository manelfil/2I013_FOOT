#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:16:15 2019

@author: 3700629
"""
from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math
import random
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu


class SuperState(object):
    def __init__(self,state,id_team,id_player):
        self.state=state
        self.id_team=id_team
        self.id_player=id_player
        
    @property
    def ball(self):
        return self.state.ball.position

    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position

    @property
    def goal(self):
        
        if(self.id_team==2):
            return Vector2D(0,settings.GAME_HEIGHT/2)
        else:
            return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
    @property    
    def dist_pb(self): #retourne la distance entre la ball et le joueur; Pas un vecteur
        return self.ball.distance(self.player)

  #  def angle_ball(self): #calcul l'angle de la ball selon sa position dans le terrain
        
        
    @property   
    def shoot_vers_balle(self): #joueur cours vers la balle
        return self.ball-self.player #norm=vitesse du joueur
             #arctan (y.ball-y.joueur/x.ball-x.joueur): correspond a l'angle de la balle selon le joueur
    @property       
    def shoot_vers_cages(self): #tirer fort
        return self.goal-self.player 
    
    @property
    def shoot_doucement_vers_cages(self):
        
        v1= self.goal-self.player
        return v1.normalize()*0.3
    @property
    def liste_coequipier(self):
        return [self.state.player_state(id_team,id_player).position for (id_team, id_player) in self.state.players if id_team == self.id_team]
    
    @property
    def coequipier_lePlusProche(self):
        return min([(self.player.distance(player),player) for player in self.liste_coequipier])[1]
    
    @property
    def liste_op(self):
        return [self.state.player_state(id_team,id_player).position for (id_team, id_player) in self.state.players
                if id_team != self.id_team]

    @property
    def op_lePlusProche(self):
        return min([(self.player.distance(player),player) for player in self.liste_op])[1] #retourne la distance et
                                                                                           #le joueur equipe adverse le plus proche
        
    @property
    def fait_la_passe(self): #des que op le plus proche est inf ou egal a une cste, fait la passe
    
            #faire la passe si pas trop proche des cages
            # avoir une constante et ditance notre joueur et op le plus proche
        cste_op=7 #cas ou le joueur et l'opposant sont vraiment tres proche a une distance precise
        cste_op2= 12 #pr 2eme cas: si l'oposant et trop proche on evalue la distance entre notre joueur et son coequipier
        cste_coequ=15
        dist_self_coeq= self.player.distance(self.coequipier_lePlusProche)
    
        if(self.delimite_zone!=4):
            
            if(self.op_lePLusProche<cste_op): #qd opposant proche de note joueur
                return self.coequipier_lePlusProche-self.player
            
            elif(self.op_lePLusProche<cste_op2): #distance entre le joueur et l'opposant le plus proche
                if(dist_self_coeq<cste_coequ and self.op_lePlusProche.distance(self.coequipier_lePlusProche)< dist_self_coeq):
                    #si la distance ente le joueur et le coequipier est inferieur a cste_op2
                    # et distance entre l'opposant le plus proche et le coequipier le plus proche < dist_self_coeq
                        return self.coequipier_lePlusProche-self.player
                    #juste le vecteur pas encore l'action(SoccerAction)
        return Vector2D(0,0)
                
    
    @property
    def delimite_zone(self):
        
        pos_joueur= self.player
        if(self.id_team==1):
            if(pos_joueur<settings.GAME_WIDTH/4):
                return 1
            elif(pos_joueur<=2*settings.GAME_WIDTH/4):
                return 2
            elif(pos_joueur<=3*settings.GAME_WIDTH/4):
                return 3
            else:
                return 4
        
        if(self.id_team==2):
             
            if(pos_joueur>=3*settings.GAME_WIDTH/4):
                return 1
            elif(pos_joueur>=2*settings.GAME_WIDTH/4):
                return 2
            elif(pos_joueur>=settings.GAME_WIDTH/4):
                return 3
            else:
                return 4
                
                
    @property
    def get_limite(self):#retourne la limite du terrain pour le defenseur 
        if(self.id_team==1):
            return settings.GAME_WIDTH/4
        
        elif(self.id_team==2):
            return 3*settings.GAME_WIDTH/4
        


    @property
    def retour_posDef(self): #retourne la position vers laquel il doit courrir
        v=Vector2D(0,0)
        v.random(0.1,0.1)
        if(self.id_team==1):
            return Vector2D(0,settings.GAME_HEIGHT/2)+v
        
            #position du joueur
        elif(self.id_team==2):
             return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)-v
    
    
    

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())   
    

class Fonceur_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "fonceur")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        action=SoccerAction()
        action_1=SoccerAction()
        s= SuperState(state, id_team, id_player)
        if(s.player.distance(s.ball)>settings.PLAYER_RADIUS+settings.BALL_RADIUS):
            action_1= SoccerAction(acceleration=s.ball-s.player) #loin de la balle que courrir
            
        
        elif(s.ball.x>4*settings.GAME_WIDTH/5 and s.id_team==1): #shoot doucement quand pres des cages de l'adversaire
            action=SoccerAction(shoot=s.shoot_doucement_vers_cages)
                #shoot moins fort
        elif(s.ball.x<settings.GAME_WIDTH/5 and s.id_team==2):
            action=SoccerAction(shoot=s.shoot_doucement_vers_cages)
        else:
            action=SoccerAction(shoot=s.shoot_vers_cages)
            
        return action_1+action

class Attaquant_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "fonceur")
       
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s= SuperState(state, id_team, id_player) #car on l'applique a s
        action1=SoccerAction()
        
        if(s.player.distance(s.ball)<settings.PLAYER_RADIUS+settings.BALL_RADIUS) and (s.fait_la_passe!=0):
            action1=SoccerAction(shoot=s.fait_la_passe)
        action2=SoccerAction(acceleration=s.ball-s.player)
        
        return action1+action2
        
        
class Defenseur_Strategy(Strategy):   #socceraction: cours ou shoot
    def __init__(self):
        Strategy.__init__(self, "defenseur")    
    
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s= SuperState(state, id_team, id_player) #car on l'applique a s
        
     
        action1= SoccerAction(acceleration=s.ball-s.player) #cours vers la balle
        action2=SoccerAction(shoot=s.shoot_vers_cages) #shoot vers la balle
        
        if(s.ball.x<s.get_limite and s.id_team==1): #si l'adversaire au 1/4 du terrain proche des cages
            
            return action1+ action2 
    
        if(s.ball.x>s.get_limite and s.id_team==2): #si l'adversaire au 1/4 du terrain proche des cages
            
            return action1+ action2 
        
        else:
            return SoccerAction(acceleration=s.retour_posDef-s.player)
            
        return SoccerAction()     
                
  


team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

 #Add players
  #Random strategy
team1.add("F1",Fonceur_Strategy()) 
team2.add("D1",Defenseur_Strategy()) 
team2.add("F2",Attaquant_Strategy()) 
team2.add("D2",Defenseur_Strategy())
 #Create a match
simu = Simulation(team1, team2)
#Simulate and display the match
show_simu(simu) 
    