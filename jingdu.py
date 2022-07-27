import asyncio
import base64
import os
import aiohttp
import random
import sqlite3
import math
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from PIL import Image
import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent
import copy
import re
import json
import nonebot
from nonebot import on_command, on_request,MessageSegment
from hoshino import sucmd,config,get_bot
from hoshino.typing import NoticeSession
from multiprocessing import Pool
import requests
import imgkit
from HTMLTable import  HTMLTable

sv = Service('进度表', help_='''
'''.strip())


DAIDAO_DB_PATH = os.path.expanduser('~/.hoshino/daidao.db')
DAIDAO_jpg_PATH = os.path.expanduser('~/.hoshino/')
SUPERUSERS = config.SUPERUSERS
GroupID_ON = True #当GO版本为0.94fix4以上时，允许从群内发起私聊（即使用管理员身份强制私聊，不需要对方主动私聊过），如果低于该版本请不要开启
NOprivate = True #全局开关，启用后，不再尝试私聊，也不会在群内发送“私聊失败”等消息，仅做记录使用，降低机器人冻结风险。
yesprivate = {}#上面填了True 的情况下，还想开私聊的白名单群（留给想只给自己群用的），按逗号隔开
jindu_bt_color="#2b4490"#进度表标题颜色，不懂？百度颜色表
jindu_bg_color="#48a6fb"#进度表表格 背景颜色
jindu_wz_color="#fff"#进度表表格 文字颜色
jindu_bk_color="#181d4b"#进度表表格 边框颜色
'''黑白风格
jindu_bt_color="#2b4490"#进度表标题颜色
jindu_bg_color="#3e4145"#进度表表格 背景颜色
jindu_wz_color="#fffffb"#进度表表格 文字颜色
jindu_bk_color="#d3d7d4"#进度表表格 边框颜色
'''
def get_db_path():
    if not (os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                        "yobot/yobot/src/client/yobot_data/yobotdata.db"))) or os.access(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                                                                                                                      "yobot/yobot/src/client/yobot_data/yobotdata.db")), os.R_OK)):
        return None
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                           "yobot/yobot/src/client/yobot_data/yobotdata.db"))
    return db_path


def get_web_address():
    if not os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                                       "yobot/yobot/src/client/yobot_data/yobot_config.json"))):
        return None
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"
                                               "yobot/yobot/src/client/yobot_data/yobot_config.json"))
    with open(f'{config_path}', 'r', encoding='utf8')as fp:
        yobot_config = json.load(fp)
    website_suffix = str(yobot_config["public_basepath"])
    port = str(hoshino.config.PORT)
    web_address = "http://127.0.0.1" + ":" + port + website_suffix
    return web_address

yobot_url = get_web_address()
if not yobot_url:
    yobot_url = '' #如果非hoshino插件版请填写yobot_config上的链接
    # 获取主页地址：在群内向bot发送指令“手册”，复制bot发送的链接地址，删除末尾的manual/后即为主页地址
    # 例:https://域名/目录/或http://IP地址:端口号/目录/,注意不要漏掉最后的斜杠！

DB_PATH = get_db_path()
if not DB_PATH:
    DB_PATH = ''
    # 例：C:/Hoshino/hoshino/modules/yobot/yobot/src/client/yobot_data/yobotdata.db
    # 注意斜杠方向！！！
    #
Version = '0.8.1'  
# 检查客户端版本

async def get_user_card(bot, group_id, user_id):
    mlist = await bot.get_group_member_list(group_id=group_id)
    for m in mlist:
        if m['user_id'] == user_id:
            return m['card'] if m['card']!='' else m['nickname']
    return str(user_id)

async def get_group_sv(gid:str) -> str:
    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/statistics/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
        server = data["groupinfo"][-1]["game_server"]  # 获取服务器
        return server

def get_apikey(gid:str) -> str:
    # 获取apikey
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f'select apikey from clan_group where group_id={gid}')
    apikey = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    return apikey


