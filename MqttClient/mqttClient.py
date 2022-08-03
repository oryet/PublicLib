import queue

import paho.mqtt.client as mqtt
import time

class MqttClientClass:
    def __init__(self, HOST, PORT, USERNAME='admin', PASSWORD='public'):
        self.HOST = HOST    # "192.168.128.155"  # 218.94.38.114
        self.PORT = PORT    # 1883  # 50258
        self.mqttClient = mqtt.Client("pythondevice2|securemode=3,signmethod=hmacsha1|")
        self.mqttClient.username_pw_set(USERNAME, PASSWORD)
        self.on_mqtt_connect()
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数
        self.mqttqueue = queue.Queue()

    # 连接MQTT服务器
    def on_mqtt_connect(self):
        self.mqttClient.connect(self.HOST, self.PORT, 60)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self, lient, userdata, msg):
        # print(msg.topic + " " + ":" + str(msg.payload))
        self.mqttqueue.put(msg)

    # subscribe 消息
    def on_subscribe(self, TopicList, qos=0):
        # 订阅监听自定义Topic
        for Topic in TopicList:
            self.mqttClient.subscribe(Topic, qos)


    def client_publish(self, pub, f, qos=0):
        # 自定义Topic消息上行
        self.on_publish(pub, f, qos)


if __name__ == '__main__':
    HOST = "192.168.128.155"
    PORT = 1883
    SubTopicList = ["TestCaseSch/TestGui/AckBuildFrame", "TestCaseSch/TestGui/AckParseFrame"]
    PubTopicList = ["TestGui/TestCaseSch/ReqBuildFrame", "TestGui/TestCaseSch/ReqParseFrame"]
    oopm = MqttClientClass(HOST, PORT)
    oopm.on_subscribe(SubTopicList)

    f = "{\"token\":\"123456\",\"timestamp\":\"2004-05-03T17:30:08Z\",\"body\":{\"task_sn\":\"1234\",\"schemeID\":\"000001\", \
            \"jsonframe\":{\"buildClass\":\"GetRequestNormal\",\"strAddr\":\"000000000001\",\"iAddrLogic\":\"0\", \
            \"iServiceID\":\"1\",\"strOAD\":\"00100200\"}}}"

    for i in range(10):
        time.sleep(5)
        oopm.client_publish(PubTopicList[0], f)

