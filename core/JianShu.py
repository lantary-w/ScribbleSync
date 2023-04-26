# -*- coding: utf-8 -*-
# @Author  : lantary
# @Email   : lantary-w@qq.com
# @Blog    : https://lantary.cn

import os
import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def cheack_element(ce_driver, ce_element):
    while True:
        try:
            element = ce_driver.find_element(by=By.CLASS_NAME, value=ce_element)
            time.sleep(1)
        except:
            return True


class JianShu:
    def __init__(self, file, config):
        self.account = config['jianshu']['login']['useraccount']
        self.password = config['jianshu']['login']['userpassword']
        self.cookie = config['jianshu']['cookie_path']
        self.config = config
        self.md_file = file

    def login(self):
        driver = webdriver.Chrome()
        url = 'https://www.jianshu.com/sign_in'
        driver.get(url)
        time.sleep(0.5)

        if self.config['jianshu']['login']['login_mode'] == 'auto':
            print('正在登录简书, 登录模式为自动登录, 但需要手动输入验证码')
            # 输入账号密码
            driver.find_element(by=By.ID, value="session_email_or_mobile_number").send_keys(self.account)
            driver.find_element(by=By.ID, value="session_password").send_keys(self.password)
            time.sleep(0.5)

            # 点击登录按钮，等待用户输入验证码
            driver.find_element(by=By.ID, value="sign-in-form-submit-btn").click()
            time.sleep(self.config['jianshu']['vf_wait_time'])

            # 保存cookies
            cookies = driver.get_cookies()
            cookie = ";".join([item["name"] + "=" + item["value"] + "" for item in cookies])
            with open(self.cookie, 'w') as cookie_f:
                cookie_f.write(str(cookie))
            driver.quit()

        elif self.config['jianshu']['login']['login_mode'] == 'manual':
            print('正在登录简书, 登录模式为手动登录, 请手动输入账号密码')
            # 等待用户输入账号密码

            if cheack_element(driver, 'sign-in-button'):
                # 保存cookies
                cookies = driver.get_cookies()
                cookie = ";".join([item["name"] + "=" + item["value"] + "" for item in cookies])
                with open(self.cookie, 'w') as cookie_f:
                    cookie_f.write(str(cookie))
                driver.quit()

    def write_blog(self):

        if os.path.exists(self.cookie):

            cookie_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.cookie))
            d_time = datetime.datetime.now() - cookie_time

            # 判断cookie是否过时
            if d_time < datetime.timedelta(hours=self.config['jianshu']['cookie_valid_time']):
                print('====正在上传到简书====')

                wb_cookie = open(self.cookie, 'r').read()
                wb_md_context = open(self.md_file, 'r', encoding='utf-8').read()
                chrome_options = Options()
                chrome_options.page_load_strategy = 'eager'
                driver = webdriver.Chrome(options=chrome_options)

                driver.get('https://www.jianshu.com/')
                time.sleep(0.5)
                # cookie转为字典格式，方便driver读取
                wb_cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in wb_cookie.split(";")}
                for key, value in wb_cookie_dict.items():
                    driver.add_cookie({'name': key, 'value': value})

                driver.get(url='https://www.jianshu.com/writer#/')
                time.sleep(0.5)
                driver.find_element(by=By.CLASS_NAME, value="_1GsW5").click()
                time.sleep(1)
                for line in wb_md_context.splitlines():
                    # 对line进行正则匹配，检查是否含有图片
                    pirtures = re.findall(r'!\[(.*?)]\(((.*?)\.(png|bmp|jpg|gif|tif|jpeg))\)', line)
                    if not pirtures:
                        driver.find_element(by=By.ID, value="arthur-editor").send_keys(Keys.PAGE_DOWN, line)
                        driver.find_element(by=By.ID, value="arthur-editor").send_keys(Keys.PAGE_DOWN, '\n')
                    else:
                        # 以图片格式为间隔构造list
                        line_list = re.split(r'!\[.*?]\(.*?\.(?:png|bmp|jpg|gif|tif|jpeg)\)', line)
                        for line_index, line_part in enumerate(line_list):
                            if line_index == len(line_list) - 1:
                                driver.find_element(by=By.ID, value="arthur-editor").send_keys(Keys.PAGE_DOWN, line_part)
                                driver.find_element(by=By.ID, value="arthur-editor").send_keys(Keys.PAGE_DOWN, '\n')
                            else:
                                pirture = os.path.join(os.path.dirname(self.md_file), pirtures[line_index][1])
                                pirture_name = pirtures[line_index][0]

                                # 写入到简书
                                driver.find_element(by=By.CLASS_NAME, value='_2zLpt').click()
                                driver.find_element(by=By.ID, value="arthur-editor").send_keys(Keys.PAGE_DOWN, line_part)
                                driver.find_element(by=By.ID, value='kalamu-upload-image').send_keys(pirture)
                                time.sleep(self.config['jianshu']['upload_wait_time'])
                                driver.find_element(by=By.ID, value='arthur-editor').send_keys(pirture_name)
                                print('图片: ' + pirture_name + ' 已上传')
            else:
                self.login()
                time.sleep(1)
                self.write_blog()

        else:
            self.login()
            time.sleep(1)
            self.write_blog()
