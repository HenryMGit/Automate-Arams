import pyautogui,time
import urllib.request
from PIL import ImageGrab, Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from champ_detection import DetectChamp


def takeScreenshot():
    #waits  5 seconds so you can navigate to the LoL client 
    time.sleep(5)

    #Screenshot the Lol Cleints and grabs the image
    pyautogui.hotkey('alt','prtscr')
    championImg = ImageGrab.grabclipboard()

    #saves the image as championSelected.png
    if isinstance(championImg, Image.Image):
        championImg.save('championSelected.png')
        return True
    
    return False


def lookUp(championName):
    #Opens Firefox and waits 2 seconds
    driver = webdriver.Firefox()
    driver.get('https://www.murderbridge.com/')
    time.sleep(2)
   
    #looks for the input element and types in the name of the champion
    searchBar = driver.find_element_by_class_name('react-autosuggest__input')
    searchBar.send_keys(championName)
    searchBar.send_keys(Keys.RETURN)

    #will use the driver later 
    return driver

def main():
    if takeScreenshot():  
        champion = DetectChamp("championSelected.png")
        champion.preprocess_image()
        champion.text_detection()
        text = champion.text_recognition()
        print(text)
        driver = lookUp(text)
       
if __name__ == "__main__":
    main()