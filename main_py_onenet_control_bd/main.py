from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython

# ESP8266 ESP-12 ��һ���͵�ƽ������������GPIO2�˿��ϵ�LED
led = Pin(2, Pin.OUT, value=1)

#MQTT�������Ϣ��ʹ��ʱ�޸ĳ��Լ���
SERVER = "183.230.40.39"   #ONENET��������ַ
SERVER_PORT=6002           #ONENET�������˿�
CLIENT_ID = "45729331"      #�����豸ʱ�õ����豸ID��Ϊ�����ִ�
TOPIC = b"zhimadiyled"             #ONENET�ϴ����ݵ���Ҫ������TOPIC
username='176495'           #ע���Ʒʱ��ƽ̨����Ĳ�ƷID��Ϊ�����ִ�
password='wang'  #��Ȩ��Ϣ


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
    #��������Ҫ�ǿͻ���ID����������ַ���������˿ڣ��û���ƷID����Ȩ��Ϣ
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
