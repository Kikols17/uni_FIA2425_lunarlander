# Moon Lander

## Authors

- Francisco Amado Lapa Marques Silva - 2022213583 - francisco.lapamsilva@gmail.com - [PL2]
- Guilherme Fernandes Rodriges - 2022232102 - gfr04@gmail.com - [PL2]
- Miguel Teixeira de Pina Monteiro Pereira - 2022232552 - miguelmpereira0409@gmail.com - [PL2]



## Index

1. [Introduction](#introduction)
3. [Perceptions](#perception)
4. [Actions](#actions)
4. [Modulate Behaviour](#modulate)
6. [Conclusion (other information)](#conclusion)


## Introduction

TODO


## Perceptions

To manage this, we will utilize the built-in perceptions of the lander:

- **Px** - Value of the Horizontal Position, with the 0 being in between the two flags.
- **Py** - Value of the Vertical Position, in relation to the ground directly below the lander.
- **Vx** - Value of the Horizontal Velocity, with positive being to the right.
- **Vy** - Value of the Vertical Velocity, with positive being up.
- **A** - Angular Direction of the lander, positive rotation being counter-clock-wise.
- **Va** - Angular Velocity of the lander, positive rotation being counter-clock-wise.
- **L** - Left-leg is on the ground.
- **R** - Right-leg is on the ground.


## Actions

To control the Moon Lander, we use these actions:

- Mp0 - Main Motor (principal) =0.49
- Mp1 - Main Motor = 0.50
- Mp2 - Main Motor = 0.60
- Mp3 - Main Motor = 0.70
- Mp4 - Main Motor = 0.80
- Mp5 - Main Motor = 0.90
- Mp6 - Main Motor = 1.0


- Ms0 - Secondary Motor OFF =0.0

- Msl0 - Secondary Motor Left =0.49
- Msl1 - Secondary Motor Left =0.50
- Msl2 - Secondary Motor Left =0.60
- Msl3 - Secondary Motor Left =0.70
- Msl4 - Secondary Motor Left =0.80
- Msl5 - Secondary Motor Left =0.90
- Msl6 - Secondary Motor Left =1.00

- Msr0 - Secondary Motor Right =-0.49
- Msr1 - Secondary Motor Right =-0.50
- Msr2 - Secondary Motor Right =-0.60
- Msr3 - Secondary Motor Right =-0.70
- Msr4 - Secondary Motor Right =-0.80
- Msr5 - Secondary Motor Right =-0.90
- Msr6 - Secondary Motor Right =-1.00


## Production System

1.  Px≃0, Py≃0, A≃0, L, R → Mp0, Ms0 [END]
2.  Px>-1, Px<1, Py≃0, A≃0 → Mp0, Ms0 [Ready to land, shut everything off]
3.  Px>-1, Px<1, A>0 → Mpl1 [Inside Safe Zone, rotate Lander left to be upright]
4.  Px>-1, Px<1, A<0 → Mpr1 [Inside Safe Zone, rotate Lander right to be upright]
5.  Px>-0.5, Px<0.5, Vy>-0.1 → Mpr0 [Lander descending in ideal zone, in ideal speeds, keep descending]
6.  Px>-0.5, Px<0.5, Vy<-0.1 → Mpr1 [Lander descending in ideal zone, too fast, slow descend]
7.  Px>0.5, Px<1.0, Vy>-0.1   → Mpr0 [Lander descending outside ideal zone, but still acceptable, rotate to the left]
7.  Px>0.5, Px<1.0, Vy<-0.1   → Mpr1 [Lander hovering outside ideal zone, but still acceptable, rotate to the left]
8.  Px<-0.5, Px>-1.0, Vy>-0.1 → Mpr0 [Lander descending outside ideal zone, but still acceptable, rotate to the right]
8.  Px<-0.5, Px>-1.0, Vy<-0.1 → Mpr1 [Lander hovering outside ideal zone, but still acceptable, rotate to the right]
9. 
10. 
7.  Vx>0.1  → Msr1 [Lander moving to the right, rotate to the left to stand still]
8.  Vx<-0.1 → Msl1 [Lander moving to the left, rotate to the right to stand still]









## Perceptions 2

To manage this, we will utilize the built-in perceptions of the lander:

- **Zl** - Lander is in Landing Zone (-1<x<1, y<1)
- **Zdi** - Lander is in the Ideal Descent Zone(-0.5<x<0.5, y>1)
- **Zda** - Lander is in the Acceptable Descent Zone (-1<x<1, 1<y<3)
- **Zs** - Lander is in the Safe Zone (y<3)

## Production System 2
1. Zl, A≃0, L, R → Mp0, Ms0 [END]
2. Zl, A≃0 → Mp0, Ms0 [Ready to land, shut everything off]
3. Zl, A>0 → Msl1 [Rotate Lander left to be upright]
4. Zl, A<0 → Msr1 [Rotate Lander right to be upright]
5. Zdi, 
6. 
7. 
5. Px≃0, Vx≃0, Vy>-0.1, [A!!] --> Mp0
6. Px≃0, Vx≃0, Vy<-0.1, [A!!] --> Mpn
7. Px<1, Px>1, Vy>-0.1, 