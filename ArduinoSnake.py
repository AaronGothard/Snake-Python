import LocoIOT
import LocoIOT_Communicator as MSG
import time
import random


# USB Port Address
usb_str = "COM3"



def main():


    # Create Class Instances
    loco_iot = LocoIOT.LocoIOT()
    msg = MSG.IOT_Codes()

    # Connect to Controller Through USB Connection
    loco_iot.connect(usb_str)

    # Enable RGB Hardware Configuration
    loco_iot.enable(msg.SUBTYPE_LED_MATRIX)
    loco_iot.enable(msg.SUBTYPE_JOYSTICK)
    # Send Start Flag
    loco_iot.start()

    Letters={
    "A":[0,0,126,18,18,126,0,0],
    "B":[0,0,126,74,78,120,0,0],
    "C":[0,0,126,66,66,66,0,0],
    "D":[0,0,126,66,66,60,0,0],
    "E":[0,0,126,74,74,66,0,0],
    "F":[0,0,126,10,10,2,0,0],
    "G":[0,0,126,66,82,114,0,0],
    "H":[0,0,126,8,8,126,0,0],
    "I":[0,0,66,126,66,0,0,0],
    "J":[0,0,32,66,62,2,0,0],
    "K":[0,0,126,8,20,98,0,0],
    "L":[0,0,126,64,64,64,0,0],
    "M":[0,0,126,4,8,4,126,0],
    "N":[0,0,126,12,48,126,0,0],
    "O":[0,0,126,66,66,126,0,0],
    "P":[0,0,126,18,18,30,0,0],
    "Q":[0,0,126,66,66,126,64,0],
    "R":[0,0,126,18,50,92,0,0],
    "S":[0,0,94,82,82,114,0,0],
    "T":[0,0,2,126,2,0,0,0],
    "U":[0,0,126,64,64,126,0,0],
    "V":[0,0,30,96,96,30,0,0],
    "W":[0,126,64,32,64,126,0,0],
    "X":[0,0,102,24,24,102,0,0],
    "Y":[0,0,14,112,112,14,0,0],
    "Z":[0,0,66,114,78,66,0,0],
    " ":[0,0,0,0,0,0,0,0],
    "1":[0,0,0,68,126,64,0,0],
    "2":[0,0,114,82,82,94,0,0],
    "3":[0,0,66,74,74,126,0,0],
    "4":[0,0,16,24,20,126,0,0],
    "5":[0,0,78,74,74,120,0,0],
    "6":[0,0,126,82,82,114,0,0],
    "7":[0,0,2,2,2,126,0,0],
    "8":[0,0,126,74,74,126,0,0],
    "9":[0,0,30,18,18,126,0,0],
    "0":[0,0,126,66,66,126,0,0]


          }



    outcome="start"
    word="initialize"
    xpos=0
    ypos=0
    wordscroll=[]
    temprange=[]
    velox=1
    veloy=0
    fulldata=[0,0,0,0,0,0,0,0]
    live=[]

    joystick_dict = loco_iot.getData(msg.SUBTYPE_JOYSTICK)

    while(loco_iot.getData(msg.SUBTYPE_JOYSTICK)["Button J"]!=0):

        xpos=0
        ypos=0
        wordscroll=[]
        velox=1
        veloy=0
        length=1
        fulldata=[0,0,0,0,0,0,0,0]
        alldots=[]
        tempdots=[]
        count=0
        bootybackwards=[]


        applex=random.randint(0,7)
        appley=random.randint(0,7)
        print(applex)
        print(appley)
        while (outcome!="dead"):


            joystick_dict = loco_iot.getData(msg.SUBTYPE_JOYSTICK)
            #change the direction you are moving in with the joystick
            print(joystick_dict)
            if(joystick_dict['X Value']>750):

                veloy=-1
                velox=0

            elif(joystick_dict['X Value']<250):

                veloy=1
                velox=0

            if(joystick_dict['Y Value']>750):

                velox=1
                veloy=0

            elif(joystick_dict['Y Value']<250):

                velox=-1
                veloy=0

            xpos=xpos+velox
            ypos=ypos+veloy

            #Kill you if you go off of the screen
            if(ypos<0):
                ypos=7
                outcome="dead"
                break
            elif(ypos>7):
                ypos=0
                outcome="dead"
                break
            if(xpos<0):
                xpos=7
                outcome="dead"
                break
            elif(xpos>7):
                xpos=0
                outcome="dead"
                break
            fulldata=[0,0,0,0,0,0,0,0]
            coordinate=[xpos,ypos]
            alldots.append(coordinate)
            live=[]
            for i in range(len(alldots)-length,len(alldots) ):
                if(i!=len(alldots)):
                    live.append(alldots[i-1])
                    print(i)

            if(coordinate==[applex,appley]):
                length=length+1

            for i in live:
                if(i==coordinate and length>2):
                    outcome="dead"
                    break






            print(live)
            print(coordinate)
            for i in range(length):
                if(coordinate==[applex,appley]):
                    applex=random.randint(0,7)
                    appley=random.randint(0,7)
                if(applex==alldots[len(alldots)+i-length][0] and appley==alldots[len(alldots)+i-length][1]):
                    applex=random.randint(0,7)
                    appley=random.randint(0,7)
                    changeturn="yes"
                else:
                    changeturn="no"


                fulldata[alldots[len(alldots)+i-length][0]]=fulldata[alldots[len(alldots)+i-length][0]]+2**alldots[len(alldots)+i-length][1]


            if(coordinate!=[applex,appley]):
                fulldata[applex]=fulldata[applex]+2**appley















            #when you eat the apple, makes you long and makes another apple


            #if you dont eat it, show the apple on the screen



            #set the matrix
            loco_iot.setData(msg.SUBTYPE_LED_MATRIX,fulldata)


            time.sleep(0.3)

        #Print out the ourcome of the game (dead or won) in scrolling text
        word=("Score"+str(length))
        tempword=list(word.upper())
        for i in tempword:
            wordscroll=wordscroll+(Letters[i])
        for i in range(len(wordscroll)-7):
            loco_iot.setData(msg.SUBTYPE_LED_MATRIX, [wordscroll[0],wordscroll[1],wordscroll[2],wordscroll[3],wordscroll[4],wordscroll[5],wordscroll[6],wordscroll[7]])
            time.sleep(0.05)
            wordscroll.pop(0)
        outcome="restart"


    # Close USB Connection to Controller
    loco_iot.close()


# Run Main Function
main()