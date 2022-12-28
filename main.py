import cv2
import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
folder_name = ""
def erode(image):
    opencvImage = np.array(image)
    rect=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_out = cv2.erode(opencvImage,rect,iterations = 1)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
    img_out = Image.fromarray(img_out)
    return img_out
def dilate(image):
    opencvImage = np.array(image)
    rect=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_out = cv2.dilate(opencvImage,rect,iterations = 1)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
    img_out = Image.fromarray(img_out)
    return img_out

def main():
    for path, subdirs, files in os.walk("./Dataset/jpeg"):
        try:
            folder_name = path.split('\\')[1]
            for name in files:
                img = cv2.imread(os.path.join(path, name),0) #read_img -> grayscale
                img = cv2.GaussianBlur(img,(3,3),0) #remove noise

                edges = cv2.Canny(img,0,255)#min threashold,max threashold
                th= cv2.threshold(edges,180,255,cv2.THRESH_BINARY)[1]
                rect=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                img_out = cv2.dilate(th,rect,iterations = 8)
                img_out = cv2.erode(img_out, rect, iterations=7)
                img_out = cv2.dilate(img_out,rect,iterations = 2)
                # kernel = np.ones(3)
                # img_out =cv2.dilate(img_out,kernel=kernel,iterations=2)
                # img_out =cv2.erode(img_out,kernel=kernel,iterations=4)
                # img_out =cv2.dilate(img_out,kernel=kernel,iterations=20)
                img_out = img_out
                # plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
                # plt.title('original'), plt.xticks([]), plt.yticks([])
                # plt.subplot(2,2,2),plt.imshow(img_out,cmap = 'gray')
                # plt.title('img_out'), plt.xticks([]), plt.yticks([])
                # plt.subplot(2,2,3),plt.imshow(edges,cmap = 'gray')
                # plt.title('edges'), plt.xticks([]), plt.yticks([])
                # plt.subplot(2,2,4),plt.imshow(th,cmap = 'gray')
                # plt.title('thresholded'), plt.xticks([]), plt.yticks([])
                # plt.savefig('img_3.png')
                i0mS = cv2.resize(img_out, (960, 540))   
                print(path)
                cv2.imshow("asda",imS)
                k = cv2.waitKey(0)
                if k == 27:         # wait for ESC key to exit
                    cv2.destroyAllWindows()
                elif k == ord('0'): # save in 0
                    cv2.imwrite(f'.\Dataset\\0\{folder_name+"_"+name}',img_out)
                    cv2.destroyAllWindows()
                    break
                elif k == ord('1'): # save in 1
                    cv2.imwrite(f'.\Dataset\\1\{folder_name+"_"+name}',img_out)
                    cv2.destroyAllWindows()
                elif k==ord("3"): #skip
                    cv2.imwrite(f'.\Dataset\\3\{folder_name+"_"+name}',img_out)
                    cv2.destroyAllWindows()
                elif k==ord('2'): #edit mode
                    print("edit mode")
                    while k!=ord('0'): 
                        k = cv2.waitKey(0)
                        if(k==ord('+')): #erode photo
                            img_out = cv2.erode(img_out, rect, iterations=1)
                            cv2.destroyAllWindows()
                            imS = cv2.resize(img_out, (960, 540))   
                            cv2.imshow("eroded",imS)
                        elif(k==ord('-')): #dilate photo
                            img_out = cv2.dilate(img_out, rect, iterations=1)
                            cv2.destroyAllWindows()
                            imS = cv2.resize(img_out, (960, 540))   
                            cv2.imshow("dilated",imS)
                        elif(k==ord('1')):
                            cv2.imwrite(f'.\Dataset\\1\{folder_name+"_"+name}',img_out)
                            cv2.destroyAllWindows()
                            break
                        elif(k==ord('0')):
                            cv2.imwrite(f'.\Dataset\\0\{folder_name+"_"+name}',img_out)
                            cv2.destroyAllWindows()
                            break
                        elif(k==ord("3")):
                            cv2.imwrite(f'.\Dataset\\3\{folder_name+"_"+name}',img_out)
                            cv2.destroyAllWindows()
                            break

                        


        except Exception as ex:
            print(ex)
