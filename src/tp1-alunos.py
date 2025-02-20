import gymnasium as gym
import numpy as np
import pygame

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
RENDER_MODE = None #seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
    continuous=True, gravity=GRAVITY, 
    enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
    turbulence_power=TURBULENCE_POWER)


def check_successful_landing(observation):
    x = observation[0]
    vy = observation[3]
    theta = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    legs_touching = contact_left==1 and contact_right==1

    on_landing_pad = abs(x) <= 0.2

    stable_velocity = vy>-0.2
    stable_orientation = abs(theta)<np.deg2rad(20)
    stable = stable_velocity and stable_orientation
 
    if legs_touching and on_landing_pad and stable:
        print("✅ Aterragem bem sucedida!")
        return True

    print("⚠️ Aterragem falhada!")        
    return False
        
def simulate(steps=1000,seed=None, policy = None):    
    observation, _ = env.reset(seed=seed)
    for step in range(steps):
        action = policy(observation)

        observation, _, term, trunc, _ = env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observation)
    return step, success



#Perceptions
def get_perceptions(observation):
    px = observation[0]
    py = observation[1]
    vx = observation[2]
    vy = observation[3]
    a = observation[4]
    av = observation[5]
    l = observation[6]
    r = observation[7]

    perceptions = {
        'px': px,
        'py': py,
        'vx': vx,
        'vy': vy,
        'a': a,
        'av': av,
        'l': l,
        'r': r
    }
    
    return perceptions



#Actions
def get_actions():
    actions = {
        'do_nothing': [0, 0],
        'main_engine': [1.0, 0],
        'rotate_left': [0.1, -0.55],
        'rotate_right': [0.1, 0.55],
        'go_left': [0.15, -0.8],
        'go_right': [0.15, 0.8]
    }
    
    return actions


def reactive_agent(observation):
    ##TODO: Implemente aqui o seu agente reativo
    ##Substitua a linha abaixo pela sua implementação
    actions = get_actions()
    perceptions = get_perceptions(observation)
    
    #if perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['l']==1 and perceptions['r']==1:
    #    ##print("landed")
    #    action = actions['do_nothing']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2:
    #    ##print("landing at " + str(perceptions['px']) + " " + str(perceptions['py']))
    #    action = actions['do_nothing']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['a']<-0.1:
    #    ##print("turning left to land")
    #    action = actions['right_engine']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['a']>0.1:
    #    ##print("turning right to land")
    #    action = actions['left_engine']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vx']<-0.1:
    #    ##print("moving left")
    #    action = actions['right_engine']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vx']>0.1:
    #    ##print("moving right")
    #    action = actions['left_engine']
#
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vy']>-0.1:
    #    ##print("descending slowly in the middle")
    #    action = actions['do_nothing']
    #elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vy']<-0.3:
    #    ##print("descending too fast in the middle")
    #    action = actions['main_engine']
    #else:
    #    ##print("hovering")
    #    action = actions['do_nothing']
    ##if perceptions['vy']<-0.1:
    ##    ###print("slowing descent")
    ##    action = actions['main_engine']
    ##elif perceptions['a']>0.1:
    ##    ###print("correcting angle to the right")
    ##    action = actions['right_engine']
    ##elif perceptions['a']<-0.1:
    ##    ###print("correcting angle to the left")
    ##    action = actions['left_engine']
    ##else:
    ##    ###print("hovering")
    ##    action = actions['do_nothing']
    ######if perceptions['l']==1 and perceptions['r']==1:
    ######    ##print("landed")
    ######    action = actions['do_nothing']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['a']<-0.1 and perceptions['a']<-0.1:
    ######    ##print("landing at " + str(perceptions['px']) + " " + str(perceptions['py']))
    ######    action = actions['do_nothing']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['a']<-0.1:
    ######    ##print("turning left to land")
    ######    action = actions['rotate_right']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['py']<0.2 and perceptions['a']>0.1:
    ######    ##print("turning right to land")
    ######    action = actions['rotate_left']
    ######
    ######elif perceptions['a']>0.1:
    ######    ##print("correcting angle to the right")
    ######    action = actions['rotate_right']
    ######elif perceptions['a']<-0.1:
    ######    ##print("correcting angle to the left")
    ######    action = actions['rotate_left']
