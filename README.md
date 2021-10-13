# 小真步代刀提醒插件 BY：光的速度（2）  
## 请注意！这是一个测试版！
## 说明  
这个插件是基于其他大佬的插件照葫芦画瓢写的代刀便利通知系统，主要是针对Hoshinobot+Yobot的用户  
部分基础代码来自 https://github.com/pcrbot/filter_knife   
在此表示感谢！（之前找不到插件在哪了没挂出来，致歉）  
如果有研究过我的贵族决斗版本，会发现他们的代码非常相似（）   
本插件使用[GLWTPL(Good Luck With That Public License)](https://github.com/me-shaon/GLWTPL)开源，即： 
- 1.代码处于可用或不可用状态，没有第三种情况。  
- 2.版权所有© 每个人，除了作者  
- 3.在不导致作者被指责或承担责任的情况下，你可以做任何你想要做的事情。  
- 4.祝你好运  
# 已知问题  
和yobot的查树重复响应，有能力的话可以把yobot关于查树的指令改掉  
和挂树计时冲突  
该插件的所有功能使用前，必须保证已经创建公会，且至少有一刀数据，否则会报错   
如果有发现其他问题，请立刻联系我或提issues！
### 新的版本已经完全重构了，改动如下  
- 使用数据库存储代刀数据，重启不再丢失数据  
主要功能有：
1.代刀自动私聊    
2.代挂树私聊 
3.代SL私聊   
4.记录暂停伤害   
5.记录锁助战情况   
来自开学以后代刀量猛增，上期还出现重复代刀结果被顶号的头秃会长被迫写的插件。  
使用方法是：  

| 关键词     | 作用     |
| :-------------: | :-------------:|
|代刀中@成员  | 发起代刀         
|取消代刀(@成员) |取消对某成员的代刀 
|SL@成员|告知成员使用了SL
|挂树@成员|代报挂树，并私聊告知
|代刀列表|查看目前正在被代刀的人的列表
|补偿刀列表 |查看目前已被登记的补偿刀
|查询代刀(@成员)| 可以查询自己或其他成员是否在被代刀  
|查树|查看当前在树上的人
|暂停:伤害（可以是文本）(@成员)|记录暂停伤害（可以代报）
|详细状态|查看目前锁助战，代刀，暂停，挂树的情况
|清空补偿数据|清空当前群的补偿记录
|清空代刀数据|清空当前群的代刀记录
|记录补偿刀：文本|记录当前群补偿刀
|代刀表|简易代刀表生成
|进度表|简易进度表生成
|提醒未出刀|提醒所有三刀没出完的人
|合刀 伤害1 伤害2 （血量）|计算合刀，自动获取服务器，可以手动输入血量，也可以自动获取血量

每天五点（日服四点）会清空所有数据！
# 安装方法：  
yobot源码版用户：  
1.复制该插件到hoshino\modules\daidao,然后在_bot_.py中开启  
2.pip install imgkit和pip install html-table两个依赖  
3.安装wkhtmltopdf,安装完要把安装路径/bin加进环境变量，可以去官网或.[这个链接].(http://www.pc6.com/softview/SoftView_559241.html)  
4.将battle.py放进yobot\src\client\ybplugins\clan_battle\ 其实没改只是最后加了个方法，因为每个人都有修改，且很多人更新了空白间隔（我没更新）  
所以强烈建议不要替换，直接复制粘贴最后一段!!!!!  
（非yobot源码版用户前往master分支，不用做第四步）  

### 注：V0.8版本目前为测试版，在公会战前随时可能需要更新！图片版代刀表可能会在会战后更新！
#### V0.2版本修正   
- 1.追加了挂树列表功能  
- 2.移除了部分错误的代码  
- 3.加入了”详细状态“指令，该指令一键查询目前存在的补偿刀，挂树情况  
- 4.追加了记录暂停伤害的功能  
#### V0.3版本修正
- 1.不兼容性更新，需要删库，更新了代刀伤害表，使现在可以报文本了，比如暂停：5s 400w
- 2.修正部分BUG
- 3.挂树模块更新
#### V0.4版本修正
- 1.不兼容性更新，需要删库，更新了补偿刀表，现在以文本方式记录
- 2.尝试加入了一个检查更新的东西，每天五点检查，当插件有新版本时，会通知超级管理员（如果有多个超级管理员，只会私聊通知第一个）
- 3.自行报挂树，暂停时，不再显示刀手了
- 4.挂树加了挂树计时
- 5.锁助战加了个冒号，避免误触
#### V0.5版本修正
- 1.加入了一个单独的暂停列表
- 2.现在没人暂停或者挂树时，尾刀将不再发送空消息
- 3.修正一个文本问题（取消挂树提示）
#### V0.6版本修正
- 1.适配了V0.94FIX4的group_id参数，您可选择性开启，开启后，当机器人为管理员时，可以主动发起私聊而不需要对方向机器人发起过私聊
已知问题：由于V1.0之后的GOCQ版本发送私聊消息会返回Code=100，插件的提示可能会出现异常，但功能正常使用
#### V0.7版本修正  
- 1.移除了锁助战模块（因为目前日台国均无锁助战）  
- 2.现在尾刀会自动记录一个补偿刀，您也可手动使用记录补偿刀：内容（@成员）来更新它  
- 3.随手写了一个简易的代刀表，但是很乱，希望有人PR个图片版本（）  
- 4.加入了合刀功能，该功能会自动获取yobot的血量，自动判断服务器，血量也可以手动输入。（计算式是我六七个月前写的，非常烂，能用就行）  
- 5.优化触发器，减少误触发[@mahosho](https://github.com/mahosho)  
- 6.优化日志处理方式[@A-kirami](https://github.com/A-kirami)  
#### V0.8版本修正
（注：需要删库，位置一般是C:\Users\Administrator\.hoshino中的Daidao.db）
- 1.加入挂树留言
~~我们公会一直是挂树就挂树不要讲故事~~
- 2.修正尾刀误触
- 3.加入模式切换，可选仅记录模式，不进行私聊，降低机器人冻结风险（目前是全局，后面会做成分群开关）
- 4.加入“状态反馈”，即报刀，尾刀后，由本插件再请求一次当前状态并发送，来缓解yobot吞消息的问题
- 5.现在SL后会自动下树了
- 6.数据更新
#### V0.82版本修正
- 1.修正台服未能及时切换至五阶段的问题
- 2.提前预装国服20S补偿机制
#### 自魔改perfect分支  
需要pip install imgkit和html-table,并安装wkhtmltopdf,安装完要把安装路径/bin加进环境变量)  
用的两台windows测的，linux没试过，不过也有这个软件应该差不多?  
- 1.代刀表支持不在公会的外援代刀者，增加进度表。现在无论你在不在公会在不在群都能正确显示信息  
- 2.之所以搞个分支是考虑到很多人不是源码版yobot,此分支需改动yobot源码以获取sl数据和公会所有成员数据  
- 3.将battle.py放进yobot\src\client\ybplugins\clan_battle\ 其实没改只是最后加了个方法，因为每个人都有修改，且很多人更新了空白间隔（我没更新）  
所以强烈建议不要替换，直接复制粘贴最后一段  
- 非源码版请前往master分支，由于无法获取上面提的数据，公会第一天看不到谁一刀没出，非公会代刀者需加入公会并报刀0才有代刀表，进度表也看不到谁没sl  
- 进度表示例：  
- <img src="https://github.com/othinus001/Daidao/blob/perfect/进度表举例.jpg" width="450" height="600"/><br/>  

**只是个普通的开源插件**

#### 注意：日服yobot目前已经无法支持，本插件高度依赖yobot，后续会提供兼容处理  

### 感谢以下几位大佬  
明见佬[@A-kirami](https://github.com/A-kirami) 优化日志处理方式  
魔法书佬[@mahosho](https://github.com/mahosho) 优化触发器  
[@mhy9989](github.com/mhy9989) BUG上报，内容测试  
感谢各位群友，感谢各位使用者！
yysy我一直以为这插件没人用的（），不过在别的群看到自己插件还是挺惊喜的  


