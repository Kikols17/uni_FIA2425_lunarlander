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

env = gym.make("LunarLander-v3", render_mode=RENDER_MODE, 
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
    # Estes valores constantes foram obtidos a olho
    LANDING_WIDTH = 0.4
    LANGING_HEIGHT = 0.2

    SAFE_DESCENT_WIDTH = 0.2

    SAFE_ZONE_HEIGHT = 0.5

    px = observation[0]
    py = observation[1]

    perceptions = {
        'zA': px>-(LANDING_WIDTH)/2 and px<(LANDING_WIDTH)/2 and py<LANGING_HEIGHT,
        'zB': px>-(SAFE_DESCENT_WIDTH)/2 and px<(SAFE_DESCENT_WIDTH)/2,
        'zC': px>-(LANDING_WIDTH)/2 and px<-(SAFE_DESCENT_WIDTH)/2 and py>LANGING_HEIGHT and py<SAFE_ZONE_HEIGHT,
        'zD': px>(SAFE_DESCENT_WIDTH)/2 and px<(LANDING_WIDTH)/2 and py>LANGING_HEIGHT and py<SAFE_ZONE_HEIGHT,
        'zE': px<-(LANDING_WIDTH)/2 and py<SAFE_ZONE_HEIGHT,
        'zF': px>(LANDING_WIDTH)/2 and py<SAFE_ZONE_HEIGHT,
        'zG': px<-(SAFE_DESCENT_WIDTH)/2 and py>SAFE_ZONE_HEIGHT,
        'zH': px>(SAFE_DESCENT_WIDTH)/2 and py>SAFE_ZONE_HEIGHT,
        'vx': observation[2],
        'vy': observation[3],
        'a': observation[4],
        'av': observation[5],
        'l': observation[6],
        'r': observation[7]
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

    MAX_A_SPEED = 0.05
    MAX_X_SPEED = 0.005
    MAX_Y_SPEED = -0.1


    if (perceptions['zA']):
        #print("ready to land")
        action = actions['do_nothing']
    elif (perceptions['av'] > MAX_A_SPEED):
        #print("angular velocity left: " + str(perceptions['av']))
        action = actions['rotate_right']
    elif (perceptions['av'] < -MAX_A_SPEED):
        #print("angular velocity right: " + str(perceptions['av']))
        action = actions['rotate_left']
    elif (perceptions['vx'] > MAX_X_SPEED):
        #print("Going right")
        action = actions['go_left']
    elif (perceptions['vx'] < -MAX_X_SPEED):
        #print("Going left")
        action = actions['go_right']
    elif (perceptions['vy'] < MAX_Y_SPEED):
        #print("SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zB']):
        #print("safe descent")
        action = actions['do_nothing']
    elif (perceptions['zC']):
        #print("moving right to land")
        action = actions['go_right']
    elif (perceptions['zD']):
        #print("moving left to land")
        action = actions['go_left']
    elif (perceptions['zE']):
        #print("unsafe left zone, move up!")
        action = actions['main_engine']
    elif (perceptions['zF']):
        #print("unsafe right zone, move up!")
        action = actions['main_engine']
    elif (perceptions['zG']):
        #print("safe left zone, move right")
        action = actions['go_right']
    elif (perceptions['zH']):
        #print("safe right zone, move left")
        action = actions['go_left']
    
    else:
        #print("hovering")
        action = actions['do_nothing']
    return action
    
    
def keyboard_agent(observation):
    action = [0,0] 
    keys = pygame.key.get_pressed()

    perceptions = get_perceptions(observation)
    print("zone: ", end="")
    if perceptions['zA']:
        print("A", end='')
    if perceptions['zB']:
        print("B", end='')
    if perceptions['zC']:
        print("C", end='')
    if perceptions['zD']:
        print("D", end='')
    if perceptions['zE']:
        print("E", end='')
    if perceptions['zF']:
        print("F", end='')
    if perceptions['zG']:
        print("G", end='')
    if perceptions['zH']:
        print("H", end='')
    print("   " + str(observation[0]) + " " + str(observation[0]), end='')
    print()
    
    ###print('observação:',observation)
    ##print('posição:',observation[0])

    #print("position: " + str(observation[0]) + " " + str(observation[1]))
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
    
