from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import os, requests, json, logging

school_num = os.getenv('SCHOOL_NUM')
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'authority': 'www.jiandaoyun.com',
    'sec-ch-ua': '\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"',
    'content-type': 'application/json;charset=UTF-8',
    'referer': 'https://www.jiandaoyun.com/dashboard'
}

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=chrome_service, options=options)

driver.get('https://www.jiandaoyun.com/app/5f36523524018e0006723761/entry/5f1039fca2c60000075671b0')
sleep(1)
nameinput = driver.find_element(By.XPATH, '//*[@id="username"]')
passinput = driver.find_element(By.XPATH, '//*[@id="password"]')
nameinput.send_keys(school_num)
passinput.send_keys(os.getenv('PASSWORD'))
driver.find_element(By.XPATH, '//*[@id="login_submit"]').click()

driver.refresh()
cookies = [f"{c['name']}={c['value']};" for c in driver.get_cookies()]
headers['cookie'] = ''.join(cookies)
for r in driver.requests:
    if r.method == 'GET': continue
    if 'x-csrf-token' in r.headers:
        headers['x-csrf-token'] = r.headers['x-csrf-token']
        headers['x-request-id'] = r.headers['x-request-id']
        break
driver.close()

data = json.loads(os.getenv('FORM_DATA'))
today = datetime.now().isoformat().split('T')[0]
timestamp = f'{int(datetime.fromisoformat(today).timestamp())}000'

base = data['values']['_widget_1581259263913']['data'].split('-')[-3:]
data['values']['_widget_1581259263913']['data'] = f'{today}-{"-".join(base)}'
data['values']['_widget_1597486309838']['data'][0]['_widget_1646815571409']['data'] = f'{today}-{school_num}'
data['values']['_widget_1581259263910']['data'] = timestamp
data['values']['_widget_1597486309838']['data'][0]['_widget_1646814426533']['data'] = timestamp

ret = requests.post('https://www.jiandaoyun.com/_/data/create', headers=headers, data=json.dumps(data))
if '????????????????????????????????????' not in ret.text:
    logging.error(json.loads(ret.text)['msg'])