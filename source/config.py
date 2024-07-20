import json

with open('config.json', 'r', encoding='utf-8') as config_json_file:
    data = json.load(config_json_file)

print(data)

WIN_NAME = data['WIN_NAME']
WIN_KEYWORDS = data['WIN_KEYWORDS']
GAME_DIR = data['GAME_DIR']
V5_DIR = data['V5_DIR']
RESOURCE_PATH = data['RESOURCE_PATH']
ICON = data['ICON']

# 默认执行次数
DEFAULT_COUNT = data['DEFAULT_COUNT']
FILED_DEFAULT_COUNT = data['FILED_DEFAULT_COUNT']
# 匹配间隔
M_INTERVAL = data['M_INTERVAL']
# 匹配率阈值
THRESHOLD = data['THRESHOLD']
# 点击坐标偏移随机量 0~CLICK_OFFSET
CLICK_OFFSET = data['CLICK_OFFSET']

# 窗口resize后的大小
RESIZE_XY = data['RESIZE_XY']
# 御魂
YuHun = data['scene']['YuHun']
# 斗技
DouJi = data['scene']['DouJi']
# 结界
Filed = data['scene']['Filed']
# Filed_Count = [
#     'Filed_Finished1.png',
#     'Filed_Finished2.png',
#     # 'Filed_Failed1.png',
#     # 'Filed_Failed2.png'
# ]
# 结界位置相对坐标
Filed_Locs = data['Filed_Locs']

# 是否打印匹配率
SHOW_THRESHOLD = ['SHOW_THRESHOLD']
# 是否显示匹配图像
SHOW_MATCH_TEMP = ['SHOW_MATCH_TEMP']
SHOW_MATCH_TEMPS = ['SHOW_MATCH_TEMPS']
