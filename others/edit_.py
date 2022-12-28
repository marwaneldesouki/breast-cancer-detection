import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
folder_name = ""
font = cv2.FONT_HERSHEY_SIMPLEX

def main():
    try:
                img = cv2.imread("./Dataset/jpeg/1230/1.jpg",0) #read_img -> grayscale
                img = cv2.GaussianBlur(img,(3,3),0) #remove noise

                edges = cv2.Canny(img,0,255)#min threashold,max threashold
                rect=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                th= cv2.threshold(edges,180,255,cv2.THRESH_BINARY)[1]
                img_out = cv2.dilate(th,rect,iterations = 8)
                plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
                plt.title('original'), plt.xticks([]), plt.yticks([])
                img_out = cv2.erode(img_out, rect, iterations=7)
                plt.subplot(2,2,2),plt.imshow(img_out,cmap = 'gray')
                plt.title('eroded 7 times'), plt.xticks([]), plt.yticks([])
                img_out = cv2.dilate(img_out,rect,iterations = 2)
                plt.subplot(2,2,3),plt.imshow(img_out,cmap = 'gray')
                plt.title('dialted 2 times'), plt.xticks([]), plt.yticks([])
                # kernel = np.ones(3)
                # img_out =cv2.dilate(img_out,kernel=kernel,iterations=2)
                # img_out =cv2.erode(img_out,kernel=kernel,iterations=4)
                # img_out =cv2.dilate(img_out,kernel=kernel,iterations=20)
                img_out = img_out
                # plt.subplot(2,2,4),plt.imshow(th,cmap = 'gray')
                # plt.title('thresholded'), plt.xticks([]), plt.yticks([])
                plt.savefig('gray_plot.jpg')
                cv2.imwrite('gray.jpg',img_out)
                imS = cv2.resize(img_out, (960, 540))   
    except:
            print("x")       
main()