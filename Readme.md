# Overview
This is a python script that is use to automate the selection process for the game mode Aram in the game called League of Legends. It is a script that looks up the champion that is given to you
in Arams and automatically sets up the right runes and opens up a webpage for suggestion of items
to build. This script uses many modules in computer vision such as text detection and text recognition alongside computer/broswer automation library to make this work. 



## Installation 
There is quite a few things we must install to get this working. The first thing you install is PyAutoGUI. You can use the package manager pip to install it and for more information you can head to https://pyautogui.readthedocs.io/en/latest/ for the documentation. 

```bash
pip install pyautogui
```

The next thing to install is Pillow which is an imaging library and you can also use the package manager pip to install it. For more information head over to the documentation https://pillow.readthedocs.io/en/stable/

```bash
pip install Pillow
```

Now the next installation is selenium which will be use to automate the broswer. You will have to install a webdriver of your choice in which I used firefox. You can install selenium by using pip . For more infomration  about  selenium for python go to https://selenium-python.readthedocs.io/installation.html and for webdriver you can navigate to https://sites.google.com/a/chromium.org/chromedriver/downloads. 

We're almost done with installing the required modules as the next few installation will be necessary for image processing. We will first install OpenCV for python which is library build for real time computer vision. We install OpenCV by using pip. For more information about installing OpenCv you can go to https://pypi.org/project/opencv-python/.

```bash
pip install opencv-python
```

After that we will be installing imutils which is used for basic impage processing function and makes working with OpenCV much easier. You can look for more information about this module by going to https://pypi.org/project/imutils/.

```bash
pip install imutils
```

The last module to install will be use for our image recognition. You can go to https://github.com/tesseract-ocr/tesseract to see how to install it.

One last thing you will need is to get EAST text detection deep learning model that we will be using in our code. You can get the model here https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV.


## Demo
This is just a small demonstration of what the script is suppose to do. So far I only gotten the first part of detecting and searching up the champion that is selected. It still needs to be work on for selecting the runes that is recommended on the site. 

![](/images/demo.gif)

## TO DO
* Finish the script so it can automatically select your runes based on the suggestion given
* Try to make the script run faster (slow down could be due to writing images to disk)
* Make the script run until you enter the game so when you reroll it will automatically update to the selected champion. 
* Try to automate the broswer using PyAutoGUI so there isn't a reason to install selenium
* Clean up some code


## License

[MIT](https://mit-license.org/)