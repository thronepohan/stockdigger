import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import argparse


URL_HEADER = 'https://tw.stock.yahoo.com/q/ta?s='


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', '-c', help='Category of stocks', type=str, dest="category", default="tech")
    args = parser.parse_args()
    return args

args = parse()

# stocks database
with open("stocks.json","r") as f:
    data = json.load(f)
stocks = data[args.category]

# check old usage record
with open("record.json","r") as f:
    data = json.load(f)
lastBrowsed = data[args.category]["lastBrowsed"] - 1

options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)


index = lastBrowsed
wanna_follow = set()
while True:
    try:
        # next
        if keyboard.is_pressed('q'):
            index += 1
            if index == len(stocks):
                break
            url = URL_HEADER + (str)(stocks[index])
            chrome.get(url)
        # previous
        elif keyboard.is_pressed('a'):
            index -= 1
            if index < 0:
                index = 0
                continue
            url = URL_HEADER + (str)(stocks[index])
            chrome.get(url)
        # save
        elif keyboard.is_pressed('s'):
            wanna_follow.add(stocks[index])
        # delete
        elif keyboard.is_pressed('d'):
            try:
                wanna_follow.remove(stocks[index])
            except Exception:
                pass
        elif keyboard.is_pressed('z'):
            break
        else:
            pass
    except:
        break

# save to json
output_data = {}
output_data[args.category] = {}
output_data[args.category]["wanna_follow"] = list(wanna_follow)
with open("output.json","w") as outfile:
    json.dump(output_data, outfile)


with open("record.json","r") as f:
    data = json.load(f)
data[args.category]["lastBrowsed"] = index
with open("record.json","w") as f:
    json.dump(data, f)

chrome.quit()