import time
import ubinascii
import machine
from umqtt.robust import MQTTClient
from machine import Pin

#MQTT服务端信息，使用时修改成自己的
SERVER = "183.230.40.39"   #ONENET服务器地址
SERVER_PORT=6002           #ONENET服务器端口
CLIENT_ID = "45729331"      #创建设备时得到的设备ID，为数字字串
TOPIC = b"$dp"             #ONENET上传数据点需要传到此TOPIC
username='176495'           #注册产品时，平台分配的产品ID，为数字字串
password='wang'  #鉴权信息
message="{\"hello\":3}"     #即{"hello":1},向名为hello的数据流传1 
message1="{\"hello\":1}"     #即{"hello":1},向名为hello的数据流传1 

msglen=len(message)
tmp=[0,0,0]
tmp[0]='\x03'
tmp[1]=msglen>>8
tmp[2]=msglen&0XFF
message="%c%c%c%s"%(tmp[0],tmp[1],tmp[2],message)    #将消息封装为ONENET要求的格式
message1="%c%c%c%s"%(tmp[0],tmp[1],tmp[2],message1)    #将消息封装为ONENET要求的格式

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server,SERVER_PORT,username,password)
    c.connect()
    print("Connected to %s, uploading 1 to server" % server)
    while True:
        while True:
            time.sleep_ms(2000)
            print(message)
            c.publish(TOPIC, message)
            time.sleep_ms(2000)
            print(message1)
            c.publish(TOPIC, message1)

    c.disconnect()

main()