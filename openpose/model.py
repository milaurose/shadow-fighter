# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 14:33:07 2019

@author: jh
"""
import utils
import time
import cv2
import argparse
import numpy as np
import copy
from playsound import playsound


k=0
h=600
w=800
xadj=150
yadj=30
delay=0.25

pB_safe = False #not safe because can be harmed
pA_safe = False

ap=argparse.ArgumentParser()
ap.add_argument('img',type=str)
ap.add_argument('scale',type=int)
ap.add_argument('data',type=str)

args=ap.parse_args()
img_url=args.img
scale=args.scale
data_url=args.data

numbering=False

data_cap=utils.predictionGrabber(data_url).start()
img_cap=utils.frameGrabber(img_url).start()

utils.start_screen(h,w,xadj,yadj,delay)

original_img=img_cap.read()
cv2.imshow('',original_img)
cv2.waitKey(1)
h,w,d=original_img.shape
#print(h)
#print(w)
game_h=int(h*scale)
game_w=int(w*scale)
#print(game_h)
#print(game_w)

white=(1,1,1)
yellow=(0,1,1)
black=(0,0,0)
red=(0,0,1)
blue=(1,0,0)
green=(0,1,0)


bgcolor=black    
canvas=np.zeros((game_h,game_w,d))

for i in range(len(bgcolor)):
    canvas[:,:,i]=bgcolor[i]

gradius=int(h/4)
hradius=int(h/2)
thickness=int(h/3)

p1_life=100
p2_life=100

status=1
old_frame=np.zeros((game_h,game_w,d))
x_trans=100

first=True

while True:
    if p1_life==0 or p2_life==0:
#        playsound('KO.mp3')
        h=600
        w=800
        xadj=150
        yadj=30
        delay=0.25
        utils.start_screen(h,w,xadj,yadj,delay)
        p1_life=100
        p2_life=100
#        first_time=False
    
    cv2.imshow('',canvas)
    info=data_cap.read()
#    print(info)
    if info !='pass':
        persons=info.split('^')
        if len(persons)==2:
            p1=persons[0]
            p2=persons[1]
    
            joint_vec1=utils.parse_info2(p1,game_h,game_w)
            new_canvas,new_joint_vec1=utils.draw_human2(x_trans,copy.deepcopy(canvas),joint_vec1,game_h,0.4,game_h-50,gradius,hradius,thickness,blue,white)

            joint_vec2=utils.parse_info2(p2,game_h,game_w)
            new_canvas,new_joint_vec2=utils.draw_human2(x_trans,copy.deepcopy(new_canvas),joint_vec2,game_h,0.4,game_h-50,gradius,hradius,thickness,green,white)

            if new_joint_vec1 is None or new_joint_vec2 is None:
                continue
            

            health,pA_safe,pB_safe=utils.collision_detection(new_joint_vec1, new_joint_vec2, pB_safe, pA_safe,hradius)

            p1_life+=health[0]*10
            p2_life+=health[1]*10
    
            if health[0]!=0:
                if 0 in new_joint_vec1.keys():
                    head1=new_joint_vec1[0]
                    cv2.circle(new_canvas, (head1['x'],head1['y']), hradius , red, -1)
    
            if health[1]!=0:
                if 0 in new_joint_vec1.keys():
                    head2=new_joint_vec2[0]
                    cv2.circle(new_canvas, (head2['x'],head2['y']), hradius , red, -1)
                    
            
    #        print(new_joint_vec1)
    #        
            new_canvas = cv2.flip(new_canvas, 1 )
            new_canvas,msg=utils.update_hp(new_canvas, p1_life, p2_life)
            if msg!=0:
                cv2.putText(new_canvas, msg, (int(w/2), int(h/2)), cv2.FONT_HERSHEY_COMPLEX, 1, red, 5, cv2.LINE_AA)
            
            old_frame=copy.deepcopy(new_canvas)
            
            if msg!=0:
                while k<500:
                    cv2.imshow('',new_canvas)
                    cv2.waitKey(1)
                    k+=1
                k=0
            else:
                cv2.imshow('',new_canvas)
    else:
        cv2.putText(old_frame, 'PLAYER NOT DETECTED!', (int(w/2), int(h/2)), cv2.FONT_HERSHEY_COMPLEX, 1, red, 2, cv2.LINE_AA)
        cv2.imshow('',old_frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        cv2.destroyAllWindows()
        break

    
        



    
    
    
    
    

    


    


        


