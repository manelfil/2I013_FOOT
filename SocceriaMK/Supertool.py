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
    def ball_norm(self):
        return self.state.ball.position.norm
    
    @property
    def ball_vitesse(self):
        return self.state.ball.vitesse

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

  
##########################################################################   Acceleration 
        
    @property   
    def court_vers_balle_anticipation(self): 
        
        if(self.ball_norm<0.5):
            return (self.ball+(self.ball_vitesse*(1*self.ball.distance(self.player))))-self.player
        return (self.ball+(self.ball_vitesse*(0.5*self.ball.distance(self.player))))-self.player





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
        return v1.normalize()*0.5
    
#    @property
#    def anticipe_balle(self):
        
###################################################################### Coequipier
    @property
    def liste_coequipier(self):
        return [self.state.player_state(id_team,id_player).position for (id_team, id_player) in self.state.players if id_team == self.id_team]
    
    @property
    def liste_coequipier_player(self):
        return [self.state.player_state(id_team,id_player) for (id_team, id_player) in self.state.players if id_team == self.id_team and id_player != self.id_player]
    
    @property
    def liste_coequipier_player_ID(self):
        return [(id_team,id_player) for (id_team, id_player) in self.state.players if id_team == self.id_team and id_player != self.id_player]
    
    @property
    def coequipier_lePlusProche(self):#player 
        cpt=-1
        min_dist=settings.GAME_WIDTH*2
        for k in self.liste_coequipier_player[0:-1]:
            if(k.position.distance(self.player)<min_dist and k.position!=self.player):
                min_dist=k.position.distance(self.player)
                cpt=cpt+1
                #print(self.liste_coequipier_player_ID[cpt])
        return self.liste_coequipier_player_ID[cpt]
#       
    
    @property
    def dist_coequipier_lePlusProche(self):#distance entre joueur et le coequip le + proche 
        return min([(self.player.distance(player),player) for player in self.liste_coequipier])[0]
   
    @property
    def position_coequipier_lePlusProche(self):#position  
        v=Vector2D(0,0)
        min_dist=settings.GAME_WIDTH*2
        for k in self.liste_coequipier[0:-1]:
            if(k.distance(self.player)<min_dist and k!=self.player):
                min_dist=k.distance(self.player)
                v=k
        #return v
        return self.state.player_state(self.coequipier_lePlusProche[0], self.coequipier_lePlusProche[1]).position
       
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
    def op_lePlusProche(self):# distance de l'opposant le + proche 
        return min([(self.player.distance(player),player) for player in self.liste_op])[0] #retourne la distance et
                     


    @property
    def position_opposant_lePlusProche(self):#position de l'opposant le + proche 
        v=Vector2D(0,0)
        min_dist=settings.GAME_WIDTH*2
        for k in self.liste_op[0:-1]:
            if(k.distance(self.player)<min_dist and k!=self.player):
                min_dist=k.distance(self.player)
                v=k
        return v   

    @property
    def op_DansLeurCamp(self): #si les opposant sont dans leur camps ou pas
        
        if(self.id_team==1):
            for k in self.liste_op:
                    if(k.x<settings.GAME_WIDTH/2):
                        return 0  #des que 1opposant du camp adverse n'est pas dans son camp on retourne 0
            return 1
        
        if(self.id_team==2):
            for k in self.liste_op:
                    if(k.x>settings.GAME_WIDTH/2):
                        return 0  #des que 1opposant du camp adverse n'est pas dans son camp on retourne 0
            return 1



                                                                   
