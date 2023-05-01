from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
import time
import GetDictionary

start_time = time.perf_counter()

dictionary = GetDictionary.GetDictionary("slownik.txt")

service = Service(executable_path='C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get("https://instaling.pl/teacher.php?page=login")
#title = driver.title
#print(title)

Login = driver.find_element_by_xpath('//*[@id="log_email"]')

#Login.send_keys("4g1293795")#JA
#Login.send_keys("4g9630262")#Stachu
Login.send_keys("4g1524432")#Michał

Password = driver.find_element_by_xpath('//*[@id="log_password"]')

#Password.send_keys("zhubx")#JA
#Password.send_keys("cphhi")#Stachu
Password.send_keys("excpm")#Michał

Password.send_keys(Keys.RETURN)

#driver.get("https://instaling.pl/ling2/html_app/app.php?child_id=2092959")#Ja
#driver.get("https://instaling.pl/ling2/html_app/app.php?child_id=2092956")#Stachu
driver.get("https://instaling.pl/ling2/html_app/app.php?child_id=2092949")#Michał

Start_session = driver.find_element_by_xpath('//*[@id="start_session_button"]/h4').click()

time.sleep(0.1)

word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text

while word != "Gratulacje!":
    time.sleep(0.1)
    word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text
    usage_example = driver.find_element_by_xpath('//*[@id="question"]/div[1]').text

    if word not in dictionary:
        try:
            time.sleep(0.3)
            Do_not_know = driver.find_element_by_xpath('//*[@id="dont_know_new"]').click()
            time.sleep(0.3)
            Skip_question = driver.find_element_by_xpath('//*[@id="skip"]').click()
            time.sleep(0.3)
        except ElementNotInteractableException:
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
            file.write(word)
            file.write(" : ")
            file.write(Translation)
            file.write("\n")

            # Close the file
            file.close()
            dictionary = GetDictionary.GetDictionary("slownik.txt")

    else:
        if word in dictionary.keys():
                Answer = driver.find_element_by_xpath('//*[@id="answer"]')
                if usage_example == "Die ______ von Berlin ist sehr schön.":
                    Answer.send_keys('die Gegend')
                    Next_question = driver.find_element_by_xpath('//*[@id="check"]/h4').click()
                    time.sleep(0.1)
                    Next_question = driver.find_element_by_xpath('//*[@id="nextword"]').click()
                    time.sleep(0.1)
                else:
                    Answer.send_keys(dictionary[word])
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