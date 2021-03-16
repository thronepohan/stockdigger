'''
filter.py
filter stock symbols from: 
https://www.tej.com.tw/webtej/doc/uid.htm
'''
import json
import re

with open("input.txt", 'r', encoding='utf-8') as f:
    input_str = f.read()

codes = re.findall(r'\d{4}', input_str)
codes = [code for code in codes]
data = {}
data["custom_topic"] = codes

with open("output.txt", 'w') as f:
    json.dump(data, f)