from __future__ import print_function

import time
from sr.robot import *

a_th = 2

 #Threshold for the control of the allignment with silver token

d_th = 0.4

 #Threshold for the control of the linear distance from silver token
   
    
R = Robot()

 #instance of the class Robot
 
 
###########################################

def drive(speed, seconds):

#drive() function is used to thr robot move straight we first move then turn them down


    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################

def turn(speed, seconds):

# turn() function is used to give the motor oppositve powe to rotate the whell without any stop


    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################

# Defining find_silver_token() find the silver token later to use some grab fucntion below

def find_silver_token():

    dist = 1.2
    for token in R.see():
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70 <token.rot_y< 70:
            dist=token.dist
            rot_y=token.rot_y
    if dist == 1.2:
        return -1, -1
    else:
           return dist, rot_y

###########################################
# Defining find_golden_token() function find the golden token later to avoid the collosion from wall

def find_golden_token():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
            dist=token.dist
        rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
           return dist, rot_y

###########################################

#This function is used to not collision with golden token distance of the silver token and angle between the robot and the silver token 
#if ture the function returns true if there is a golden token inside the detecting area closer to the robot than a silver one is. 
#It also returns true if no silver tokens are detected. 
#if false the function will return false if the closest token detected by the robot is silver

def far_from_gold_token(distance,angle):
    if ( distance==-1):
    
        return True
    else:
        dist=1.2
        for token in R.see():
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and angle-30 < token.rot_y < angle+30:
                   dist=token.dist
            rot_y=token.rot_y
        if dist==1.2:
            return False
        elif (distance>dist):
            
            return True
        elif (distance<=dist):
           
            return False

###########################################
#Move Fucntion is used to robot away from wall if robot detect golden token() they see right and left 
#where the closet wall is accoreding to detection the robot move otherisde

def Move():


    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (-105 < token.rot_y < -75 or 75<token.rot_y<105):
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        print("err")
    if rot_y>=0:
        turn(-25,0.1)
        return True
    else:
        turn(25,0.1)
        return False
        
#########################################
# Defining the grab_it() routine, this is a funciton created to make the main() function code
# a little bit more conceptual rather than writing just a bunch of instructions. As you will
# see in the main() this is going to be appreciatable.
def grab_it():

	if R.grab():
	    	print("Gotcha! Grab Silver Token")
	    	turn(44, 1)
	    	drive(20, 0.9)
	    	R.release()
	    	drive(-20,0.9)
		turn(-44,1)

###########################################

#pickup_silver_token to approach to silver token and getting close as possible it 

def pickup_silver_token(silver_token):

    if silver_token < -a_th:
    
        print ("Left a bit...")
        turn(-15, 0.1)
                        
    if silver_token > a_th:
    
        print ("Right a bit...")
        turn(+15, 0.1)
        
    if(-a_th<silver_token<a_th ):
        drive(80,0.10)


###########################################


def main():

    while (1):
    
        dist_silver , silver_token = find_silver_token()
        dist_gold, rot_y_gold= find_golden_token()
        golden = far_from_gold_token(dist_silver, silver_token)
        #Periodic call of all the detectiong functions needed to get the info on the surroundings of the robot
        
        if(golden):
            # if the robot can't see any gold silver token or either there's a gold one closer. 
            if (dist_gold!=-1 and dist_gold<0.9):
             #If the robot gets closer than 0.9' to a gold wall
                 print("Robot close to the golden wall ")
                 
                 Move()
                 #Routine to get way of the wall
            
            else:
             #If the robot doesen't see neither the silver nor the gold token
              
                drive(100,0.2)
                
        
        else:
         #If the robot sees a silver token and its closer to the robot than any other gold ones

            print ("Ah Go ahaed ")
            pickup_silver_token(silver_token)
            #Aproach to the siver token

                
            if dist_silver < d_th:
            #The distance between the robot and the detected siver token lies within the given treashold, the robot will operate the grab routine
                grab_it()
                print ("Pick and Release the silver token")
                #Grabbing routine of the silver token
                
###########################################
                    
main()
