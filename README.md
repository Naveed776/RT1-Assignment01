# RT1-Assignment01

# Python Robotics Simulator
# Professor. Carmine Recchiuto

This is a simple, portable robot simulator developed by Student Robotics. Some of the arenas and the exercises have been modified for the Research Track I course

# Assignment

The aim of this project was to code a python script capable of making holomonic robot that move the enviorment to pickup the silver token and avoid from golden token The behavior of the robot has to stand by the following rules:

constantly driving the robot around the environment in the counter-clockwise direction,
Avoiding the gold tokens,
And once the robot will get close enough to a silver token, it should grab it and move it behind itself. enivorment
![enivorment](https://user-images.githubusercontent.com/91262613/151734072-f01ee69f-a18b-4a20-a712-bd72933b8bf0.png)

### Installing and running

The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.

Pygame, unfortunately, can be tricky (though not impossible) to install in virtual environments. If you are using pip, you might try pip install hg+https://bitbucket.org/pygame/pygame, or you could use your operating system's package manager. Windows users could use Portable Python. PyPyBox2D and PyYAML are more forgiving, and should install just fine using pip or easy_install.

## How to Run the Assignment

To run one or more scripts in the simulator, use run.py, passing it the file names. When done, you can run the program with:

`$ python run.py Assignment01.py`

Troubleshooting
When running python run.py , you may be presented with an error: ImportError: No module named 'robot'. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:

(Find the location of srtools: pip show sr.tools

Get the location. In my case this was /usr/local/lib/python2.7/dist-packages

Create symlink: ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/)

## Robot API
The API for controlling a simulated robot is designed to be as similar as possible to the SR API.

## Motors
The simulated robot has two motors configured for skid steering, connected to a two-output Motor Board. The left motor is connected to output 0 and the right motor to output 1.

The Motor Board API is identical to that of the SR API, except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```
## how to drive the robot

I used drive function to drive the robot

from this Code
```python def drive(speed, seconds)
 R.motors[0].m0.power = speed
 R.motors[0].m1.power = speed
 time.sleep(seconds)
 R.motors[0].m0.power = 0
 R.motors[0].m1.power = 0
 ```
* speed: represents the speed at which the wheels will spin.
* seconds: represents the time intervel in seconds during the which the wheel spin.
from this code the wheel turn
```python
def turn(speed, seconds):
 R.motors[0].m0.power = speed
 R.motors[0].m1.power = -speed
 time.sleep(seconds)
 R.motors[0].m0.power = 0
 R.motors[0].m1.power = 0
 ```
* `speed`: represents the speed at which the wheels will spin.
* `seconds`: represents the time intervel in seconds during the which the wheel spin.

## The Grabber
The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the R.grab method:
```python
    def grab_it():
    R.grab():
	    	print("Gotcha! Grab Silver Token")
	    	turn(44, 1)
	    	drive(20, 0.9)
	    	R.release()
	    	drive(-20,0.9)
		turn(-44,1)
 ```
grab_it() is used to grab the silver token and place them the back of the robot and avoiding the wall and follow the silver token chnage the direction left or right

```python
success = R.grab()
```

The `R.grab `function returns True if a token was successfully picked up, or False otherwise. If the robot is already holding a token, it will throw an AlreadyHoldingSomethingException.

To drop the token, call the R.release method.

Cable-tie flails are not implemented.

### FIND_SILVER_TOKEN
This function will detect the closest silver token to the center of the robot within a defined area in front of it. In the following example, we can see how to cycle all the Data contained in the R.see() until we find the closest token to the robot.
```python
def find_token():
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
        rot_y=token.rot_y
    if dist==100:
    return -1, -1
    else:
       return dist, rot_y 
```
### FIND_GOLDEN_TOKEN

This function works in a similar way to find_silver_token() but for gold tokens. Thanks to this function, the robot will detect the closest gold token to the center of the robot within a defined area. The main difference between find_silver_token() and find_golden_token() is the wider detecting area of 90° degrees compared to the 90° degrees of the other one. find_golden_token() is used inside the main() function to check if the robot got too close to the wall. This function will tell the robot whether it has to change direction to get away of a wall (turns()) or if it has to drive straight(drive())
```python
def find_golden_token():

    dist= 1.2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -45 < token.rot_y < 45:
            dist=token.dist
        rot_y=token.rot_y
    if dist== 1.2:
        return -1, -1
    else:
           return dist, rot_y
```

### GO_AWAY_FROM_GOLDEN_TOKEN
This function is used to not collision with golden token distance of the silver token and angle between the robot and the silver token if ture the function returns true if there is a golden token inside the detecting area closer to the robot than a silver one is. It also returns true if no silver tokens are detected. if false the function will return false if the closest token detected by the robot is silver
```python
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
 ```
### MOVE

Move Fucntion is used to robot away from wall if robot detect golden token() they see right and left where the closet wall is accoreding to detection the robot move otherisde
```python
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
```
### PICKUP_SILVER_TOKEN
The function is used to pickup the silver token seee the silver token and get the direction and then go ahed and grab the silver token
```python
    def pickup_silver_token(silver_token):

    if silver_token < -a_th:
    
        print ("Left a bit...")
        turn(-15, 0.1)
                        
    if silver_token > a_th:
    
        print ("Right a bit...")
        turn(+15, 0.1)
        
    if(-a_th<silver_token<a_th ):
        drive(80,0.10)
```
### MAIN
The Main() function is used to consist update the data through while it divided in some steps Step 1

Begining the while loop

Step 2

The call of all the functions needed to make the robot aware of its surroundings at every moment during its action. There are two different data sets about the position of the closest gold token. The only difference between the two is the angle within which the function detects the closest gold token. These sets are used at different points of the code.
```python
     dist_silver , silver_token = find_silver_token()
        dist_gold, rot_y_gold= find_golden_token()
        golden = far_from_gold_token(dist_silver, silver_token)
Step 3 Thanks to the return function if golden fucntion is near to the robot robot go away from the wall if its near to the silver token pickup the silver token and drive smothly

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
```
### Vision
To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