######################################################################## utilisé dans Strategy Attaquant        
    @property
    def fait_la_passe(self): #des que op le plus proche est inf ou egal a une cste, on retourne un Vector2D pour faire la passe
    
            #faire la passe si pas trop proche des cages, et on fait toujours une passe si l'opposant est tres proche  
            # avoir une constante et distance notre joueur et op le plus proche
        cste_op=7 #cas ou le joueur et l'opposant sont vraiment tres proche 
        cste_op2= 12 #pr 2eme cas: si l'oposant est trop proche on evalue la distance entre notre joueur et son coequipier
        cste_coequ=15
        dist_self_coeq= self.dist_coequipier_lePlusProche
        
        #  on ne fait pas de passe si on est proche des cages
        if(self.delimite_zone!=4):
            
            if(self.op_lePlusProche<cste_op): #qd la distance entre opposant proche et joueur est inf a une cst petite 
                # on fait forcement une passe au coequip si opp tres proche 
                return self.position_coequipier_lePlusProche-self.player # Vector2D entre le joueur le coequip le +proche
            
            elif(self.op_lePlusProche<cste_op2): #qd la distance entre opposant proche et joueur est inf a une cst 
                if(dist_self_coeq<cste_coequ and (self.position_opposant_lePlusProche.distance(self.position_coequipier_lePlusProche))> dist_self_coeq):
                    #si la distance ente le joueur et le coequipier est inferieur a cste_op2
                    # et le coequipier est + proche du joueuer que l'opposant 
                        if(self.id_team==1): 
                            if(self.player.x>self.position_coequipier_lePlusProche.x):
                                if(self.position_opposant_lePlusProche.x<self.player.x or self.position_opposant_lePlusProche.x>self.player.x-5 ):
                                    return self.shoot_vers_cages
                        else:
                            return (self.position_coequipier_lePlusProche-self.player).normalize()*0.01
                    #juste le vecteur pas encore l'action(SoccerAction)
                elif(self.dist_pb< self.ball.distance(self.position_coequipier_lePlusProche)):# joueur est + proche de la balle que le coequipier
                        return self.shoot_vers_cages 
        return Vector2D(0,0)
                
    
    #--------------------------------------------------------------------------------------------------------------------------#
    
    @property
    def fait_la_passe2(self):
       
        cste_op=15 
        cste_def= 7
        
        #  on ne fait pas de passe si on est proche des cages
        if(self.delimite_zone!=4):
            if(self.op_lePlusProche>self.dist_coequipier_lePlusProche):
                 #qd la distance entre opposant le + proche et joueur > distance entre coequipier le + proche et joueur 
                if(self.id_team==1 and self.player.x>self.position_coequipier_lePlusProche.x):
                    if(self.player.x>=self.position_opposant_lePlusProche.x):# 10 a ete choisit
                        #print("eq1")
                        return (self.shoot_vers_cages).normalize()*0.5
                elif(self.id_team==2 and self.player.x<self.position_coequipier_lePlusProche.x):
                    if(self.player.x<= self.position_opposant_lePlusProche.x):# 10 a ete choisit
                       # print("eq2")                        
                        return (self.shoot_vers_cages).normalize()*0.5
                else: #fait la passe 
                    if(self.op_lePlusProche< cste_op and self.dist_coequipier_lePlusProche<cste_def):####### modifier la condition 
                        #print("33333")
                        return (self.position_coequipier_lePlusProche-self.player).normalize()*0.5  # Vector2D entre le joueur le coequip le +proche  normalisé et... 
                        
            
        else: 
            #print("44444")
            return (self.shoot_vers_cages).normalize()*0.05
        return Vector2D(0,0)
    
    
    #--------------------------------------------------------------------------------------------------------------------------#

########################################################################## delimite zones    
    @property
    def delimite_zone(self):#  def angle_ball(self): #calcul l'angle de la ball selon sa position dans le terrain
        # 1: zone de son terain 
        # 4: zone du terain adversaire ,zone dans laquelle il y a la cage pour shouter 
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
             #  def angle_ball(self): #calcul l'angle de la ball selon sa position dans le terrain
            if(pos_joueur.x>=3*settings.GAME_WIDTH/4):
                return 1
            elif(pos_joueur.x>=2*settings.GAME_WIDTH/4):
                return 2
            elif(pos_joueur.x>=settings.GAME_WIDTH/4):
                return 3
            else:
                return 4
                
                
    @property
    def get_limite(self):#retourne la limite du terrain  
        if(self.id_team==1):
            return settings.GAME_WIDTH/3
        
        elif(self.id_team==2):
            return 2*settings.GAME_WIDTH/3
############################################################################ fonctions utilisées dans les strategies defenseur         


    @property
    def retour_posDef(self): #retourne la position vers laquel il doit courrir
        v=Vector2D(0,0)
        v.random(0.1,0.1)
        if(self.id_team==1):
            return Vector2D(0,settings.GAME_HEIGHT/2)+v
            #position du joueur
        elif(self.id_team==2):
             return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)-v
    

    @property
    def pos_defenseur(self):  #donne les coordonnées du defenseur
        a= (self.ball.y-self.goal.y)/(self.ball.x-self.goal.x)
        #fixer x
        x=self.modif_x_def
        
        #b(ax+b)
        b=self.goal.y-(a*self.goal.x) #x et y du vecteur retour pos def
        
        #y=ax+b
        y=a*x+b
        if(self.op_DansLeurCamp==1):#pas d'opposant dans notre camp
            y= settings.GAME_HEIGHT/2
            
        return Vector2D(x,y)

    @property
    def modif_x_def(self):
        if(self.id_team==1):
            if(self.ball.x>settings.GAME_WIDTH/2): #dans le camp adversaire
                x=settings.GAME_WIDTH/6 #position x du defenseur
            elif (self.ball.x>settings.GAME_WIDTH/4):
                x=15 #position de retour de position du defenseur
        
        elif(self.id_team==2):
            if(self.ball.x<settings.GAME_WIDTH/2):
                x=5*settings.GAME_WIDTH/6
            elif (self.ball.x<3*settings.GAME_WIDTH/4):
                x=135  #position de retour de position du defenseur GAME_WIDTH-15
    
        return x

