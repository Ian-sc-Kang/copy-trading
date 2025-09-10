from discord.ext import commands

from datetime import datetime
import pytz
import re

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os, sys

import asyncio

import TD_Client

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

class Kindred:
    def __init__(self, string):
        self.string = string
        self.instruction_op = r"\bBTO\b|\bSTC\b|\bBTC\b|\bSTO\b"
        self.symbol_op = r"\b[A-Z]+\b"
        self.instruction_list = ["BTO", "STC"]
    
    def regx_search(self, operator):
        m = re.search(operator, self.string)
        return m
    
    def regx_findall(self, operator):
        m = re.findall(operator, self.string)
        return m                  
            
    def is_callout(self):
        split_list = self.string.split()
        i = 1
        try:
            instruction = split_list[i]
        except Exception as e:
            instruction = False
        try:
            ticker = split_list[i+1]
        except Exception as e:
            ticker = False
        try:
            strike_price = re.search("[0-9]+", split_list[i+2]).group()
        except Exception as e:
            strike_price = False
        try:
            putcall = re.search("P|C|p|c", split_list[i+2]).group()
        except Exception as e:
            putcall = False
        try:
            exp_month = split_list[i+3].split("/")[0]
        except Exception as e:
            exp_month = False
        try:
            exp_day = split_list[i+3].split("/")[1]
        except Exception as e:
            exp_day = False
        try:
            order_price = float(re.search("[0-9]*[.][0-9]*", split_list[i+4]).group())
        except AttributeError:
            try:
                order_price = float(re.search("[0-9]+[.]*[0-9]*", split_list[i+4]).group())
            except Exception as e:
                order_price = False
        except:
            order_price = False
        
        if instruction in self.instruction_list and ticker and strike_price and putcall and exp_month and exp_day and order_price:
            return True
        else:
            return False
            
    def split_option_scanner(self):
        split_list = self.string.split()
        i = 1
        instruction = split_list[i]
        if instruction == "BTO":
            instruction = "BUY_TO_OPEN"
        elif instruction == "STC":
            instruction = "SELL_TO_CLOSE"
        

        ticker = split_list[i+1]
        strike_price = re.search("[0-9]+[.]*[0-9]", split_list[i+2]).group()
        put_call = re.search("P|C", split_list[i+2]).group()
        exp_month = split_list[i+3].split("/")[0]
        if len(exp_month) == 1:
            exp_month = f"0{exp_month}"
        exp_day = split_list[i+3].split("/")[1]
        if len(exp_day) == 1:
            exp_day = f"0{exp_day}"
        try:
            exp_year = split_list[i+3].split("/")[2]
        except IndexError:
            exp_year = str(local_to_nytime().year)[-2:] # if 2021, it's last 2 digits 21
        # try:
        #     order_price = float(re.search("[0-9]*[.][0-9]*", split_list[i+4]).group())
        # except AttributeError:
        #     order_price = float(re.search("[0-9]+[.]*[0-9]*", split_list[i+4]).group())
        # try:
        #     stop_index = split_list.index("SL")
        #     stop_price_index = stop_index + 1
        #     try:
        #         stop_price = float(re.search("[0-9]*[.][0-9]*", split_list[stop_price_index]).group())
        #     except AttributeError:
        #         stop_price = float(re.search("[0-9]+[.]*[0-9]*", split_list[stop_price_index]).group())
        #     except IndexError:
        #         stop_price = False
        # except ValueError:
        #     stop_price = False
            
        symbol = f"{ticker}_{exp_month}{exp_day}{exp_year}{put_call}{strike_price}"
        
        if instruction == "BUY_TO_OPEN":
            operator = "[(].*[)]"
            try:                
                m = self.regx_search(operator)
                position = m.group().lower()
                if "half" in position or "50%" in position:
                    position_rate = 0.01 # 5% of netliquidation value
                elif "small" in position:
                    position_rate = 0.01 # 2.5% of netliquidation value
                elif "risky" in position or "slow" in position or "lotto" in position:
                    position_rate = 0.01 # 1% of netliquidation value
                else:
                    position_rate = 0.01 # 10% of netliquidation value
            except AttributeError:
                position_rate = 0.01 # 5% of netliquidation value
        elif instruction == "SELL_TO_CLOSE":
            position_rate = 1
            

        return (instruction, symbol, position_rate)

       


def local_to_nytime():
    eastern = pytz.timezone('US/Eastern')
    ny_dt = datetime.now().astimezone(eastern)
    return ny_dt
    #fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    #loc_dt.strftime(fmt)

def confirm_msg(order_res_status_code, msg):
    kindred = Kindred(msg)
    if kindred.is_callout():
        i = 0
        instruction = kindred.split_option_scanner()[i]
        symbol = kindred.split_option_scanner()[i+1]
        # order_price = kindred.split_option_scanner()[i+2]
        # stop_price = kindred.split_option_scanner()[i+3]
        position_rate = kindred.split_option_scanner()[i+2]
        msg_d = f"{instruction}: {symbol} ({position_rate*100}%)"
    if order_res_status_code == 201:
        return f"{msg_d}\nThe order is sucessfully placed."
    elif order_res_status_code == 400:
        return f"{msg_d}\nAn error message indicating the validation problem with the request."
    elif order_res_status_code == 401:
        return f"{msg_d}\nAn error message indicating the caller must pass a valid AuthToken in the HTTP authorization request header."
    elif order_res_status_code == 500:
        return f"{msg_d}\nAn error message indicating there was an unexpected server error."        
    elif order_res_status_code == 403:
        return f"{msg_d}\nAn error message indicating the caller is forbidden from accessing this page."
    elif order_res_status_code == 999:
        return f"{msg_d}\nThis is not in your positions"
    elif order_res_status_code == 998:
        return f"{msg_d}\nBuy/Sell Instruction is not valid in the callout message."


    

