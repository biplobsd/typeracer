import time
import sys
import requests
import shutil
import os
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from io import BytesIO
from PIL import Image
import win32clipboard
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

import lib.findPatterns as findPatterns
from lib.speedControl import speeds
import lib.multipleAcccount as multipleAcccount


def findopj(pattern: str, delay: int = 10, inputDriver=False):
    """
    Find object by visibile on page
    """
    global driver
    if inputDriver:
        driver = inputDriver
        
    try:
        return WebDriverWait(driver, delay).until(
            EC.visibility_of_element_located((By.XPATH, pattern))
        )
    except UnexpectedAlertPresentException:
        time.sleep(2)
        return False
    except TimeoutException:
        return False


def imageToClipboard(img_path='img.png'):
    """
    From image path this function set this to clipboard.
    """
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
        username = args.u
        password = args.p
        findUserBox = findopj(findPatterns.userBox)
        if findUserBox:
            findUserBox.send_keys(username)
            findPassBox = findopj(findPatterns.passBox)
            if findPassBox:
                findPassBox.send_keys(password)
                findSubmitbutton = findopj(findPatterns.submitButton)
                if findSubmitbutton:
                    findSubmitbutton.click()
                    time.sleep(5)


def loginCheck():
    findUsername = findopj(findPatterns.loginButton)
    if findUsername:
        return findUsername
    else:
        return False


def humanVarification():
    beginTest = findopj(findPatterns.beginTest, 2)
    while beginTest:
        driver.execute_script(
            '''window.open("https://yandex.com/images/search", "_blank");''')
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
                    findtextBox = findopj(findPatterns.textBox)
                    if findtextBox:
                        textData = findtextBox.text
                        print(textData)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        findChallInputBox = findopj(
                            findPatterns.challangeInput)
                        if findChallInputBox:
                            findChallInputBox.send_keys(textData)
                            findchallSubmit = findopj(
                                findPatterns.challangeImgSubmit)
                            if findchallSubmit:
                                findchallSubmit.click()
                                time.sleep(2)
                                beginTest = findopj(findPatterns.beginTest, 2)
                                if not beginTest:
                                    findPassedClose = findopj(
                                        findPatterns.closePopup)
                                    if findPassedClose:
                                        findPassedClose.click()
                    else:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        return


def isImFirstPosition():
    findFistPosition = findopj(findPatterns.firstPosition, 3)
    if findFistPosition:
        print(findFistPosition.text)
        return findFistPosition.text
    else:
        return False


def main(speed=0.5):
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
                for i, word in enumerate(text):
                    time.sleep(speed)
                    print(word, end=' ')
                    findInputBox.send_keys(
                        word+' ' if i != lenText-1 else word)

    humanVarification()
    # findraceAgain = findopj(findPatterns.raceAgain, 20)

    # if findraceAgain:
    #     findraceAgain.click()
    # else:
    #     break
    print('\n')


if __name__ == "__main__":
    LOGGER.setLevel(logging.CRITICAL)
    parser = argparse.ArgumentParser(
        description='Auto geting blc exp. Just for fun!')
    parser.add_argument('--justOne', type=str, help='Target just one mode')
    parser.add_argument('--speed', type=str, help='Set your speed')
    parser.add_argument('--createAccounts', type=int, help='Create multiple accounts. It is required human for recapture solving.')
    parser.add_argument(
        '-l', action=argparse.BooleanOptionalAction, help='Set as infinity loop')
    parser.add_argument('-u', type=str, help='Set your username')
    parser.add_argument('-p', type=str, help='Set your password')
    args = parser.parse_args()

    modes = ['', 'accuracy', 'dictionary', 'anime', 'lang_pt', 'lang_pt_dictionary', 'lang_es', 'jokes', 'repeat', 'games',
             'music', 'movies', 'copypasta', 'education', 'steno', 'lang_de', 'lang_id', 'lang_it', 'lang_fr', 'lang_nl', 'lang_pl']
    options = Options()
    # Hare your Edge user profile folder path. You can find in edge://version/ "Profile Path" section
    options.add_argument(
        rf'--user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1')

    driver = webdriver.Edge(options=options)
    landing = f"https://play.typeracer.com/"
    driver.get(landing)
    time.sleep(1)
    if args.createAccounts:
        print(f"Creating {args.createAccounts} accounts...")
        multipleAcccount.multipleAccount(driver, count=args.createAccounts)
        sys.exit()
    toggolClicked = False
    findtoggol = findopj(findPatterns.offcanasToggle, 2)
    if findtoggol:
        findtoggol.click()
        toggolClicked = True

    findUserleble = findopj(findPatterns.userNameLabel, 2)
    loginUser = findUserleble.text
    if loginUser != 'Guest':
        print(f"Already Login in {loginUser}")
    else:
        login()
    if toggolClicked:
        findCloseToggo = findopj(findPatterns.offcanasToggleClose, 2)
        if findCloseToggo:
            findCloseToggo.click()
    if args.justOne:
        while True:
            driver.get(args.justOne)
            time.sleep(1)
            main(args.speed if args.speed else 0.5)
            if not args.l:
                break
    else:
        while True:
            for i, mode in enumerate(modes):
                print(f'{i+1}/{len(modes)}', mode)
                for speed in speeds:
                    landing = f"https://play.typeracer.com/?universe={mode}"
                    driver.get(landing)
                    time.sleep(1)
                    fistPosition = isImFirstPosition()
                    if fistPosition and (loginUser.split('(')[0].strip()[:5] != isImFirstPosition().split('(')[0].strip()[:5]):
                        print(
                            f"I'm not first position. trying by speed {speed}")
                        main(speed)
                    elif not fistPosition:
                        main(0.5)
                    else:
                        break
            if not args.l:
                break