##############################################################  Strategies    

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
        #strat  = Attaquant_Strategy()#  on ne fait pas de passe si on est proche des cages
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
        
        if(s.player.distance(s.ball)>settings.PLAYER_RADIUS+settings.BALL_RADIUS):#court car ne peut pas shouter
            if(s.position_coequipier_lePlusProche.distance(s.ball)<=s.dist_pb):# coequip + proche de la balle que le joueur 
                action2=SoccerAction(acceleration=((s.ball-s.player).normalize())*0.09)# court moins vite vers la balle
            else: # joueur + proche de la balle que le joueur
                action3=SoccerAction(acceleration=((s.ball-s.player).normalize())*1)# court  vite
        elif (s.fait_la_passe != Vector2D(0,0)):#
            action1=SoccerAction(shoot=(s.fait_la_passe2))
        
        return action1+action2+action3
        
        
class Defenseur1_Strategy(Strategy):   #socceraction: cours ou shoot  shoot dans la balle #GARDIEN
    def __init__(self):
        Strategy.__init__(self, "defenseur1")    
    
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s= SuperState(state, id_team, id_player) 
        
     
        action1= SoccerAction(acceleration=s.ball-s.player) 
        action2=SoccerAction(shoot=s.shoot_vers_cages) 
        
        
        if(((s.id_team==1) and s.ball.x<(s.get_limite/2) and (s.goal.y-15)<s.ball.y and s.ball.y<(s.goal.y+15)) or (s.id_team==2 and (s.ball.x>(s.get_limite+(settings.GAME_WIDTH/3)) and (s.goal.y-15)<s.ball.y and s.ball.y<(s.goal.y+15)))):   
            return action1+ action2  
        else:
            return SoccerAction(acceleration=s.retour_posDef-s.player)
        return SoccerAction()     




class Defenseur2_Strategy(Strategy):   #socceraction: cours ou shoot  #fait la passe+shoot
    def __init__(self):
        Strategy.__init__(self, "defenseur")    
    
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s= SuperState(state, id_team, id_player)
        
       # print(s.state.strategies)
       
        action1= SoccerAction(acceleration=(s.court_vers_balle_anticipation))
        
        action2=SoccerAction(shoot=s.shoot_vers_cages) 
       # action3=SoccerAction(shoot=s.position_coequipier_lePlusProche-s.player)#shoot vers coequipier le + proche 
       # print(s.state.strategies.keys())
        #print(s.state.strategies[(s.id_team,s.id_player)])
        #si la balle est au 1/3 du terrain proche des cages, zone pour laquelle le defenseur doit reagir
        
        if((s.ball.x<s.get_limite and s.id_team==1) or (s.ball.x>s.get_limite and s.id_team==2) ): 
            if((s.dist_coequipier_lePlusProche<s.op_lePlusProche and s.ball.distance(s.player)<s.ball.distance(s.position_opposant_lePlusProche)) and s.state.strategies[(s.coequipier_lePlusProche[0]-1,s.coequipier_lePlusProche[1])]!= "defenseur1"): 
                # defenseur + proche de son coequipier que l'opposant ET la balle + proche du defenseur que l'opposant
                #if(s.id_player!=2) #if le coequipier est un defenseur1 on fait pas de passes
               # print(s.coequipier_lePlusProche)
                return action1+ SoccerAction(shoot=s.position_coequipier_lePlusProche-s.player) # defenseur court vers la balle et ensuite shout vers le coequipier + proche 
            return action1 + action2# sinon il court et et shoot vers la cage de l'autre côté du terrain 
        # sinon le defenseur revient a sa position dans la cage 
        else:
            return SoccerAction(acceleration=s.pos_defenseur-s.player) #s.pos: la position ou doit se placer le player != de s.player qui est la position ou il est deja
            
        return SoccerAction()     




class Fonceur2_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "fonceur")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        action=SoccerAction()
        action_1=SoccerAction()
        #strat  = Attaquant_Strategy()#  on ne fait pas de passe si on est proche des cages
        #return strat.compute_strategy(state, id_team, id_player)
    
        s= SuperState(state, id_team, id_player)
        if(s.player.distance(s.ball)>settings.PLAYER_RADIUS+settings.BALL_RADIUS):
            action_1= SoccerAction(acceleration=(s.ball-s.player).normalize()*0.1) #loin de la balle que courrir
            
        
        elif(s.ball.x>4*settings.GAME_WIDTH/5 and s.id_team==1): #shoot doucement quand pres des cages de l'adversaire
            action=SoccerAction(shoot=s.shoot_doucement_vers_cages)
                #shoot moins fort
        elif(s.ball.x<settings.GAME_WIDTH/5 and s.id_team==2):
            action=SoccerAction(shoot=s.shoot_doucement_vers_cages)
        else:
            action=SoccerAction(shoot=s.shoot_vers_cages)
            
        return action_1+action