from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython

# ESP8266 ESP-12 有一个低电平触发，连接在GPIO2端口上的LED
led = Pin(2, Pin.OUT, value=1)

#MQTT服务端信息，使用时修改成自己的
SERVER = "183.230.40.39"   #ONENET服务器地址
SERVER_PORT=6002           #ONENET服务器端口
CLIENT_ID = "45729331"      #创建设备时得到的设备ID，为数字字串
TOPIC = b"zhimadiyled"             #ONENET上传数据点需要传到此TOPIC
username='176495'           #注册产品时，平台分配的产品ID，为数字字串
password='wang'  #鉴权信息


state = 0

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
    elif msg == b"off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state


def main(server=SERVER):
    #括号里主要是客户端ID，服务器地址，服务器端口，用户产品ID，鉴权信息
    c = MQTTClient(CLIENT_ID, server,6002,username,password)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            #micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()

main()
