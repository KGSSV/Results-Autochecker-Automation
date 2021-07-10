
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium import options
from selenium.webdriver.common.by import By
import requests
from datetime import datetime
import time
import smtplib
import sys
#============================================$#
# to get the options
choose = webdriver.ChromeOptions()
choose.headless = True
web = webdriver.Chrome(options=choose)

# =============================================
# get the api call


# Time to wait input
time_to_wait = int(
    input('Time to wait After each successful Cycle (Enter in Mins): '))
time_to_wait = time_to_wait * 60   # convertion to


def getText():
    # -----------------------------prereq---------------
    url = 'https://api.ocr.space/parse/image'
    api_key = 'a07656b96688957'

    lang = 'eng'
    # to open the file ans store it in the variable
    filepointer = open(r'C:\Users\akura\OneDrive\Desktop\captha.png', 'rb')

    # get the payload
    payload = {'apikey': api_key, 'language': lang}
    response = requests.request('POST', url, data=payload, files={
                                'filename': filepointer})
    FileH = open(r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')

    # ================================================
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    # ================================================

    FileH.write(
        '\nResponse Code received : {} ----> At time : {}'.format(response, current_time))
    FileH.close()
    response = response.json()

    # data extraction
    try:
        data_received = str(response['ParsedResults'][0]['ParsedText'])
        # data cleaning
        sub = ['\r', '\n', '\r\n', '\n\r']
        for s in sub:
            data_received = data_received.replace(s, " ")

        cleaned_data = data_received
        print(cleaned_data)
        return cleaned_data

    except Exception as e:
        FileH = open(r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
        FileH.write(
            '\n \t Cannot Get Captha Response possible error(Server Offline) Trying again in 10 min')
        FileH.write('\n Reason : {}'.format(e))
        FileH.write(
            '\n==================================================================================\n\n')
        FileH.close()
        return ''


i = 1
no_of_api_calls = 0
no_of_cycles = 1
result = '.'
#wait_time = 20
web.get('https://evarsity.srmist.edu.in/srmwebonline/exam/onlineResult.jsp')
while True:
    result = '.'
    while True:
        if(result == '.'):

            # loging trials
            FileH = open(
                r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            FileH.write(
                '\n Try  {}... Trying at : {}'.format(i, current_time))
            FileH.close()
            web.refresh()
            time.sleep(5)
            regno = 'xxxxxxxxxxxxxxxx'

            last = web.find_element_by_xpath('//*[@id="txtRegisterno"]')
            last.send_keys(regno)
            web.find_element(By.ID, 'txtFromDate').send_keys('xx')
            web.find_element(By.ID, 'selFromMonth').send_keys('xxxxxx')
            web.find_element(By.ID, 'txtFromYear').send_keys('xxxxxx')

            # taken screen shop and is placed in desktop directory
            tookss = web.find_element_by_xpath(
                '//*[@id="searchfilter"]/table/tbody/tr/td/table/tbody/tr[4]/td[4]/img').screenshot(r'C:\Users\akura\OneDrive\Desktop\captha.png')
            unique_code = getText()
            no_of_api_calls = no_of_api_calls + 1
            length_of_captcha = len(unique_code)
            if(length_of_captcha == 0):
                print('waiting 10 min')

                time.sleep(600)
                break
            else:
                pass

            web.find_element(By.ID, 'txtvericode').send_keys(unique_code)

            web.find_element(By.ID, 'imgsubmit').click()

            # try:
            #     result = web.find_element_by_xpath('//*[text()="PASS"]')
            #     result = 'PASS'
            # except:
            #     result = web.find_element_by_xpath(
            #         '//*[@id="divResult"]/table/tbody/tr/td/font/b').text

            #page_source = web.page_source
            try:
                result = web.find_element_by_xpath(
                    '//*[@id="table1"]/tbody/tr[1]/td[5]/b').text
            except:
                result = web.find_element_by_xpath(
                    '//*[@id="divResult"]/table/tbody/tr/td/font/b').text

            if(result == 'Invalid Verification Code.'):
                FileH = open(
                    r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                FileH.write(
                    '\n Captha Sent successfully but not correct Retrying in 10 sec ')
                FileH.close()
                # web.refresh()
                print('Trying Again in 10 sec due to incorrect captcha')
                time.sleep(10)
                i = i + 1
                break

            else:
                FileH = open(
                    r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                FileH.write('\n Try {} ....  Success'.format(i))
                FileH.close()
                FileH = open(
                    r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                FileH.write(
                    ' \n \t\t No of calls used this run : {}  with Avg calls per cycle :{}:'.format(no_of_api_calls, no_of_api_calls/no_of_cycles))
                i = 0
                if result != 'Invalid Verification Code.':
                    if 'not available.' in result:
                        no_of_cycles = no_of_cycles + 1
                        FileH = open(
                            r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                        FileH.write(
                            '\n Result Not published --> next try after {} seconds'.format(time_to_wait))
                        FileH.close()
                        FileH = open(
                            r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                        FileH.write(
                            '\n==================================================================================\n\n')
                        FileH.close()

                        print(
                            'result is not published ------> checked at :  {}'.format(current_time))
                        time.sleep(time_to_wait)
                        break

                    else:

                        def S(X): return web.execute_script(
                            'return document.body.parentNode.scroll' + X)
                        web.set_window_size(S('Width'), S('Height'))
                        web.find_element_by_tag_name(
                            'body').screenshot(r'C:\Users\akura\OneDrive\Desktop\SEMISTERMARKS.png')

                        FileH = open(
                            r'C:\Users\akura\OneDrive\Desktop\logsautocheck.txt', 'a')
                        FileH.write('\n $$$$$$$$$ MARKS RELEASED $$$$$$$$$$')
                        FileH.close()

                        # mail sending

                        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.ehlo()
                            smtp.login('xxxxxxxxxxxxx',
                                       'xxxxxxxxxxxxxxxx')

                            # =======================================
                            subject = 'Marks are released'
                            body = 'please check the desktop for full screen shot'

                            msg = f'Subject : {subject} \n\n {body}'
                            smtp.sendmail('xxxxxxxxxxxxxx',
                                          'xxxxxxxxxxxxxxxx', msg)

                            web.close()
                            sys.exit()
                            ## Completed ##
