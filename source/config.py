from json import load as load_json

with open('config.json', 'r', encoding='utf-8') as config_json_file:
    data = load_json(config_json_file)

WIN_NAME: str = data['WIN_NAME']
WIN_KEYWORDS: str = data['WIN_KEYWORDS']
GAME_PATH: str = data['GAME_PATH']
V5_PATH: str = data['V5_PATH']
RESOURCE_PATH: str = data['RESOURCE_PATH']
ICON_PATH: str = data['ICON_PATH']
IS_DEBUG: bool = data['IS_DEBUG']
# 默认执行次数
DEFAULT_COUNT: int = data['DEFAULT_COUNT']
FILED_DEFAULT_COUNT: int = data['FILED_DEFAULT_COUNT']
DOWNGRADE_COUNT: int = data['DOWNGRADE_COUNT']
# 匹配间隔
CLICK_INTERVAL: float = data['CLICK_INTERVAL']
# 匹配率阈值
THRESHOLD: float = data['THRESHOLD']
# 点击坐标偏移随机量 0~CLICK_OFFSET
CLICK_OFFSET: int = data['CLICK_OFFSET']

# 窗口resize后的大小
RESIZE_XY = data['RESIZE_XY']
# 御魂
YuHun: list = data['scene']['YuHun']
# 斗技
DouJi: list = data['scene']['DouJi']
# 结界
Filed: list = data['scene']['Filed']
FILED_COUNT_TEMP: list = data['scene']['FILED_COUNT_TEMP']
# 结界位置相对坐标
FILED_LOCS: list = data['FILED_LOCS']

# 是否打印匹配率
SHOW_THRESHOLD: bool = data['SHOW_THRESHOLD']
# 是否显示匹配图像
IS_SHOW_MATCH_TEMP: bool = data['IS_SHOW_MATCH_TEMP']
IS_SHOW_MATCH_TEMPS: bool = data['IS_SHOW_MATCH_TEMPS']
