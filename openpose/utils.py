# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 13:29:35 2019

@author: jh
"""
from threading import Thread
import cv2
import requests
import numpy as np
import math
import time
#from playsound import playsound

# Return true if line segments AB and CD intersect
def not_intersect(A,B,C,D):
    return ccw(A,C,D) == ccw(B,C,D) and ccw(A,B,C) == ccw(A,B,D)

def ccw(A,B,C):
    return (C["y"]-A["y"]) * (B["x"]-A["x"]) > (B["y"]-A["y"]) * (C["x"]-A["x"])

def collision_detection(pA, pB, pB_safe, pA_safe,radius):
  health = [0,0]
  #return an array for how many points to deduct from health bar
  if 0 in pA.keys() and 4 in pA.keys() and 7 in pA.keys() and 0 in pB.keys() and 4 in pB.keys() and 7 in pB.keys():  

      pA_head = pA[0]
      pA_rf = pA[7]
      pA_lf = pA[4]
      pB_head = pB[0]
      pB_rf = pB[7]
      pB_lf = pB[4]
#      pA_midbody = {"x": (pA[1]["x"] + pA[8]["x"])/2, "y": (pA[1]["y"] + pA[8]["y"])/2}
#      pB_midbody = {"x": (pB[1]["x"] + pB[8]["x"])/2, "y": (pB[1]["y"] + pB[8]["y"])/2}
      #before recording a collision, make sure that the hit isn't being blocked
      #check that pA is not blocking person B
#      blockA_la_lf = not_intersect(pA[3], pA[4], pB[3], pB[4])
#      blockA_ra_lf = not_intersect(pA[6], pA[7], pB[3], pB[4])
#      blockA_la_rf = not_intersect(pA[3], pA[4], pB[6], pB[7])
#      blockA_ra_rf = not_intersect(pA[6], pA[7], pB[6], pB[7])
#      
      #person A hits B head
      dist_pA_lfist_pB_head = math.hypot(pB_head["x"] - pA_lf["x"], pB_head["y"] - pA_lf["y"])
      dist_pA_rfist_pB_head = math.hypot(pB_head["x"] - pA_rf["x"], pB_head["y"] - pA_rf["y"])
#      print(dist_pA_lfist_pB_head)
#      print(dist_pA_rfist_pB_head)
      if (dist_pA_lfist_pB_head<radius or dist_pA_rfist_pB_head<radius) :
        if pB_safe==False:  
          health[1]=-1
          pB_safe = True
          print('aaaaaaaaaaaaaaaaaaaaaaaaaa')

      else:
        pB_safe = False
        
        
#      #person B hits A head
      dist_pB_lfist_pA_head = math.hypot(pA_head["x"] - pB_lf["x"], pA_head["y"] - pB_lf["y"])
      dist_pB_rfist_pA_head = math.hypot(pA_head["x"] - pB_rf["x"], pA_head["y"] - pB_rf["y"])
##      print(dist_pB_lfist_pA_head)
##      print(dist_pB_rfist_pA_head)
      if (dist_pB_lfist_pA_head<radius or dist_pB_rfist_pA_head<radius) :
        if pA_safe==False:  
          health[0]=-1
          pA_safe = True
          print('bbbbbbbbbbbbbbbbbbbbbbbb')
#
      else:
        pA_safe = False
#        
#      #person A hits B midbody
#      dist_pA_lfist_pB_midbody = math.hypot(pB_midbody["x"] - pA_lf["x"], pB_midbody["y"] - pA_lf["y"])
#      dist_pA_rfist_pB_midbody = math.hypot(pB_midbody["x"] - pA_rf["x"], pB_midbody["y"] - pA_rf["y"])
#      if (dist_pA_lfist_pB_midbody<radius or dist_pA_rfist_pB_midbody<radius) :
#        if pB_safe==False and (blockA_la_lf or blockA_ra_lf or blockA_la_rf or blockA_ra_rf):  
#          health[1]=-1
#          pB_safe = True
#      else:
#        pB_safe = False
#     
#      #person B hits A midbody
#      dist_pB_lfist_pA_midbody = math.hypot(pA_midbody["x"] - pB_lf["x"], pA_midbody["y"] - pB_lf["y"])
#      dist_pB_rfist_pA_midbody = math.hypot(pA_midbody["x"] - pB_rf["x"], pA_midbody["y"] - pB_rf["y"])
#      if (dist_pB_lfist_pA_midbody<radius or dist_pB_rfist_pA_midbody<radius) :
#        if pA_safe==False and (blockA_la_lf or blockA_ra_lf or blockA_la_rf or blockA_ra_rf):  
#          health[1]=-1
#          pA_safe = True
#      else:
#        pA_safe = False
#        
#      
      return health, pA_safe, pB_safe  
  else:
      return [0,0],False,False

def parse_info(p):
    p=p.replace('<','')
    p=p.replace('>','')
    info=p.split('|')

    
    joint_info={}
    for piece in info:
        joint=piece.split(',')
        joint_id=int(joint[0])
        joint_x=(float(joint[1]))
        joint_y=(float(joint[2]))
        subdict={'x':joint_x,'y':joint_y}
        joint_info[joint_id]=subdict
    return joint_info



def parse_parts(incoming,original,canvas):
    original_h,original_w,_=original.shape
    canvas_h,canvas_w,_=canvas.shape
    
    scale_h=canvas_h/original_h
    scale_w=canvas_w/original_w
    scale=min(scale_h,scale_w)
    
    parts={}
    info=incoming.split('|')
    for message in info:
        data=message.split(',')
        part_id=int(data[0])
        part_x=int(float(data[1])*original_w*scale)
        part_y=int(float(data[2])*original_h*scale)
        part_score=float(data[3])
        subdict={'x':part_x,'y':part_y,'score':part_score}
        parts[part_id]=subdict
    
    return parts,scale

def parse_info2(p,h,w):
    p=p.replace('<','')
    p=p.replace('>','')
    info=p.split('|')

    
    joint_info={}
    for piece in info:
        joint=piece.split(',')
        joint_id=int(joint[0])
        joint_x=int((float(joint[1])*w))
        joint_y=int((float(joint[2])*h))
        subdict={'x':joint_x,'y':joint_y}
        joint_info[joint_id]=subdict
    return joint_info


def draw_human2(x_trans,img,parts,screen_height,human_ratio,base,gradius,hradius,thickness,line_color,gcolor,numbering=False):
    connections=[(0,1),(1,2),(1,5),(1,8),(1,11),(2,3),(3,4),(5,6),(6,7),(8,9),(9,10),(11,12),(12,13)]
    keys=list(parts.keys())
    
    
    X=[]
    Y=[]
    for i in parts.keys():
        if i<14:
            joint=parts[i]
            joint_x=int(joint['x'])
            joint_y=int(joint['y'])
            X.append(joint_x)
            Y.append(joint_y)
    original_height=max(Y)-min(Y)
    print(original_height)
    if original_height>0:
        target_height=screen_height*human_ratio
        h_scale=target_height/original_height
        
        for i in parts.keys():
            parts[i]['x']=int(parts[i]['x']*h_scale)
            parts[i]['y']=int(parts[i]['y']*h_scale)
        
        X=[]
        Y=[]
        for i in parts.keys():
            if i<14:
                joint=parts[i]
                joint_x=int(joint['x'])
                joint_y=int(joint['y'])
                X.append(joint_x)
                Y.append(joint_y)
        foot=max(Y)
        y_trans=base-foot
        for i in parts.keys():
            parts[i]['y']=int(parts[i]['y']+y_trans)
            parts[i]['x']=int(parts[i]['x']+x_trans)
           
        for pair in connections:
    #        print(pair)
            start=pair[0]
            end=pair[1]
            if start in keys and end in keys:
                x1=int(parts[start]['x'])
                x2=int(parts[end]['x'])
                y1=int(parts[start]['y'])
                y2=int(parts[end]['y'])
                cv2.line(img, (x1, y1), (x2, y2), line_color , thickness)
                
        if 4 in parts.keys() and 7 in parts.keys():
            rhand=parts[4]
            lhand=parts[7]
    
            cv2.circle(img, (rhand['x'],rhand['y']), gradius , gcolor, -1)
            cv2.circle(img, (lhand['x'],lhand['y']), gradius , gcolor, -1)
        
        if 0 in parts.keys():
            head=parts[0]
    
            cv2.circle(img, (head['x'],head['y']), hradius , line_color, -1)
    
        return img, parts
    else:
        return img,None


def draw_human(img,parts,h,w,numbering=False):
    connections=[(0,1),(1,2),(1,5),(1,8),(1,11),(2,3),(3,4),(5,6),(6,7),(8,9),(9,10),(11,12),(12,13)]
    keys=list(parts.keys())
#    print(keys)
    thickness=4
    line_color=(0,255,0)
    joint_color=(0,255,255)
    radius=int(2)
    
    for i in parts.keys():
        if i<14:
            joint=parts[i]
            joint_x=int(joint['x']*w)
            joint_y=int(joint['y']*h)
#            print(joint_x)
#            print(joint_y)
            cv2.circle(img, (joint_x,joint_y), radius , joint_color, -1)
            if numbering:
                cv2.putText(img,str(i), (joint_x,joint_y),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)


    for pair in connections:
#        print(pair)
        start=pair[0]
        end=pair[1]
        if start in keys and end in keys:
            x1=int(parts[start]['x']*w)
            x2=int(parts[end]['x']*w)
            y1=int(parts[start]['y']*h)
            y2=int(parts[end]['y']*h)
            cv2.line(img, (x1, y1), (x2, y2), line_color , thickness)

    return img


class frameGrabber:
    
    def __init__(self,url):
        self.r=requests.get(url,stream=True)
        self.img=None
        self.stopped=False
        print(self.r.status_code)       
                  
        
    def start(self):
        print('starting thread')
        t=Thread(target=self.update,args=())
        t.setDaemon(True)
        t.start()
        print('thread started')
        return self
       
    def update(self):
        while True:
            if self.stopped==True:
                return
            else:
                img_bytes=bytes()
                for chunk in self.r.iter_content(chunk_size=1024):
                    img_bytes+=chunk
                    a=img_bytes.find(b'\xff\xd8')
                    b=img_bytes.find(b'\xff\xd9')
                    if a!=-1 and b!=-1:
                        jpg=img_bytes[a:b+2]
                        img_bytes=img_bytes[b+2:]
                        self.img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_COLOR)
    def read(self):
        return self.img
    
    def stop(self):
        self.stopped=True
        
class predictionGrabber(frameGrabber):
          
    def update(self):
        while True:
            if self.stopped==True:
                return
            else:
                msg=bytes()
                for chunk in self.r.iter_content():
                    msg+=chunk
                    a=msg.find(b'$')
                    b=msg.find(b'&')
                    if a!=-1 and b!=-1:
                        val=msg[a+1:b]
                        msg=msg[b+1:]
                        self.img=val.decode()

def update_hp(img, score1, score2):
  
  max_1 = 200
  max_2 = 500
  
  #player 1 score
  img = cv2.rectangle(img,(max_1-100,450),(max_1,500),(0,255,0),cv2.FILLED)
  img = cv2.rectangle(img,(max_1-100+score1,450),(max_1,500),(0,0,255), cv2.FILLED)
  
  img = cv2.rectangle(img,(max_2-100,450),(max_2,500),(0,255,0),cv2.FILLED)
  img = cv2.rectangle(img,(max_2+score2-100,450),(max_2,500),(0,0,255), cv2.FILLED)
  
  if score1==100:
      
    img = cv2.rectangle(img,(max_1-100,450),(max_1,500),(0,255,0),cv2.FILLED)
  if score2==100:
    img = cv2.rectangle(img,(max_2-100,450),(max_2,500),(0,255,0
                        ),cv2.FILLED)
  
  if score1 <= 0 and score2!=0:
      cv2.putText(img, 'K.O!', (120, 200), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
      msg='PLAYER 2 WINS!!!'
      return img,msg
  elif score2 <= 0 and score1!=0:
      cv2.putText(img, 'K.O!', (120, 200), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
      msg='PLAYER 1 WINS!!!'
      return img,msg
  elif score1<=0 and score2<=0:
      cv2.putText(img, 'K.O!', (120, 200), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
      msg='DRAW!!!'
      return img,msg
  else:
      return img,0

def start_screen(h,w,xadj,yadj,delay):
    cute_img = cv2.imread("cute_no_background.png")
    small = cv2.resize(cute_img, (0,0), fx=0.2, fy=0.2)
    while True:
        img = np.zeros((h,w,3), np.uint8)
        cv2.putText(img, 'Welcome to', (150+xadj, 100+yadj), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA);
        cv2.putText(img, 'SHADOW FIGHTER!', (30+xadj, 200+yadj), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 5, cv2.LINE_AA);
        y_offset=230+yadj
        x_offset=130+xadj
        img[y_offset:y_offset+small.shape[0], x_offset:x_offset+small.shape[1]] = small
        cv2.imshow('',img)
        if cv2.waitKey(1) & 0xff == ord('\r'):
            print('ahhh')
            break
        time.sleep(delay)
        
        cv2.putText(img, 'Press enter to start', (100+xadj, 450+yadj), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA);
        cv2.imshow('',img)
        if cv2.waitKey(1) & 0xff == ord('\r'):
            print('ahhh')
            break
        time.sleep(delay)
    
        
        img = np.zeros((h,w,3), np.uint8)
        cv2.putText(img, 'Welcome to', (150+xadj, 100+yadj), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA);
        cv2.putText(img, 'SHADOW FIGHTER!', (30+xadj, 200+yadj), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 5, cv2.LINE_AA);
        y_offset=230+yadj
        x_offset=130+xadj
        img[y_offset:y_offset+small.shape[0], x_offset:x_offset+small.shape[1]] = small
        cv2.imshow('',img)
        if cv2.waitKey(1) & 0xff == ord('\r'):
            print('ahhh')
            break
        time.sleep(delay)
        
    
    
    
    img2 = np.zeros((h,w,3), np.uint8)
    cv2.putText(img2, '3', (160+xadj, 300+yadj), cv2.FONT_HERSHEY_TRIPLEX, 8, (0, 0, 255), 4, cv2.LINE_AA);
    cv2.imshow('',img2)
    cv2.waitKey(1)
    #
    img2 = np.zeros((h,w,3), np.uint8)
    cv2.putText(img2, '2', (160+xadj, 300+yadj), cv2.FONT_HERSHEY_TRIPLEX, 8, (0, 0, 255), 4, cv2.LINE_AA);
    cv2.imshow('',img2)
    time.sleep(1)
    cv2.waitKey(1)
    
    img2 = np.zeros((h,w,3), np.uint8)
    cv2.putText(img2, '1', (160+xadj, 300+yadj), cv2.FONT_HERSHEY_TRIPLEX, 8, (0, 0, 255), 4, cv2.LINE_AA);
    cv2.imshow('',img2)
    time.sleep(1)
    cv2.waitKey(1)
    #
    img2 = np.zeros((h,w,3), np.uint8)
    cv2.putText(img2, 'FIGHT!', (40+xadj, 300+yadj), cv2.FONT_HERSHEY_TRIPLEX, 4, (0, 0, 255), 4, cv2.LINE_AA);
    time.sleep(1)
    cv2.imshow('',img2)
    cv2.waitKey(1)
    time.sleep(1)
#    cv2.destroyAllWindows()

