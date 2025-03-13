import gymnasium as gym
import numpy as np
import pygame

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
#RENDER_MODE = None #seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
EPISODES = 1000

totaldeath_count = 0
rollover_count = 0
horizonleft_count = 0
horizonright_count = 0
outsideleft_count = 0
outsideright_count = 0
crashonland_count = 0

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
    # ----------------------------------------------
    # Death statistics
    global totaldeath_count
    global rollover_count
    global horizonleft_count
    global horizonright_count
    global outsideleft_count
    global outsideright_count
    global crashonland_count
    totaldeath_count += 1
    if (abs(observation[4])>=np.deg2rad(20)):
        rollover_count += 1
    elif (observation[0]<-1):
        horizonleft_count += 1
    elif (observation[0]>1):
        horizonright_count += 1
    elif (observation[0]<-0.2):
        outsideleft_count += 1
    elif (observation[0]>0.2):
        outsideright_count += 1
    elif (observation[3]>-0.2):
        crashonland_count += 1
    # ----------------------------------------------

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
        'go_left': [0.1, -0.8],
        'go_right': [0.1, 0.8]
    }
    
    return actions


def reactive_agent(observation):
    ##TODO: Implemente aqui o seu agente reativo
    ##Substitua a linha abaixo pela sua implementação
    actions = get_actions()
    perceptions = get_perceptions(observation)

    ZERO_A_SPEED = 0.05     # Absolute of the speed at which the angular velocity is considered ≃0
    ZERO_X_SPEED = 0.005    # Absolute of the speed at which the x velocity is considered ≃0
    ZERO_Y_SPEED = 0.01     # Absolute of the speed at which the y velocity is considered ≃0

    MAX_A_SPEED = 0.1       # Absolute of the maximum angular velocity
    MAX_X_SPEED = 0.01      # Absolute of the maximum x velocity
    MAX_Y_SPEED = 0.1       # Absolute of the maximum y velocity


    ##### ZONE A #####
    if (perceptions['zA'] and perceptions['l'] and perceptions['r']):
        #print("landing, legs touching, on landing pad")
        action = actions['do_nothing']
    elif (perceptions['zA'] and perceptions['av'] > ZERO_A_SPEED):
        #print("landing, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zA'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("landing, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zA'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("landing, moving sideways, go left")
        action = actions['go_left']
    elif (perceptions['zA'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("landing, moving sideways, go right")
        action = actions['go_right']
    elif (perceptions['zA'] and perceptions['vy'] < -ZERO_Y_SPEED):
        #print("landing, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zA'] and perceptions['vy'] > ZERO_Y_SPEED):
        #print("landing, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zA']):
        #print("ready to land")
        action = actions['do_nothing']

    ##### ZONE B #####
    elif (perceptions['zB'] and perceptions['av'] > ZERO_A_SPEED):
        #print("safe descent, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zB'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("safe descent, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zB'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("safe descent, moving sideways, go left")
        action = actions['go_left']
    elif (perceptions['zB'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("safe descent, moving sideways, go right")
        action = actions['go_right']
    elif (perceptions['zB'] and perceptions['vy'] < -MAX_Y_SPEED):
        #print("safe descent, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zB'] and perceptions['vy'] > ZERO_Y_SPEED):
        #print("safe descent, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zB']):
        #print("safe descent")
        action = actions['do_nothing']

    ##### ZONE C #####
    elif (perceptions['zC'] and perceptions['av'] > ZERO_A_SPEED):
        #print("on the left to land, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zC'] and perceptions['av'] < -MAX_A_SPEED):
        #print("on the left to land, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zC'] and perceptions['vx'] > MAX_X_SPEED):
        #print("on the left to land, moving sideways too fast, go left")
        action = actions['go_left']
    elif (perceptions['zC'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("on the left to land, moving sideways, go right")
        action = actions['go_right']
    elif (perceptions['zC'] and perceptions['vy'] < -MAX_Y_SPEED):
        #print("on the left to land, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zC'] and perceptions['vy'] > ZERO_Y_SPEED):
        #print("on the left to land, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zC']):
        #print("on the left to land")
        action = actions['go_right']

    ##### ZONE D #####
    elif (perceptions['zD'] and perceptions['av'] > MAX_A_SPEED):
        #print("on the left to land, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zD'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("on the left to land, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zD'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("on the left to land, moving sideways, go left")
        action = actions['go_left']
    elif (perceptions['zD'] and perceptions['vx'] < -MAX_X_SPEED):
        #print("on the left to land, moving sideways too fast, go right")
        action = actions['go_right']
    elif (perceptions['zD'] and perceptions['vy'] < -MAX_Y_SPEED):
        #print("on the left to land, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zD'] and perceptions['vy'] > ZERO_Y_SPEED):
        #print("on the left to land, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zD']):
        #print("on the right to land")
        action = actions['go_left']

    ##### ZONE E #####
    elif (perceptions['zE'] and perceptions['av'] > ZERO_A_SPEED):
        #print("left of landing zone, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zE'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("left of landing zone, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zE'] and perceptions['vx'] > MAX_X_SPEED):
        #print("left of landing zone, moving sideways too fast, go left")
        action = actions['go_left']
    elif (perceptions['zE'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("left of landing zone, moving sideways, go right")
        action = actions['go_right']
    elif (perceptions['zE'] and perceptions['vy'] < -ZERO_Y_SPEED):
        #print("left of landing zone, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zE'] and perceptions['vy'] > MAX_Y_SPEED):
        #print("left of landing zone, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zE']):
        #print("left of landing zone")
        action = actions['go_right']

    ##### ZONE F #####
    elif (perceptions['zF'] and perceptions['av'] > ZERO_A_SPEED):
        #print("right of landing zone, spinning out, rotate right")
        action = actions['rotate_right']
    elif (perceptions['zF'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("right of landing zone, spinning out, rotate left")
        action = actions['rotate_left']
    elif (perceptions['zF'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("right of landing zone, moving sideways, go left")
        action = actions['go_left']
    elif (perceptions['zF'] and perceptions['vx'] < -MAX_X_SPEED):
        #print("right of landing zone, moving sideways too fast, go right")
        action = actions['go_right']
    elif (perceptions['zF'] and perceptions['vy'] < -ZERO_Y_SPEED):
        #print("right of landing zone, SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zF'] and perceptions['vy'] > MAX_Y_SPEED):
        #print("right of landing zone, stop going up")
        action = actions['do_nothing']
    elif (perceptions['zF']):
        #print("right of landing zone")
        action = actions['go_left']

    elif (perceptions['av'] > ZERO_A_SPEED):
        #print("angular velocity left: " + str(perceptions['av']))
        action = actions['rotate_right']
    elif (perceptions['av'] < -ZERO_A_SPEED):
        #print("angular velocity right: " + str(perceptions['av']))
        action = actions['rotate_left']
    elif (perceptions['vx'] > ZERO_X_SPEED):
        #print("Going right")
        action = actions['go_left']
    elif (perceptions['vx'] < -ZERO_X_SPEED):
        #print("Going left")
        action = actions['go_right']
    elif (perceptions['vy'] < -ZERO_Y_SPEED):
        #print("SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['vy'] > ZERO_Y_SPEED):
        #print("stop going up")
        action = actions['do_nothing']

    ##### ZONE G #####
    elif (perceptions['zG'] and perceptions['av'] > ZERO_A_SPEED):
        #print("angular velocity left: " + str(perceptions['av']))
        action = actions['rotate_right']
    elif (perceptions['zG'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("angular velocity right: " + str(perceptions['av']))
        action = actions['rotate_left']
    elif (perceptions['zG'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("Going right")
        action = actions['go_left']
    elif (perceptions['zG'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("Going left")
        action = actions['go_right']
    elif (perceptions['zG'] and perceptions['vy'] < ZERO_Y_SPEED):
        #print("SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zG'] and perceptions['vy'] > MAX_Y_SPEED):
        #print("stop going up")
        action = actions['do_nothing']
    elif (perceptions['zG']):
        #print("hovering")
        action = actions['main_engine']

    ##### ZONE H #####
    elif (perceptions['zH'] and perceptions['av'] > ZERO_A_SPEED):
        #print("angular velocity left: " + str(perceptions['av']))
        action = actions['rotate_right']
    elif (perceptions['zH'] and perceptions['av'] < -ZERO_A_SPEED):
        #print("angular velocity right: " + str(perceptions['av']))
        action = actions['rotate_left']
    elif (perceptions['zH'] and perceptions['vx'] > ZERO_X_SPEED):
        #print("Going right")
        action = actions['go_left']
    elif (perceptions['zH'] and perceptions['vx'] < -ZERO_X_SPEED):
        #print("Going left")
        action = actions['go_right']
    elif (perceptions['zH'] and perceptions['vy'] < ZERO_Y_SPEED):
        #print("SLOW DOWN")
        action = actions['main_engine']
    elif (perceptions['zH'] and perceptions['vy'] > MAX_Y_SPEED):
        #print("stop going up")
        action = actions['do_nothing']
    elif (perceptions['zH']):
        #print("hovering")
        action = actions['main_engine']


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
    print("   " + str(observation[0]) + " " + str(observation[1]), end='')
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

# ----------------------------------------------
# Death statistics
print()
print("##################### DEATH STATISTICS #####################")
print("Total death count: ", totaldeath_count)
print("Rollover count: ", rollover_count)
print("Horizon left count: ", horizonleft_count)
print("Horizon right count: ", horizonright_count)
print("Outside left count: ", outsideleft_count)
print("Outside right count: ", outsideright_count)
print("Crash on land count: ", crashonland_count)
print("############################################################")
# ----------------------------------------------
