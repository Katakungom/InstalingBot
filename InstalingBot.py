from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import GetDictionary

start_time = time.perf_counter()
dictionary = GetDictionary.GetDictionary("slownik.txt")

service = Service(executable_path='C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get("https://instaling.pl/teacher.php?page=login")

Login = driver.find_element_by_xpath('//*[@id="log_email"]')

#Login.send_keys("5g1310675")#JA
#Login.send_keys("5g1011844")#Stachu
#Login.send_keys("5g1595316")#Michał
Login.send_keys('2i1110462')#Aleks

Password = driver.find_element_by_xpath('//*[@id="log_password"]')

#Password.send_keys("idtks")#JA
#Password.send_keys("gcajb")#Stachu
#Password.send_keys("ghzex")#Michał
Password.send_keys('gezgy')#Aleks

Password.send_keys(Keys.RETURN)

#driver.get("https://instaling.pl/student/pages/mainPage.php?student_id=2193030")#Ja
#driver.get("https://instaling.pl/student/pages/mainPage.php?student_id=2193027")#Stachu
#driver.get("https://instaling.pl/student/pages/mainPage.php?student_id=2193018")#Michał
driver.get('https://instaling.pl/student/pages/mainPage.php?student_id=1985351')#Aleks


Start_session = driver.find_element_by_xpath('//*[@id="student_panel"]/p[1]/a').click()
warunki = driver.find_element_by_xpath('//*[@id="start_session_button"]').click()


time.sleep(0.1)

word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text

while word != "Gratulacje!":

    word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text
    usage_example = driver.find_element_by_xpath('//*[@id="question"]/div[1]').text

    if usage_example not in dictionary:
        try:
            #pomiń dodatkowe słówko
            time.sleep(0.3)
            Do_not_know = driver.find_element_by_xpath('//*[@id="dont_know_new"]').click()
            time.sleep(0.3)
            Skip_question = driver.find_element_by_xpath('//*[@id="skip"]').click()
            time.sleep(0.3)
        except ElementNotInteractableException:
            #Dodaj nowe słowo do słownika
            
            Answer = driver.find_element_by_xpath('//*[@id="answer"]')
            
            Answer.send_keys("a")
            Next_question = driver.find_element_by_xpath('//*[@id="check"]/h4').click()
            time.sleep(0.1)
            Translation = driver.find_element_by_xpath('//*[@id="word"]').text
            time.sleep(0.1)
            Next_question = driver.find_element_by_xpath('//*[@id="nextword"]').click()
            time.sleep(0.1)
            file = open("slownik.txt", "a", encoding='utf-8')
            # Write some data to the file   
            file.write(usage_example)
            file.write("|")
            file.write(word)
            file.write("|")
            file.write(Translation)
            file.write("\n")

            # Close the file
            file.close()
            dictionary = GetDictionary.GetDictionary("slownik.txt")

    else:
        if usage_example in dictionary.keys():
                Answer = driver.find_element_by_xpath('//*[@id="answer"]')

                Answer.send_keys(dictionary[usage_example])
                Next_question = driver.find_element_by_xpath('//*[@id="check"]/h4').click()
                time.sleep(0.1)
                Next_question = driver.find_element_by_xpath('//*[@id="nextword"]').click()
                time.sleep(0.1)
            
    test_word=driver.find_element_by_xpath('//*[@id="summary"]/table/caption').text
    if test_word == "Gratulacje!":
        word = test_word
    else:
        word = word

time.sleep(0.1)
Back_to_homepage = driver.find_element_by_xpath('//*[@id="return_mainpage"]').click()
time.sleep(0.1)

driver.quit()

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
