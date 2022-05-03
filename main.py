import time, sys, requests, shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from io import BytesIO
from PIL import Image
import win32clipboard
import findPatterns

def findopj(pattern: str, delay: int = 10):
    try:
        return WebDriverWait(driver, delay).until(
            EC.visibility_of_element_located((By.XPATH, pattern))
        )
    except TimeoutException:
        return False

def imageToClipboard(img_path='img.png'):
    image = Image.open(img_path)
    output = BytesIO()
    image.convert('RGB').save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def imgUrlToFile(src):
    response = requests.get(src, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def imgUrlToClipboard(src):
    imgUrlToFile(src)
    imageToClipboard()


def login():
    findLoginB = findopj(findPatterns.loginButton, 5)
    if findLoginB:
        print("Trying to login ...")
        findLoginB.click()
        username = sys.argv[1]
        password = sys.argv[2]
        findUserBox = findopj(findPatterns.userBox)
        if findUserBox:
            findUserBox.send_keys(username)
            findPassBox = findopj(findPatterns.passBox)
            if findPassBox:
                findPassBox.send_keys(password)
                findSubmitbutton = findopj(findPatterns.submitButton)
                if findSubmitbutton:
                    findSubmitbutton.click()

def loginCheck():
    findUsername = findopj(findPatterns.loginButton)
    if findUsername:
        return findUsername
    else:
        return False


def humanVarification():
    beginTest = findopj(findPatterns.beginTest, 2)
    if beginTest:
        driver.execute_script('''window.open("https://yandex.com/images/search", "_blank");''')
        time.sleep(0.5)
        
        beginTest.click()
        findchallangeImg = findopj(findPatterns.challangeImg)
        if findchallangeImg:
            challImgsrc = findchallangeImg.get_attribute("src")
            imgUrlToClipboard(challImgsrc)

            driver.switch_to.window(driver.window_handles[-1])
            findImageSeachButton = findopj(findPatterns.imageSearchButton)
            if findImageSeachButton:
                findImageSeachButton.click()
                findclipboardPaste = findopj(findPatterns.clipboardPaste)
                if findclipboardPaste:
                    findclipboardPaste.click()
                    findtextBox= findopj(findPatterns.textBox)
                    if findtextBox:
                        textData = findtextBox.text
                        print(textData)
                        driver.switch_to.window(driver.window_handles[0])
                        findChallInputBox = findopj(findPatterns.challangeInput)
                        if findChallInputBox:
                            findChallInputBox.send_keys(textData)
                            findchallSubmit = findopj(findPatterns.challangeImgSubmit)
                            if findchallSubmit:
                                findchallSubmit.click()
                                time.sleep(2)
                                findPassedClose = findopj(findPatterns.closePopup)
                                if findPassedClose:
                                    findPassedClose.click()

def main(mode):
    landing = f"https://play.typeracer.com/?universe={mode}"
    driver.get(landing)
    time.sleep(1)
    startbutton = findopj(findPatterns.startRace)
    if startbutton:
        startbutton.click()
    
    findclosePopup = findopj(findPatterns.closePopup, 10)
    if findclosePopup:
        findclosePopup.click()

    findGo = findopj(findPatterns.gameStatus, 30)
    if findGo:
        findgetText = findopj(findPatterns.getTest)
        if findgetText:
            findInputBox = findopj(findPatterns.inputBox)
            if findInputBox:
                text = findgetText.text.split()
                lenText = len(text)
                for i,word in enumerate(text):
                    time.sleep(0.4)
                    print(word, end=' ')
                    findInputBox.send_keys(word+' ' if i!=lenText-1 else word)
    
    humanVarification()
    # findraceAgain = findopj(findPatterns.raceAgain, 20)

    # if findraceAgain:
    #     findraceAgain.click()
    # else:
    #     break
    print()

if __name__ == "__main__":


    modes = ['accuracy','dictionary', 'anime', 'lang_pt', 'lang_pt_dictionary', 'lang_es', 'jokes', 'repeat', 'games', 'music', 'movies', 'copypasta', 'education', 'steno', 'lang_de', 'lang_id', 'lang_it', 'lang_fr', 'lang_nl', 'lang_pl']
    options = Options()
    # Hare your Edge user profile folder path. You can find in edge://version/ "Profile Path" section
    options.add_argument(
        r'--user-data-dir=C:\\Users\\alpha4d\\AppData\\Local\\Microsoft\\Edge\\User Data')

    driver = webdriver.Edge(options = options)
    landing = f"https://play.typeracer.com/"
    driver.get(landing)
    time.sleep(1)
    toggolClicked = False
    findtoggol = findopj(findPatterns.offcanasToggle, 2)
    if findtoggol:
        findtoggol.click()
        toggolClicked = True

    findUserleble = findopj(findPatterns.userNameLabel, 2)
    if findUserleble.text != 'Guest':
        print(f"Already Login in {findUserleble.text}")
    else:
        login()
    if toggolClicked:
        findCloseToggo = findopj(findPatterns.offcanasToggleClose, 2)
        if findCloseToggo:
            findCloseToggo.click()
    for mode in modes:
        main(mode)
