## rpi0_ws2812b
----------------------------------------------------

### Files :
- rpi0_ws2812b
	- app.py --------------------- 执行文件
	- ws2812b.py ---------------- ws2812b灯串驱动
	- README.md --------------- 说明文档


### Python Version : 
- V3.7.x
- Dependency:
    - paho-mqtt
    - [neopixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython)
    - numpy


### Description :
- 通过Raspberry Pi zero W 控制 ws2812b 显示
- 通过MQTT实现开关机、显示效果切换等功能
- 当程序需要完整更新时在根目录添加update文件即可


### MQTT - API:

- system_control：系统控制：
    - 控制列表如下：
    
|  功能  |  指令  |  
| :----: | :----: |  
|  开机  |  "PowerON" |
|  关机  |  "PowerOFF" |
|  亮度调整  |  ""  |

```
{
    "Command":"system_control",         # 控制模式选择
    "Brightness":0.8,                   # 控制灯串亮度，范围 0 ~ 1，空缺则保持不变
    "Wait_s":60,                        # 延时60秒执行
    "Value":{
        "cmd":"PowerOFF"                # 关机指令
        }
}
```
- mode0：通过灯珠编号独立控制每一个灯珠，示例演示控制第0个灯珠和第一个灯珠的控制方式，其他灯珠以此类推：
```
{
    "Command":"mode0",         # 控制模式选择
    "Brightness":0.8,          # 控制灯串亮度，范围 0 ~ 1，空缺则保持不变
    "Wait_s":120,              # 延时120秒执行
    "Value":{                  # 模式0时的参数，空缺则保持不变
            "0":"255,0,0"      # 第0个灯珠，RGB色彩
            "1":"0,255,0"
    }
}
```
- mode1：显示字符串，由于使用3x5的字体，所以部分字符无法显示：
```
{
    "Command":"mode1",         # 控制模式选择
    "Brightness":0.8,          # 控制灯串亮度，范围 0 ~ 1，空缺则保持不变
    "Wait_s":120,              # 延时120秒执行
    "Value":{
        "str":"hello"          # 参数为需要显示的字符串
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
    "Brightness":0.8,                             # 控制灯串亮度，范围 0 ~ 1，空缺则保持不变
    "Wait_s":120,                                 # 延时120秒执行
    "Value":{
        "effect":"effect01"                       # 参数为预置效果编号
        }
}
```

### Change Log:

- v0.1(2019.05.09):
    - 修改滚动字符串为"HELLO",并修改对应函数等待时间(wait time)为0.15

- v0.1(2019.05.08):
    - 完成远程控制的API

- 2019.05.06：
    - 新增对MQTT通讯的支持
    - 新增说明文档


**Author**         : Jackie Yang  
**Email**          : czyangyinghao@163.com  
**Date**           : 06/05/2019
