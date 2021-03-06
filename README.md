## rpi0_ws2812b
----------------------------------------------------

### Files :
- rpi0_ws2812b
	- app.py --------------------- 执行文件
	- ws2812b.py ---------------- ws2812b灯串驱动
    - mqtt_client ----------------- MQTT客户端驱动


### Python Version : 
- V3.7.x
- Dependency:
    - paho-mqtt
    - [neopixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython)
    - numpy
    - multiprocess


### Description :
- 通过Raspberry Pi zero W 控制 ws2812b 显示
- 通过MQTT实现开关机、显示效果切换等功能
- 当程序需要完整更新时在根目录添加update文件即可


### MQTT - API:

- system_control：系统控制：
    - 控制列表如下：
    
|  功能  |  指令  |  
| :----: | :----: |  
|  开启显示  |  "PowerON" |
|  关闭显示  |  "PowerOFF" |
|    关机    |  "SystemHalt"  |
|    重启    |  "SystemReboot"  |

```
{
    "Command":"system_control",         # 控制模式选择
    "Wait_s":0,                         # 立即执行
    "Brightness":40,                    # 亮度调整，范围为 0~48
    "Value":{
        "cmd":"PowerON"                 # 开启显示
        }
}
```
- change_brightness：改变灯光亮度：
```
{
    "Command":"change_brightness",         # 控制模式选择
    "Brightness":40,                       # 亮度调整，范围为 0~48
}
```
- lightning：照明模式：
```
{
    "Command":"lightning",         # 控制模式选择
    "Wait_s":0,                    # 立即执行
    "Brightness":48,               # 亮度调整，范围为 0~48
    "Value":{}                     # 开启显示
```
- solid_color：纯色显示：
```
{
    "Command":"solid_color",         # 控制模式选择
    "Wait_s":0,                      # 立即执行
    "Brightness":48,                 # 亮度调整，范围为 0~48
    "Value":{
        "color":256                  # 颜色编号 0 ~ 0xFFFFFF, 如果此参数为0则关闭显示
        }       
```
- mode0：通过灯珠编号独立控制每一个灯珠，示例演示控制第0个灯珠和第一个灯珠的控制方式，其他灯珠以此类推：
```
{
    "Command":"mode0",         # 控制模式选择
    "Wait_s":60,               # 延时120秒执行
    "Brightness":40,           # 亮度调整，范围为 0~48
    "Value":{                  # 模式0时的参数，空缺则保持不变
        "0":256,               # 第0个灯珠，RGB色彩 0 ~ 0xFFFFFF
        "1":65536
    }
}
```
- mode1：显示字符串，由于使用3x5的字体，所以部分字符无法显示：
```
{
    "Command":"mode1",         # 控制模式选择
    "Wait_s":120,              # 延时120秒执行
    "Brightness":40,       # 亮度调整，范围为 0~48
    "Value":{
        "str":"hello",         # 参数为需要显示的字符串
        "color":0              # 颜色编号 0 ~ 0xFFFFFF, 如果此参数为0则随机显示
        }
}
```
- mode2：控制显示预置的灯串演示效果：
    - 效果列表如下：  

|   指令   |  效果  |
| :------: | :----: |
|  effect01  |  显示滚动字符串“HELLO” |  
|  effect02  |  随机位置灯珠显示随机颜色 |
|  effect03  |  逐行刷新显示一种颜色 |

```
{
    "Command":"mode2",                            # 控制模式选择
    "Wait_s":120,                                 # 延时120秒执行
    "Brightness":40,                          # 亮度调整，范围为 0~48
    "Value":{
        "effect":"effect01"                       # 参数为预置效果编号
        }
}
```

### Change Log:

- v0.4.03(2019.06.06):
    - 添加纯色显示模式
    - 修改照明模式API 

- v0.4.02(2019.06.04):
    - 修改开机画面为呼吸灯样式
    - 添加照明模式

- v0.4.01(2019.06.03):
    - 修复模式0无法正常使用的BUG

- v0.4(2019.06.03):
    - 将多进程通讯由内存共享机制修改为队列机制，优化执行效率
    - 修复其他BUG

- v0.3(2019.05.31):
    - 重写底层LED驱动，恢复独立的亮度调整指令
    - 修改开机动画为白光渐亮
    - 修复其他BUG

- v0.2.03(2019.05.17):
    - 对于模式1添加修改字符串颜色的API接口

- v0.2.02(2019.05.14):
    - 修改亮度调整机制。删除独立的亮度调整指令
    - 修复其他bug

- v0.2.01(2019.05.13):
    - 修改亮度调整机制，添加独立的亮度调整指令

- v0.2(2019.05.13):
    - 优化进程管理机制
    - 修改开机启动画面为随机显示颜色
    - 添加对于树莓派的软关机指令 “SystemHalt”
    - 添加对于树莓派的重启指令 “SystemReboot”
    - 修复其他bug

- v0.1.01(2019.05.10):
    - 修复开机启动时不显示预设动画的bug

- v0.1(2019.05.10):
    - 修改MQTT服务器地址为本地127.0.0.1

- v0.1(2019.05.09):
    - 修改滚动字符串为"HELLO",并修改对应函数等待时间(wait time)为0.15
    - 修改开机启动机制，现在开机自动循环三个预设效果，直到收到新的指令为止

- v0.1(2019.05.08):
    - 完成远程控制的API

- 2019.05.06：
    - 新增对MQTT通讯的支持
    - 新增说明文档


**Author**         : Jackie Yang  
**Email**          : czyangyinghao@163.com  
**Date**           : 06/05/2019