def copy_option(msg, user):
    kindred = Kindred(msg)
    if kindred.is_callout():
        i = 0
        instruction = kindred.split_option_scanner()[i]
        symbol = kindred.split_option_scanner()[i+1]
        # order_price = kindred.split_option_scanner()[i+2]
        # stop_price = kindred.split_option_scanner()[i+3]
        position_rate = kindred.split_option_scanner()[i+2]
        
        if instruction == "BUY_TO_OPEN":
            order_type = "LIMIT"
            new_access_token = user.get_refreshed_access_token()
            account_res = user.get_account(new_access_token)
            netliq = user.get_netliq(account_res)

            quote_res = user.get_quote(symbol, new_access_token)
            j = quote_res.json()
            mark = j.get(symbol).get("mark")
            price_s = "{:.2f}".format(mark)
            order_price = float(price_s)

            quantity = netliq * position_rate // (order_price * 100)
            
            order_res = user.place_option_order(new_access_token, order_type, order_price, instruction, symbol, quantity)
            return order_res.status_code

            
        elif instruction == "SELL_TO_CLOSE":
            order_type = "MARKET"
            try:
                new_access_token = user.get_refreshed_access_token()
                account_res = user.get_account(new_access_token)
                quantity = user.get_qty_all_out(symbol, account_res)

                # quote_res = user.get_quote(symbol, new_access_token)
                # j = quote_res.json()
                # mark = j.get(symbol).get("mark")
                # price_s = "{:.2f}".format(mark)
                # order_price = float(price_s)
                order_price = ""
                

                order_res = user.place_option_order(new_access_token, order_type, order_price, instruction, symbol, quantity)
                return order_res.status_code
            except ValueError:
                    return 999           
        else:
            return 998


chrome_options = Options()
# Prefer the new headless mode where available
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use Selenium Manager to handle the correct ChromeDriver automatically across OSes
# Do not pass an explicit driver path; Selenium will download/manage the driver.
browser = webdriver.Chrome(options=chrome_options)

url = "https://discord.com/login"
browser.get(url)

browser.find_element(By.NAME, "email").send_keys(email)
browser.find_element(By.NAME, "password").send_keys(password)

browser.find_element(By.XPATH, "//button[@type='submit']").click()

WebDriverWait(browser, 10).until(EC.url_contains(("https://discord.com/channels/")))


# Discord server and channel configuration - replace with your actual values
server_id = os.getenv('DISCORD_SERVER_ID', 'your_server_id_here')
channel_id = os.getenv('DISCORD_CHANNEL_ID', 'your_channel_id_here')

ch_url = f"https://discord.com/channels/{server_id}/{channel_id}"
browser.get(ch_url)

WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//main[@class='chatContent-a9vAAp']")))

# TD Ameritrade client configuration - replace with your actual credentials
follower = TD_Client(
    os.getenv('TD_ACCESS_TOKEN', 'your_access_token_here'),
    os.getenv('TD_ACCOUNT_ID', 'your_account_id_here'), 
    os.getenv('TD_CONSUMER_KEY', 'your_consumer_key_here'),
    os.getenv('TD_REFRESH_TOKEN', 'your_refresh_token_here')
)



async def kindred_task(client, noti_ch):
    await client.wait_until_ready()
    
    channel = client.get_channel(noti_ch)

    n = 0
    ms_list = []
    last_msg = ""
    print("-"*10, "Ready to read messages...", "-"*10)
    while n < 27000: # 9:30am - 4:00pm 6.5hrs = 390 mins = 23,400 seconds + 1 extra hour
        s = time.perf_counter()
        ms_list.clear()
        soup = BeautifulSoup(browser.page_source, "lxml")        
        msgs = soup.find_all("div", attrs={"class": "contents-2mQqc9"})    
        for msg in msgs:
            ms = msg.find("div", attrs={"class": "markup-2BOw-j messageContent-2qWWxC"}).get_text()
            ms_list.append(ms)
        new_last_msg = ms_list[-1]
        
        if last_msg != new_last_msg:
            
            if n == 0:
                pass
            else:
                print("Read message:",new_last_msg)
                await channel.send(f"Read message: {new_last_msg}")

                order_res = copy_option(new_last_msg, follower)
                elapsed = time.perf_counter() - s
                
                if order_res:
                    conf_msg = confirm_msg(order_res, new_last_msg)
                    print(conf_msg)
                    await channel.send(conf_msg)
                    
                print(f"*finished in {elapsed:0.2f} seconds")
                await channel.send(f"*finished in {elapsed:0.2f} seconds")
                print(datetime.now())            

            last_msg = new_last_msg
        
        n += 1
        if n == 26999:
            print("-"*10, "The program is shutting down...(run for 6.5 hours)", "-"*10, "\n")
            browser.quit()

        await asyncio.sleep(1)