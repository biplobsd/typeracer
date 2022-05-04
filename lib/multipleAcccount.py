import time
import string
import random

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

from lib.findopj import Findopj
import lib.findPatterns as findPatterns

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def readAccounts():
    with open('../accountNames.txt') as r:
        return r.read()


def multipleAccount(driver, count=20, random=True):
    # accounts = readAccounts()
    m = Findopj(driver)
    
    findtoggol = m.findopj(findPatterns.offcanasToggle, 2)
    if findtoggol:
        findtoggol.click()
        for _ in range(count):
            firstName = id_generator()
            lastName = 'test'
            print(f'Creating account {_+1} Name: {firstName} {lastName}')
            findSignIn = m.findopj(findPatterns.loginButton)
            if findSignIn:
                findSignIn.click()
                findCreateAccount = m.findopj(findPatterns.clearAaccount)
                if findCreateAccount:
                    findCreateAccount.click()
                    findFirstNamBox = m.findopj(findPatterns.firstNamebox)
                    if findFirstNamBox:
                        findFirstNamBox.send_keys(firstName)
                    
                    findlastNamBox = m.findopj(findPatterns.lastNamebox)
                    if findlastNamBox:
                        findlastNamBox.send_keys(lastName)

                    findEmailBox = m.findopj(findPatterns.createEmail)
                    if findEmailBox:
                        findEmailBox.send_keys(f"{firstName}{lastName}@gmail.com")
                    
                    select = Select(m.findopj(findPatterns.dateOfBirthMonth))
                    select.select_by_value('1')

                    findYearBox = m.findopj(findPatterns.dateOfBirthYear)
                    if findYearBox:
                        findYearBox.send_keys('1999')
                    
                    findUsername = m.findopj(findPatterns.createUsernamebox)
                    if findUsername:
                        findUsername.send_keys(f'{firstName}{lastName}')
                    
                    findPasswordBox = m.findopj(findPatterns.createPasswordbox)
                    if findPasswordBox:
                        findPasswordBox.send_keys(f'{firstName}{lastName}')
                    
                    findRePasswordBox = m.findopj(findPatterns.createRePasswordbox)
                    if findRePasswordBox:
                        findRePasswordBox.send_keys(f'{firstName}{lastName}')

                    findSignUp = m.findopj(findPatterns.signUpButton)
                    if findSignUp:
                        findSignUp.click()
                    
                    for t in range(30):
                        time.sleep(1)
                        print(f"Please complete recapture {t}")
                        if not m.findopj(findPatterns.recapture):
                            print("Completed..")
                            findOK = m.findopj(findPatterns.OK)
                            if findOK:
                                findOK.click()
                            break
                    # time.sleep(2)
                    findtoggol = m.findopj(findPatterns.offcanasToggle)
                    if findtoggol:
                        try:
                            findtoggol.click()
                        except ElementClickInterceptedException:
                            print("Toggole is not clickable.")

                    findUserleble = m.findopj(findPatterns.userNameLabel)
                    loginUser = findUserleble.text
                    if loginUser != 'Guest':
                        print(f"Account create successful {loginUser}")
                        with open("accountsCreated.txt", 'a') as w:
                            w.write(
                                f'{firstName}{lastName} {firstName}{lastName}\n')
                        findSignOut = m.findopj(findPatterns.signOut)
                        if findSignOut:
                            findSignOut.click()
                    else:
                        print("Account not created.")
    
    findCloseToggo = m.findopj(findPatterns.offcanasToggleClose)
    if findCloseToggo:
        findCloseToggo.click()