async def get_boss_Zhou(gid:str) -> str:

    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/statistics/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
        Zhou = data["challenges"][-1]["cycle"]  # 获取Boss周目
        return Zhou

async def get_boss_Hao(gid:str) -> str:

    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/statistics/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
        Hao = data["challenges"][-1]["boss_num"]  # 获取Boss号
        return Hao

async def get_boss_HP(gid:str) -> str:

    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/daidao/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
        if  data["challenges"]!=[]:
            boss_hp = data["challenges"][-1]["health_ramain"]  # 获取最后一刀的boss血量
        else:
            boss_hp=6000000
        if boss_hp == 0:
           boss_hp=data["groupinfo"][-1]["now_full_health"]
        return boss_hp




async def get_dao(gid:str) -> str:
    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/daidao/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
    with open(os.path.join(os.path.dirname(__file__),f"data.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
    challenges = data['challenges']
    dao = {}
    members = data['members']
    for member in members:
        dao[member['qqid']] = 0
    for challenge in challenges:
        if challenge['is_continue'] == False:
            num = 1
        else:
            num = 0.5
        if challenge['health_ramain'] == 0:
            num = 0.5
        if challenge['behalf'] == None or challenge['behalf'] == challenge['qqid']:
         try:
            dao[challenge['qqid']] += num
         except:
           dao[challenge['qqid']] = 0
           dao[challenge['qqid']] += num
        if challenge['behalf'] != None:
            continue
    return dao

async def get_dai(gid:str) -> str:
    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/daidao/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
    with open(os.path.join(os.path.dirname(__file__),f"data.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
    challenges = data['challenges']
    dai = {}
    members = data['members']
    for member in members:
        dai[member['qqid']] = 0
    for challenge in challenges:
        if challenge['is_continue'] == False:
            num = 1
        else:
            num = 0
        if challenge['damage'] == 0:
            continue
        if challenge['behalf'] == None:
            continue
        if challenge['behalf'] != None and challenge['behalf'] != challenge['qqid']:
          try:
            dai[challenge['behalf']] += num
          except:
            dai[challenge['behalf']] = 0
            dai[challenge['behalf']] += num
    return dai

@sv.on_fullmatch('代刀表')
async def cddqk(bot,ev):
    gid = ev.group_id
    dao = await get_dao(gid)
    dai = await get_dai(gid)
    table = HTMLTable(caption='代刀表')
    # 表头行
    table.append_header_rows((
    ("名字", "出刀数", "代刀数", "总出刀"),))

    for qq in dai:
        try:
            name = (await bot.get_group_member_info(group_id=ev.group_id,user_id=qq))['card']
            if name == '':name = (await bot.get_group_member_info(group_id=ev.group_id,user_id=qq))['nickname']
        except:
            name = "不在群成员"
        if qq in dao:
           a=dao[qq]+dai[qq]
           if a != 0:
            table.append_data_rows(((name,str(dao[qq]), str(dai[qq]), str(dao[qq]+dai[qq])),))
        else:
           a=dai[qq]
           if a != 0:
            table.append_data_rows(((name,'0', str(dai[qq]), str(dai[qq])),))
    table.caption.set_style({
    'font-size': '15px',})
    table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'keep-all',
    'white-space': 'nowrap',
    'font-size': '14px',})
    table.set_cell_style({
    'width': "250px",
    'border-color': '#000',
    'border-width': '1px',
    'border-style': 'solid',
    'padding': '5px',})
    table.set_header_row_style({
    'color': '#fff',
    'background-color': '#48a6fb',
    'font-size': '18px',})
    table.set_header_cell_style({
    'padding': '15px',})


    newdao = ''

    table[1].set_cell_style({
    'padding': '8px',
    'font-size': '15px',})
    
    for row in table.iter_data_rows():
      introw = int(row[2].value)  
      if introw > 10: #看看哪些人被代的多
         row.set_style({
             'background-color': '#ffdddd',})
    body = table.to_html()
    # html的charset='UTF-8'必须加上，否则中午会乱码
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{0}</body></html>".format(body)
    #tb.add_row([name,str(dao[qq]), str(dai[qq]), str(dao[qq]+dai[qq])])
    imgkit.from_string(html, DAIDAO_jpg_PATH +'out.jpg')
    await bot.send(ev,MessageSegment.image(f'file:///{DAIDAO_jpg_PATH}\\out.jpg'))
    

@sv.on_prefix(["合刀"])
async def hedao(bot, ev):
    args = ev.message.extract_plain_text().split()
    boss_HP={}
    if not args:
        return
    if len(args) < 2:
        return
    gid = str(ev['group_id'])
    if len(args) == 2:
        boss_HP[gid] = float(await get_boss_HP(gid))
    if len(args) == 3:
        boss_HP[gid] = args[2]
    server = str(await get_group_sv(gid))
    if server == 'cn':
        bz = 20
        mode = '国服'
    else:
        bz = 20
        mode = '日/台服'
    a = float(args[0])
    b = float(args[1])
    if a < 10000:
        a = 10000 * a
    if b < 10000:
        b = 10000 * b
    c = float(boss_HP[gid])
    if c < 10000:
        c = 10000 * c
    d = int(c)
    if a>c :
        time = ((1-(c)/a)*90+bz)
        if time > 90 :
            time = (90)
        time = math.ceil(time)
        msg = f"存在可以直接收尾的刀，请确认！刀1直出可补偿{time}秒"
        await bot.send(ev, msg)
    if b>c :
        time2 = ((1-(c)/b)*90+bz)
        if time2 > 90 :
            time2 = (90)
        time2 = math.ceil(time2)
        msg = f"存在可以直接收尾的刀，请确认！刀2直出可补偿{time2}秒"
        await bot.send(ev, msg)
    if (a+b>c):
        time = ((1-(c-a)/b)*90+bz)
        if time > 90 :
            time = (90)
        time2 = ((1-(c-b)/a)*90+bz)
        if time2 > 90 :
            time2 = (90)
        time = math.ceil(time)
        time2 = math.ceil(time2)
        msg = f"当前BOSS血量为{d}\n若1先2后，则补偿{time}秒，若2先1后，则补偿{time2}秒\n当前群为{mode}！"
        await bot.send(ev, msg)
    if (a+b<c):
        msg = f"当前BOSS血量为{d}\n这两刀打不死！"
        await bot.send(ev, msg)
        
async def get_daotd(gid:str) -> str:
     apikey = get_apikey(gid)
     url = f'{yobot_url}clan/{gid}/daidao/api/?apikey={apikey}'
     print(apikey)
     session = aiohttp.ClientSession()
     async with session.get(url) as resp:
        data = await resp.json()
     with open(os.path.join(os.path.dirname(__file__),f"data.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
     challenges = data['challenges']
     daotd = {}
     daote = {}#测试用，计算已出刀数
     members = data['members']
     n = '0'
     daots = '0'
     n = int(n)
     daotdu = []#记录补偿刀和完整刀
     daotds = [] 
     sl=False
     for challenge in challenges:
        if challenge['challenge_pcrdate'] > n:
            n = challenge['challenge_pcrdate'] #得出最近一天
     for member in members:
       daote[member['qqid']] = 0
       for challenge in challenges:
          try:                                 #这里利用daote，再tryexcept找出出了刀被踢出公会(buyi)的人
           if challenge['challenge_pcrdate'] == n and member['qqid']==challenge['qqid']:
             daote[challenge['qqid']] += 1
             cdb = str(challenge['damage'])
             qqid = str(challenge['qqid'])
             ic = str(challenge['is_continue'])
             hr = str(challenge["health_ramain"])
             cy = str(challenge["cycle"])
             bn = str(challenge["boss_num"])
             daotdu.append(cdb)
             daotdu.append(ic)
             daotdu.append(hr)
             daotdu.append(cy)
             daotdu.append(bn) 
          except:
           if challenge['challenge_pcrdate'] == n:
             cdb = str(challenge['damage'])
             qqid = str(challenge['qqid'])
             daote[qqid] += 1
             ic = str(challenge['is_continue'])
             hr = str(challenge["health_ramain"])
             cy = str(challenge["cycle"])
             bn = str(challenge["boss_num"])
             daotds.append(cdb)
             daotds.append(ic)
             daotds.append(hr)
             daotds.append(cy)
             daotds.append(bn)
             daotds.append("???")             
             daots =challenge['qqid']                  
       if member['sl']==n:sl=True
       daotdu.append(sl) 
       daotd[member['qqid']] = daotdu             #得出字典下数组：【出刀伤害，是否为补偿刀，boss剩余血量，第几周目，几号boss】
       if daots!='0':
        daotd[daots] = daotds   
       daotdu = [] 
       daotds = []
       daots ='0'  
       sl=False        
       
     return daotd                                             
                                              
@sv.on_fullmatch('进度表')                   
async def cddqkj(bot,ev):                   #由代刀表魔改而来，思路一致：
    gid = ev.group_id
    dao = await get_daotd(gid)             #get_daotd获取json,获取数组,之后分析数组，靠穷举得出所有出刀可能性
    daoz = await get_daoz(gid)            #get_daoz再次读取上面获取的json,获取数组包括(当前周目,boss,剩余血量,总刀数)
    c = daoz[0]                          #未来还有可能完善的地方：json里member并没有公会里没出刀的人，所以没有这一行，意味着第一天看不到谁一刀没出
    b = daoz[1]  
    h = daoz[2]  
    hz =daoz[4] 
    daozz = daoz[3]                           
    daozs = 90 - daozz
    sl=''
    table = HTMLTable(caption=f'进度表 已出{daozz}刀,还剩{daozs}刀 当前状态{c}-{b}-({h}/{hz}) 指令"提醒未出刀"内测中')
    table.append_header_rows((
    ("名字", "第一刀", "", "第二刀", "","第三刀","","是否sl"),))
    table[0][1].attr.colspan = 2
    table[0][3].attr.colspan = 2
    table[0][5].attr.colspan = 2
    ta=table.append_header_rows
    n = 0
    print('nnnnnnnnnnnnnnnnnnnnnnnnnnn')
    for qq in dao:                                                                          #别问，问就是穷举
        try:
            name = (await bot.get_group_member_info(group_id=ev.group_id,user_id=qq))['card']
            if name == '':name = (await bot.get_group_member_info(group_id=ev.group_id,user_id=qq))['nickname']
        except:
            name = f'qq{qq}'
        n+=1 
        if len(dao[qq])==6:        
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           if dao[qq][5]==False:sl=''
           if dao[qq][5]==True:sl='用掉了'
           if dao[qq][5]=="???":sl="未知"
        if len(dao[qq])==11:
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           cybs2=f'{str(dao[qq][5])}({str(dao[qq][8])}-{str(dao[qq][9])})'
           if dao[qq][10]==False:sl=''
           if dao[qq][10]==True:sl='用掉了'
           if dao[qq][10]=="???":sl="未知"
        if len(dao[qq])==16:
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           cybs2=f'{str(dao[qq][5])}({str(dao[qq][8])}-{str(dao[qq][9])})'
           cybs3=f'{str(dao[qq][10])}({str(dao[qq][13])}-{str(dao[qq][14])})'
           if dao[qq][15]==False:sl=''
           if dao[qq][15]==True:sl='用掉了'
           if dao[qq][15]=="???":sl="未知"
        if len(dao[qq])==21:
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           cybs2=f'{str(dao[qq][5])}({str(dao[qq][8])}-{str(dao[qq][9])})'
           cybs3=f'{str(dao[qq][10])}({str(dao[qq][13])}-{str(dao[qq][14])})'
           cybs4=f'{str(dao[qq][15])}({str(dao[qq][18])}-{str(dao[qq][19])})'
           if dao[qq][20]==False:sl=''
           if dao[qq][20]==True:sl='用掉了'
           if dao[qq][20]=="???":sl="未知"
        if len(dao[qq])==26:
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           cybs2=f'{str(dao[qq][5])}({str(dao[qq][8])}-{str(dao[qq][9])})'
           cybs3=f'{str(dao[qq][10])}({str(dao[qq][13])}-{str(dao[qq][14])})'
           cybs4=f'{str(dao[qq][15])}({str(dao[qq][18])}-{str(dao[qq][19])})'
           cybs5=f'{str(dao[qq][20])}({str(dao[qq][23])}-{str(dao[qq][24])})'
           if dao[qq][25]==False:sl=''
           if dao[qq][25]==True:sl='用掉了'
           if dao[qq][25]=="???":sl="未知"
        if len(dao[qq])==31:
           cybs1=f'{str(dao[qq][0])}({str(dao[qq][3])}-{str(dao[qq][4])})'
           cybs2=f'{str(dao[qq][5])}({str(dao[qq][8])}-{str(dao[qq][9])})'
           cybs3=f'{str(dao[qq][10])}({str(dao[qq][13])}-{str(dao[qq][14])})'
           cybs4=f'{str(dao[qq][15])}({str(dao[qq][18])}-{str(dao[qq][19])})'
           cybs5=f'{str(dao[qq][20])}({str(dao[qq][23])}-{str(dao[qq][24])})'
           cybs6=f'{str(dao[qq][25])}({str(dao[qq][28])}-{str(dao[qq][29])})'
           if dao[qq][30]==False:sl=''
           if dao[qq][30]==True:sl='用掉了'
           if dao[qq][10]=="???":sl="未知"
        if len(dao[qq])==1:                                                                  #一刀都没出的懒狗
           if dao[qq][0]==False:sl=''
           if dao[qq][0]==True:sl='用掉了'
           if dao[qq][0]=="???":sl="未知"
           ta(((name,'','','','','','',sl),)) 
           table[n][1].attr.colspan = 2
           table[n][3].attr.colspan = 2
           table[n][5].attr.colspan = 2

        if len(dao[qq])==6:                                                                  #共出了一刀
           if str(dao[qq][2])== '0':                                                         #第一刀是尾刀
               ta(((name,cybs1,'','','','','',sl),))
               table[n][3].attr.colspan = 2
               table[n][5].attr.colspan = 2
           else:                                                                             #第一刀是完整刀
               ta(((name,cybs1,'','','','','',sl),))
               table[n][1].attr.colspan = 2
               table[n][3].attr.colspan = 2
               table[n][5].attr.colspan = 2
        if len(dao[qq])==11:                                                                 #共出了两刀
           if str(dao[qq][2])== '0':                                                         #1尾2补
               ta(((name,cybs1,cybs2,'','','','',sl),))
               table[n][3].attr.colspan = 2
               table[n][5].attr.colspan = 2
           else:                                                                             #第一刀是完整刀
             if str(dao[qq][7])== '0':                                                       #1完2尾
               ta(((name,cybs1,'',cybs2,'','','',sl),))
               table[n][1].attr.colspan = 2
               table[n][5].attr.colspan = 2
             else:                                                                           #1完2完
               ta(((name,cybs1,'',cybs2,'','','',sl),))
               table[n][1].attr.colspan = 2
               table[n][3].attr.colspan = 2
               table[n][5].attr.colspan = 2
        if len(dao[qq])==16:                                                                 #共出了三刀
           if str(dao[qq][2])== '0':
              if str(dao[qq][12])== '0':                                                     #1尾2补3尾 
               ta(((name,cybs1,cybs2,cybs3,'','','',sl),))
               table[n][5].attr.colspan = 2
              else:                                                                          #1尾2补3完
               ta(((name,cybs1,cybs2,cybs3,'','','',sl),))
               table[n][3].attr.colspan = 2
               table[n][5].attr.colspan = 2
           else:
              if str(dao[qq][7])== '0':                                                      #1完2尾3补
                ta(((name,cybs1,'',cybs2,cybs3,'','',sl),))
                table[n][1].attr.colspan = 2
                table[n][5].attr.colspan = 2
              else:                                                                          #1完2完3尾
                if str(dao[qq][12])== '0':
                  ta(((name,cybs1,'',cybs2,'',cybs3,'',sl),))
                  table[n][1].attr.colspan = 2 
                  table[n][3].attr.colspan = 2
                else:                                                                        #1完2完3完
                   ta(((name,cybs1,'',cybs2,'',cybs3,'',sl),))
                   table[n][1].attr.colspan = 2
                   table[n][3].attr.colspan = 2
                   table[n][5].attr.colspan = 2
        if len(dao[qq])==21:                                                                 #共出了四刀
           if str(dao[qq][2])== '0':
              if str(dao[qq][12])== '0':                                                     #1尾2补3尾4补
               ta(((name,cybs1,cybs2,cybs3,cybs4,'','',sl),))
               table[n][5].attr.colspan = 2
              else: 
                 if str(dao[qq][17])== '0':                                                  #1尾2补3完4尾
                   ta(((name,cybs1,cybs2,cybs3,'',cybs4,'',sl),))
                   table[n][3].attr.colspan = 2
                 else:                                                                       #1尾2补3完4完
                     ta(((name,cybs1,cybs2,cybs3,'',cybs4,'',sl),))
                     table[n][3].attr.colspan = 2
                     table[n][5].attr.colspan = 2
           else:
              if str(dao[qq][7])== '0':                                                      #1完2尾3补4尾
                 if str(dao[qq][17])== '0':
                   ta(((name,cybs1,'',cybs2,cybs3,cybs4,'',sl),)) 
                   table[n][1].attr.colspan = 2
                 else:                                                                       #1完2尾3补4完
                   ta(((name,cybs1,'',cybs2,cybs3,cybs4,'',sl),)) 
                   table[n][1].attr.colspan = 2
                   table[n][5].attr.colspan = 2
              else:                                                                          #1完2完3尾4补
                   ta(((name,cybs1,'',cybs2,'',cybs3,cybs4,sl),))
                   table[n][1].attr.colspan = 2
                   table[n][3].attr.colspan = 2
        if len(dao[qq])==26:                                                                 #共出了五刀
           if str(dao[qq][22]) == '0' and str(dao[qq][21]) == 'False':                       #1尾2补3尾4补5尾
                   ta(((name,cybs1,cybs2,cybs3,cybs4,cybs5,'',sl),))
           if str(dao[qq][22]) != '0' and str(dao[qq][21])== 'False':                        #1尾2补3尾4补5完
                   ta(((name,cybs1,cybs2,cybs3,cybs4,cybs5,'',sl),))
                   table[n][5].attr.colspan = 2
           if str(dao[qq][12])!= '0' and str(dao[qq][11])== 'False':                         #1尾2补3完4尾5补
                   ta(((name,cybs1,cybs2,cybs3,'',cybs4,cybs5,sl),))
                   table[n][3].attr.colspan = 2
           if str(dao[qq][2])!= '0' and str(dao[qq][1])== 'False':                           #1完2尾3补4尾5补
                   ta(((name,cybs1,'',cybs2,cybs3,cybs4,cybs5,sl),))
                   table[n][1].attr.colspan = 2
        if len(dao[qq])==31:                                                                 #1尾2补3尾4补5尾6补
                   ta(((name,cybs1,cybs2,cybs3,cybs4,cybs5,cybs6,sl),))

    table.caption.set_style({
    'font-size': '30px',
    'padding':'10px 0px',
    'color':jindu_bt_color,})
    table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'keep-all',
    'white-space': 'nowrap',
    'font-size': '20px',
    'margin':'auto',})
    table.set_cell_style({
    'width': '250px',
    'border-color': jindu_bk_color,
    'border-width': '1px',
    'border-style': 'solid',
    'font-size': '20px',
    'align':'center',})
    table.set_header_row_style({
    'color': jindu_wz_color,
    'background-color': jindu_bg_color,
    'font-size': '15px',})
    table.set_header_cell_style({
    'padding': '15px',})


    body = table.to_html()
    # html的charset='UTF-8'必须加上，否则中午会乱码
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{0}</body></html>".format(body)
    imgkit.from_string(html, DAIDAO_jpg_PATH +'out.jpg')
    await bot.send(ev,MessageSegment.image(f'file:///{DAIDAO_jpg_PATH}\\out.jpg'))
    
async def get_daoz(gid:str) -> str:                  
    apikey = get_apikey(gid)
    url = f'{yobot_url}clan/{gid}/daidao/api/?apikey={apikey}'
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        data = await resp.json()
    with open(os.path.join(os.path.dirname(__file__),f"data.json"), "w", encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4,ensure_ascii=False))
    challenges = data['challenges']
    daoz = {}  #提取每人刀数
    shuju = []#返一个数组回去包括(周目,boss,剩余血量,总刀数,完整血量）,一次性调用完
    n =0   #天
    if  data["challenges"]!=[]:
     c = data["challenges"][-1]["cycle"]          #周目
     b = data["challenges"][-1]["boss_num"]       #boss
     h = data["challenges"][-1]["health_ramain"]  #剩余血量
    else:
     c=1
     b=1
     h=6000000
    nfh=data["groupinfo"][-1]["now_full_health"]
    daozz = 0                                    #当天总刀数
    members = data['members']
    for challenge in challenges:
        if challenge['challenge_pcrdate'] > n:
            n = challenge['challenge_pcrdate'] #得出最近一天
    for member in members:
           daoz[member['qqid']] = 0
    for challenge in challenges:              #有一种情况暂不考虑：出了刀后踢出公会
      if challenge['challenge_pcrdate']==n:
        if challenge['is_continue'] == False:
            num = 1
        else:
            num = 0.5
        if challenge['health_ramain'] == 0:
            num = 0.5
        try:           
           daoz[challenge['qqid']] += num
        except:
           daoz[challenge['qqid']]=0
           daoz[challenge['qqid']] += num     #排除一种情况：出刀后被踢了
    for qq in daoz:                     #未来还有可能完善的地方
        daozz += daoz[qq]
    shuju.append(c)
    shuju.append(b)
    shuju.append(h)
    shuju.append(daozz)
    shuju.append(nfh)
    return shuju

@sv.on_fullmatch('提醒未出刀')                   
async def txwcd(bot,ev):                   #由代刀表魔改而来，思路一致：
    gid = ev.group_id
    if not hoshino.priv.check_priv(ev, hoshino.priv.ADMIN):
        await bot.send(ev,message = '仅限管理可用',at_sender = True)
        return
    dao = await get_daotd(gid) 
    
    msgTX = "未出完刀的来出刀了:\n"
    for qq in dao:                                                                          #别问，问就是穷举
        try:
            name = (await bot.get_group_member_info(group_id=ev.group_id,user_id=qq))['nickname']
        except:
            name = f'qq{qq}'
            continue
        if len(dao[qq])==1:
           msgTX += f"[CQ:at,qq={qq}]"            
        if len(dao[qq])==6:
           msgTX += f"[CQ:at,qq={qq}]"    
        if len(dao[qq])==11:
           msgTX += f"[CQ:at,qq={qq}]" 
        if len(dao[qq])==16:
          if str(dao[qq][2])!= '0'and str(dao[qq][7])!= '0' and str(dao[qq][12])!= '0':
             msg =''
          else:
                msgTX += f"[CQ:at,qq={qq}]"
        if len(dao[qq])==21:
          if str(dao[qq][2])!= '0'and str(dao[qq][7])!= '0': msg =''
          elif str(dao[qq][2])== '0'and str(dao[qq][7])!= '0' and str(dao[qq][17])!= '0': msg =''
          elif str(dao[qq][2])!= '0'and str(dao[qq][7])== '0' and str(dao[qq][17])!= '0': msg =''
          elif str(dao[qq][2])== '0'and str(dao[qq][7])== '0' and str(dao[qq][12])!= '0'and str(dao[qq][17])!= '0': msg =''
          else:
             msgTX += f"[CQ:at,qq={qq}]"                                
        if len(dao[qq])==26:
          if str(dao[qq][22]) == '0' and str(dao[qq][21]) == 'False': 
             msgTX += f"[CQ:at,qq={qq}]"
    await bot.send(ev, msgTX)

@sv.on_prefix(["一穿二"])
async def ycr(bot, ev):
    args = ev.message.extract_plain_text().split()    
    gid = ev.group_id
    helpmsg="指令如下：\n 一穿二 剩余时间s 目标时间s boss血量(不填默认当前boss) \ns可不填，w视为万，少于一万自动乘万\n例：一穿二 50 80 1000"
    if not args:
        await bot.send(ev,  '输入错误！\n'+helpmsg )       
        return
    boss_HP = {}
    if len(args) != 3 and len(args) != 2:
        await bot.send(ev,  '输入错误！\n'+helpmsg )
        return
    if len(args) == 2:
        boss_HP[gid] = float(await get_boss_HP(gid))
        c = float(boss_HP[gid])
        t = args[0].strip('sS')
        tt = args[1].strip('sS')
        t = int(t)
        tt = int(tt)
        if tt < 0 or tt > 90 or t < 0 or t > 90:
           msg = "两个数据的情况下必须都为时间，可以不带s,必须在90s内"+helpmsg
           await bot.send(ev, msg)
           return
        if tt -t <= 20:
           msg = "已经满足条件,现有时间+20s"
           await bot.send(ev, msg)
           return
        bt = c-(110-tt)*c/(90-t)
        bt = math.ceil(bt)
        bt = formatNum(bt)
        msg = f"boss血量为{c}\n当前剩余{t}s,想让此刀达到{tt}s需要垫{bt}伤害\n"
        await bot.send(ev, msg)
    if len(args) == 3:
       c = args[2].replace('w', '0000').replace('W', '0000').replace('万', '0000').split(' ')
       c = float(''.join(c))
       t = args[0].strip('sS')
       tt = args[1].strip('sS')
       t = int(t)
       tt = int(tt)
       if c<10000:
         c = c*10000
       if tt < 0 or tt > 90 or t < 0 or t > 90:
           msg = "两个数据的情况下必须都为时间，可以不带s,必须在90s内" + helpmsg
           await bot.send(ev, msg)
           return
       if tt -t <= 20:
           msg = "已经满足条件,现有时间+20s"
           await bot.send(ev, msg)
           return
       bt = c - (110 - tt) * c / (90 - t)
       bt = math.ceil(bt)
       bt = formatNum(bt)
       msg = f"boss血量为{c}\n当前剩余{t}s,想让此刀达到{tt}s需要垫{bt}伤害\n"
       await bot.send(ev, msg)     
       
def formatNum(num):    #伤害万位分割，如1,4567,0000
    num=str(num)
    pattern=r'(\d+)(\d{4})((,\d{4})*)'
    while True:
        num,count=re.subn(pattern,r'\1,\2\3',num)
        if count==0:
            break
    return num
    