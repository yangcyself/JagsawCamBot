# -^- coding:utf-8 -^-
import cv2
import matplotlib.pyplot as plt
import numpy as np
import re
from Cut import *

def RGBEqualizeHist(target):
    for i in range(3):
        target[:,:,i] = cv2.equalizeHist(target[:,:,i])
    return target

def cutout_source(source,template):
    source = RGBEqualizeHist(source)
    sAx = int(source.shape[1]*0.470)
    sAy = int(source.shape[0]*0.343)
    sBx = int(source.shape[1]*0.641)
    sBy = int(source.shape[0]*0.667)
    source = source[sAy:sBy,sAx:sBx,:]
    return source

def cutout_template_area(source,template):
    template = RGBEqualizeHist(template)
    tAx = int(template.shape[1]*0.172)
    tAy = int(template.shape[0]*0.144)
    tBx = int(template.shape[1]*0.250)
    tBy = int(template.shape[0]*0.799)

    temp = template[tAy:tBy,tAx:tBx,:]
    return temp

def cutout_template(source,template,temp_pos = None):
    temp = cutout_template_area(source,template)
    gradient = get_Gradient(temp)
    #高斯平滑&阈值分割
    blurred = cv2.blur(gradient, (5, 5))
    _, thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=cv2.contourArea, reverse=True)
    if(temp_pos is None): # display mode
        out = temp.copy()
        for i in range(min(5,len(contours))):
            t = temp.copy()
            c = contours[i]
            x,y,w,h= cv2.boundingRect(c)
            cv2.rectangle(t,(x,y),(x+w,y+h),(0,255,0),2)
            out = np.concatenate([out,t],axis = 1)
        return out
    else:
        c = contours[0]
        x,y,w,h= cv2.boundingRect(c)
        out = temp[y:y+w,x:x+w]
        temp_pos.append(x)
        temp_pos.append(y)
        # draw a bounding box arounded the detected barcode and display the image
        return out

def cutout_target(template):
    DAx = int(template.shape[1]*0.303)
    DAy = int(template.shape[0]*0.123)
    DBx = int(template.shape[1]*0.696)
    DBy = int(template.shape[0]*0.889)
    target = template[DAy:DBy,DAx:DBx,:]
    return target

def generateGaussianKernel(shape,u,cov):
    res = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            p = np.array((i,j))
            deltaS = np.sum((p-u)**2)
            res[i][j] = np.exp(-deltaS/cov)
    return res

def matching(source,template,mode="match"):
    sor = cutout_source(source,template)
    
    s_x = int(sor.shape[0]/3)
    s_y = int(sor.shape[1]/3)
    
    temp_area = cutout_template_area(source,template)
    
    temp_pos = []
    temp = cutout_template(source,template,temp_pos)
    temp_pos = (temp_pos[0]+20,temp_pos[1]+20) # change it into tuple 
    tep = cv2.copyMakeBorder(temp,10,40,10,40,cv2.BORDER_CONSTANT,value=[0,0,0])
    
    scores = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            img = sor[s_x*i:s_x*(i+1),s_y*j:s_y*(j+1),:]
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR_NORMED) #87.29 vs 85.55
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCORR) # 不好，倒数
            res = cv2.matchTemplate(tep,img,cv2.TM_CCOEFF) # 最高！
#             res = cv2.matchTemplate(tep,img,cv2.TM_CCOEFF_NORMED) # 最高！
#             res = cv2.matchTemplate(tep,img,cv2.TM_SQDIFF) # 不好
#             res = cv2.matchTemplate(tep,img,cv2.TM_SQDIFF_NORMED) # 最高，但是和后面的差距并不很大
            g = generateGaussianKernel(res.shape,np.array([15,15]),500)
            res = res * g
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            scores[i,j] = max_val
    if(mode=="match"):
        temp_pos = (temp_pos[0] + template.shape[1]*0.172 , temp_pos[1] + template.shape[0]*0.144) # add the temp area margin
        return temp_pos, scores

    source_x = np.argmax(scores)//3 # x => i 
    source_y = np.argmax(scores)%3
    source_x *= s_x
    source_y *= s_y

    source_y += temp_area.shape[1]
    
    out = np.zeros( (max(temp_area.shape[0],sor.shape[0]),
                        temp_area.shape[1]+sor.shape[1] ,3),dtype = np.uint8)
    out[0:temp_area.shape[0],0:temp_area.shape[1] ,:] = temp_area
    out[0:sor.shape[0],temp_area.shape[1]:,:] = sor
    
    cv2.line(out, temp_pos, (source_y+20,source_x+20), (0,255,0), 2) #line point: (shape1, shape0)
    return out


def findEmpty(emptypic, targetpic,threshold = 100, mode = "release"):
    #given an empty pic and compare it with the targetpic
    #decide which part is empty
    # use the background subtraction method
#     backSub = cv2.createBackgroundSubtractorKNN()
#     backSub =cv2.createBackgroundSubtractorMOG2()
#     for i in range(1, 16):
#         backSub.apply(emptypic, learningRate=0.5)
#     fgmask = backSub.apply(targetpic, learningRate=0)

#   directly substract the two picture
    tx,ty,_ = targetpic.shape
    ex,ey,_ = emptypic.shape
    commonsize = (min(tx,ex),min(ty,ey))
    fgmask = targetpic[:commonsize[0],:commonsize[1],:] - emptypic[:commonsize[0],:commonsize[1],:]
    
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)
    fgmask =  cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    (_, fgmask) = cv2.threshold(fgmask, 20, 255, cv2.THRESH_BINARY)
    fgmask =  cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, np.ones((10,10),np.uint8))
    if(mode=="debug"):
        plt.imshow(fgmask)
        plt.show()
    # cut it to be dividedable by 3
    w,h = fgmask.shape
    fgmask = fgmask[:(w//3)*3,:(h//3)*3]
    wd,hd = int(fgmask.shape[0]/3),int(fgmask.shape[1]/3)  # the width and height eash small block
    fgmask = fgmask.reshape((3,wd,3,hd))
    fgmask = fgmask.mean(axis = 3)
    fgmask = fgmask.mean(axis = 1)
    print(fgmask)
    return fgmask<threshold
    