######
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vx']<-0.1:
    ######    ##print("moving left")
    ######    action = actions['rotate_right']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vx']>0.1:
    ######    ##print("moving right")
    ######    action = actions['rotate_left']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vy']<-0.3:
    ######    ##print("descending too fast in the middle")
    ######    action = actions['main_engine']
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vy']>-0.1:
    ######    ##print("descending slowly in the middle")
    ######    action = actions['do_nothing']
    ######
    ######elif perceptions['px']>-0.1 and perceptions['px']<0.1 and perceptions['vx']>-0.1 and perceptions['vx']<0.1:
    ######    ##print("hovering")
    ######    action = actions['do_nothing']
######
    ######elif perceptions['px']<-0.1 and perceptions['vx']<0.0:
    ######    ##print("moving left")
    ######    action = actions['go_right']
    ######elif perceptions['px']<-0.1 and perceptions['vx']>0.0:
    ######    ##print("moving right")
    ######    action = actions['do_nothing']
    ######elif perceptions['px']>0.1 and perceptions['vx']<0.0:
    ######    ##print("moving left")
    ######    action = actions['do_nothing']
    ######elif perceptions['px']>0.1 and perceptions['vx']>0.0:
    ######    ##print("moving right")
    ######    action = actions['go_left']
######
    ######else:
    ######    ##print("hovering")
    ######    action = actions['do_nothing']

    #print("position: " + str(perceptions['px']) + " " + str(perceptions['py']))

    LANDING_SIZE = 0.4
    LANDER_SIZE = 0.04
    #print("position: " + str(perceptions['px']) + " " + str(perceptions['py']))
    if (perceptions['px']>-(LANDING_SIZE-LANDER_SIZE)/2 and perceptions['px']<(LANDING_SIZE-LANDER_SIZE)/2 and perceptions['py']<LANDING_SIZE/2):
        #print("landed")
        action = actions['do_nothing']
    elif (perceptions['av'] > 0.01):
        #print("angular velocity left: " + str(perceptions['av']))
        action = actions['rotate_right']
    elif (perceptions['av'] < -0.01):
        #print("angular velocity right: " + str(perceptions['av']))
        action = actions['rotate_left']
    ##elif (perceptions['px']<-(LANDING_SIZE)/2 and perceptions['py']<LANDING_SIZE):
    ##    #print("too low, left of landing pad, up")
    ##    action = actions['main_engine']
    ##elif (perceptions['px']>(LANDING_SIZE)/2 and perceptions['py']<LANDING_SIZE):
    ##    #print("too low, right of landing pad, up")
    ##    action = actions['main_engine']
    elif (perceptions['vx'] > 0.01):
        #print("Going right")
        action = actions['go_left']
    elif (perceptions['vx'] < -0.01):
        #print("Going left")
        action = actions['go_right']
    elif (perceptions['vy'] < -0.1):
        #print("SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['px'] < -0.1):
        #print("going left to land")
        action = actions['go_right']
    elif (perceptions['px'] > 0.1):
        #print("going right to land")
        action = actions['go_left']
    #elif (perceptions['px'] > -0.1 and perceptions['px'] < 0.1 and perceptions['py'] < 0.1):
    #    #print("landing")
    #    action = actions['do_nothing']
    #elif (perceptions['px'] < -0.1 ):
    #    #print("moving left to land")
    #    action = actions['go_left']
    #elif (perceptions['px'] > 0.1):
    #    #print("moving right to land")
    #    action = actions['go_right']
    else:
        #print("hovering")
        action = actions['do_nothing']
    return action
    
    
def keyboard_agent(observation):
    action = [0,0] 
    keys = pygame.key.get_pressed()
    
    ###print('observação:',observation)
    ##print('posição:',observation[0])

    print("position: " + str(observation[0]) + " " + str(observation[1]))
    if keys[pygame.K_UP]:  
        action += np.array([1,0])
    if keys[pygame.K_LEFT]:  
        action += np.array( [0,-1])
    if keys[pygame.K_RIGHT]: 
        action += np.array([0,1])

    return action
    

success = 0.0
steps = 0.0
for i in range(EPISODES):
    st, su = simulate(steps=1000000, policy=reactive_agent)
    if su:
        steps += st
    success += su
    
    if su>0:
        print('Média de passos das aterragens bem sucedidas:', steps/(su*(i+1))*100)
    print('Taxa de sucesso:', success/(i+1)*100)
    
