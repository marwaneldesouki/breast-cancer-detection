# Project Title
- breast-cancer-detection using image processing and deeplearning 

## Description
- breast cancer detection using image processing and neural deeplearning.<br />
i used image processing to put some process on the image like enhancment and segmantation to make the mass more visible.<br />
and used neural deep learning to build a classifier model to detect the mass and telling us if there is cancer or not.<br />


## DataSet used
-[Dataset Link](https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset)<br />
<img src="https://www.researchgate.net/publication/338558131/figure/fig3/AS:962412517793792@1606468433025/CBIS-DDSM-example-images-used-for-detection.jpg" data-canonical-src="https://www.researchgate.net/publication/338558131/figure/fig3/AS:962412517793792@1606468433025/CBIS-DDSM-example-images-used-for-detection.jpg" width="720" height="400" />
- used mamogram images to make the image processing on it.


## Libraries used
•	Tkinter.<br />
• customtkinter.<br />
• PIL.<br />
• threading.<br />
• random.<br />
• thread.<br />
• keras.<br />
• cv2.<br />
• numpy.<br />
• matplotlib.<br />

## Requirements
  •	Python 3.10.6.<br />
• Install all libraries.<br />


## Project’s main functions:
 main.py:<br />
    •erode: to erode image by one iteration.<br />
    •dilate: to dilate image by one iteration.<br />
    •erode: to erode image by one iteration.<br />
    •main: to get all images in sub folders,then read the image and start image processing on it.<br />
    -GaussianBlur with filter (3x3).<br />
    -Canny with min,max threshold (0,255).<br />
    -threshold with min,max 180,255 and THRESHBINARY.<br />
    -getStructuringElement with MORPH(3X3).<br />
    -dilate 8-iteration.<br />
    -erode 7-iteration.<br />
    -dilate 2-iteration.<br />
    
    then you will enter to edit mode for each image in dataset,and this to edit every image to build your seperation dataset.<br />
    so the edit_mode working with your keypad numbers (0,1,2,3).<br />
    0-to save image in non-cancerd folder.<br />
    1-to save image in cancerd folder.<br />
    2-to enter another edit_mode -> i will explain it now.<br />
    3-skip the current image and don`t save it.<br />
  
    so to enter another edit_mode and after press 2 in keypad
    you will enter another edit_mode.<br />
    and that to make more edits on the image like dilate and erode
    so you can use your keypad numbers to make edit (0,1,3,+,-).<br />
    0 - for save image in non-cancerd folder.<br />
    1 - for save image in cancerd folder.<br />
    3 - for skip image and don`t save it.<br />
    + - for increment the erode.<br />
    - - for increment the dilate.<br />
  
  ##
 BreastCancer_Classifier.py:<br />
    •classifiy: it takes the image to return the perdiction result if it cancerd or not.
    
  
## GUI
    
    •Classifier_Page.<br />
    <img src="https://user-images.githubusercontent.com/37198610/209975749-424d9794-21a6-4a73-b34e-1317eeb19ea8.PNG" data-canonical-src="https://user-images.githubusercontent.com/37198610/209975749-424d9794-21a6-4a73-b34e-1317eeb19ea8.PNG" width="720" height="400" />
    
    •Classifier_Page if the classifier found cancer.<br />
    <img src="https://user-images.githubusercontent.com/37198610/209975759-4d260691-e453-4443-8278-ed0e3bdcdca1.PNG" data-canonical-src="https://user-images.githubusercontent.com/37198610/209975759-4d260691-e453-4443-8278-ed0e3bdcdca1.PNG" width="720" height="400" />

    •Classifier_Page if the classifier did`t found cancer.<br />
    <img src="https://user-images.githubusercontent.com/37198610/209975761-66e7518b-1373-4e74-9c8d-b321013794ff.PNG" data-canonical-src="https://user-images.githubusercontent.com/37198610/209975761-66e7518b-1373-4e74-9c8d-b321013794ff.PNG" width="720" height="400" />

    •ImageProcessing_Page
    <img src="https://user-images.githubusercontent.com/37198610/209975762-28ee0a01-350c-4a84-87c7-014441352a56.PNG" data-canonical-src="https://user-images.githubusercontent.com/37198610/209975762-28ee0a01-350c-4a84-87c7-014441352a56.PNG" width="720" height="400" />


## Developer
marwan eldesouki
