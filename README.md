## 说明  
这个插件是基于其他大佬的插件照葫芦画瓢写的出刀记录图片版兼代刀提醒功能,针对Hoshinobot+Yobot的用户  
项目fork自2佬的代刀提醒插件，最近捡起来修了下bug  
原先是加在后面，有用户建议分离开所以最后修修代码弄出来，关于代刀提醒部分我也不是很懂有问题去问2佬（   
本插件使用[GLWTPL(Good Luck With That Public License)](https://github.com/me-shaon/GLWTPL)开源，即： 
- 1.代码处于可用或不可用状态，没有第三种情况。  
- 2.版权所有© 每个人，除了作者  
- 3.在不导致作者被指责或承担责任的情况下，你可以做任何你想要做的事情。  
- 4.祝你好运  
# 已知问题  
和yobot的查树重复响应，有能力的话可以把yobot关于查树的指令改掉  
和挂树计时冲突  
如果有发现其他问题，请立刻联系我或提issues！
### 新的版本已经完全重构了，改动如下  
- 使用数据库存储代刀数据，重启不再丢失数据  
主要功能有：  
1.代刀自动私聊    
2.代挂树私聊   
3.代SL私聊   
4.记录暂停伤害   
5.记录锁助战情况
6.不用登录网页也能看出刀记录/代刀记录  
7.一键提醒所有未出刀的取代@全体  
8.合刀一穿二计算，优点是当前boss不用填血量

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
|**以上为代刀提醒功能基本没动**|**以下是个人魔改**|
|进度表|当天出刀记录
|代刀表|全期代刀记录
|提醒未出刀|提醒所有三刀没出完的人
|合刀 伤害1 伤害2 （血量）|计算合刀，自动获取服务器，可以手动输入血量，也可以自动获取血量
|一穿二 剩余时间s 目标时间s boss血量(不填默认当前boss) |计算一穿二，自动获取服务器，可以手动输入血量，也可以自动获取血量
每天五点（日服四点）会清空所有数据！

# 安装方法：  
yobot源码版用户：  
1.复制daidao.py到modules\daidao\后在_bot_.py中开启（如果你不需要代刀提醒功能复制jingdu.py到modules\jingdu\  
2.pip install imgkit和pip install html-table两个依赖  
3.安装wkhtmltopdf,安装完要把安装路径/bin加进环境变量，下载可以去 [官网](https://wkhtmltopdf.org/downloads.html)或 [这个链接（不保证安全，只是给小白看教程）](http://www.pc6.com/softview/SoftView_559241.html)  用的两台windows测的，linux没试过，不过也有这个软件应该差不多? 
提供从官网下的windous（其他自己去官网下）百度网盘链接：链接：https://pan.baidu.com/s/1b3TMcS_XR-ps7Jm6O5e_Hg 提取码：ratz    
4.将battle.py放进yobot\src\client\ybplugins\clan_battle\ 其实没改只是最后加了个方法，因为每个人都有修改，
所以强烈建议不要替换，直接复制粘贴最后一段!!!!!   
5.如果你是hoshino缝合yobot，不用动；如果你的yobot是独立版，在daidao.py填写你的yobot_url
（非yobot源码版用户前往master分支，不用做第四步，由于无法获取部分数据，公会第一天看不到谁一刀没出，非公会代刀者需加入公会并报刀0才有代刀表，进度表也看不到谁没sl ）  

#### 当前更新内容
 
- 1.代刀表支持不在公会的外援代刀者，增加进度表。现在无论你在不在公会在不在群都能正确显示信息  
- 2.之所以搞个分支是考虑到很多人不是源码版yobot,此分支需改动yobot源码以获取sl数据和公会所有成员数据  
- 3.修复一切需要档案内至少出一刀才能正确显示的bug
- 4.boss完整血量原来需要自己填，现在直接同步yobot,只需改yobot的血量即可
- 5.删除“状态反馈”，能发出来就没必要，发不出来直接改battle.py消息格式,可以以本py做参考（别抄我的到时一起风控了）  
- 目前来看功能已经够我用了，所以如果没bug也不会更新了（大概，有issue会看的
- 非源码版请前往master分支，由于无法获取上面提的数据，公会第一天看不到谁一刀没出，非公会代刀者需加入公会并报刀0才有代刀表，进度表也看不到谁没sl  
- 进度表示例：  
- <img src="https://github.com/othinus001/Daidao/blob/perfect/进度表举例.jpg" width="450" height="600"/><br/>  

**只是个普通的开源插件**

#### 注意：日服yobot目前已经无法支持，本插件高度依赖yobot，后续会提供兼容处理  

### 感谢以下几位大佬  
明见佬[@A-kirami](https://github.com/A-kirami) 优化日志处理方式  
魔法书佬[@mahosho](https://github.com/mahosho) 优化触发器  
[@mhy9989](https://github.com/mhy9989) BUG上报，内容测试  
[@sdyxxjj123](https://github.com/sdyxxjj123) 项目基础fork自他的代码
感谢各位群友，感谢各位使用者！  


