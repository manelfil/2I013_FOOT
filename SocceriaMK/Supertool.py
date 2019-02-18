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
    
    def __get_attr__(self,attr):
        return getattr(self.state, attr)
        
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

###########################################################################    Differents Shoots        
        
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
###################################################################### Coequipier
    @property
    def liste_coequipier(self):
        return [self.state.player_state(id_team,id_player).position for (id_team, id_player) in self.state.players if id_team == self.id_team]
    
    @property
    def dist_coequipier_lePlusProche(self):#distance 
        return min([(self.player.distance(player),player) for player in self.liste_coequipier])[0]
    @property
    def position_coequipier_lePlusProche(self):#distance 
        v=Vector2D(0,0)
        min_dist=settings.GAME_WIDTH*2
        for k in self.liste_coequipier[0:-1]:
            if(k.distance(self.player)<min_dist and k!=self.player):
                min_dist=k.distance(self.player)
                v=k
        return v
    
    
    @property
    def dist_CoequlePlusProche_de_balle(self):
        min_dist=settings.GAME_WIDTH*2
        for k in self.liste_coequipier[0:-1]:
            if(k.distance(self.ball)<min_dist and k!=self.player):
                min_dist=k.distance(self.ball)
        return min_dist
#######################################################################  Opposant     
    @property
    def liste_op(self):
        return [self.state.player_state(id_team,id_player).position for (id_team, id_player) in self.state.players
                if id_team != self.id_team]

    @property
    def op_lePlusProche(self):
        return min([(self.player.distance(player),player) for player in self.liste_op])[0] #retourne la distance et
                                                                                           #le joueur equipe adverse le plus proche
######################################################################## utilisé dans Strategy Attaquant        
    @property
    def fait_la_passe(self): #des que op le plus proche est inf ou egal a une cste, fait la passe
    
            #faire la passe si pas trop proche des cages
            # avoir une constante et ditance notre joueur et op le plus proche
        cste_op=7 #cas ou le joueur et l'opposant sont vraiment tres proche a une distance precise
        cste_op2= 12 #pr 2eme cas: si l'oposant et trop proche on evalue la distance entre notre joueur et son coequipier
        cste_coequ=15
        dist_self_coeq= self.dist_coequipier_lePlusProche
    
        if(self.delimite_zone!=4):
            
            if(self.op_lePlusProche<cste_op): #qd opposant proche de note joueur
                return self.position_coequipier_lePlusProche-self.player
            
            elif(self.op_lePlusProche<cste_op2): #distance entre le joueur et l'opposant le plus proche
                if(dist_self_coeq<cste_coequ and self.op_lePlusProche.distance(self.dist_coequipier_lePlusProche)< dist_self_coeq):
                    #si la distance ente le joueur et le coequipier est inferieur a cste_op2
                    # et distance entre l'opposant le plus proche et le coequipier le plus proche < dist_self_coeq
                        return self.position_coequipier_lePlusProche-self.player
                    #juste le vecteur pas encore l'action(SoccerAction)
        return Vector2D(0,0)
                
########################################################################## delimite zones    
    @property
    def delimite_zone(self):
        
        pos_joueur= self.player
        if(self.id_team==1):
            if(pos_joueur.x<settings.GAME_WIDTH/4):
                return 1
            elif(pos_joueur.x<=2*settings.GAME_WIDTH/4):
                return 2
            elif(pos_joueur.x<=3*settings.GAME_WIDTH/4):
                return 3
            else:
                return 4
        
        if(self.id_team==2):
             
            if(pos_joueur.x>=3*settings.GAME_WIDTH/4):
                return 1
            elif(pos_joueur.x>=2*settings.GAME_WIDTH/4):
                return 2
            elif(pos_joueur.x>=settings.GAME_WIDTH/4):
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
        #strat  = Attaquant_Strategy()
        #return strat.compute_strategy(state, id_team, id_player)
    
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
        Strategy.__init__(self, "attaquant")
       
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s= SuperState(state, id_team, id_player) #car on l'applique a s
        action1=SoccerAction()
        action2=SoccerAction()
        action3=SoccerAction()
        
        if(s.player.distance(s.ball)>settings.PLAYER_RADIUS+settings.BALL_RADIUS):#court
            if(s.dist_CoequlePlusProche_de_balle<s.dist_pb):#court vite vers la balle car coequipier loin de la balle
                action2=SoccerAction(acceleration=s.ball-s.player)
            else: # court moins vite
                action3=SoccerAction(acceleration=(s.ball-s.player).normalize()*0.03)####probleme
        elif (s.fait_la_passe != Vector2D(0,0)):
            action1=SoccerAction(shoot=s.fait_la_passe)
        
        return action1+action3+action2
        
        
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