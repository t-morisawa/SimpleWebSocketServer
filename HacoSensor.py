# -*- coding: utf-8 -*-
import json
import HacoServer, HacoMotor
import threading
import time
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

#AD変換用
from gpiozero import MCP3008
import pigpio
import time
import threading
import sys,os

pot0 = MCP3008(channel=0)#右from gpiozero import MCP3008 #AD変換用ライブラリ



"""
Hacoのセンサクラス（仮）
"""
class HacoSensor():
    def __init__(self):
        self.motor = HacoMotor.HacoMotor()

    """
    開発用メソッド
    :param json message
    """
    def printToMotor(self):
        self.motor.printMessage('This is a message from HacoSensor')

    def printToServer(self):
        self.server.printMessage('This is a message from HacoSensor')

    def startServer(self):
        self.websocketserver = SimpleWebSocketServer('', 8000, HacoServer.HacoServer)
        th_server = threading.Thread(target=self.websocketserver.serveforever, name="th_server", args=() )
        th_server.setDaemon(True)
        th_server.start()

    """
    HacoServerクラスのインスタンスを受け取り、このクラスからの情報送信を可能にする
    :return HacoServer: 接続が確立していない場合はNone
    """
    def _getServerInstance(self):
        return self.websocketserver.getConnector()

    """
    websocketクライアントに送信
    接続が確立していない場合は何もしない
    """
    def sendToClient(self, message):
        server = self._getServerInstance()
        if server is not None:
            server.sendMessage(message)

class potentio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) #init threading class
        self.setDaemon(True)
        self.return_value = False
        
    def run(self):
        now0=0 #現在位置
        now1=0
        pre0=0 #一瞬前の位置
        pre1=0
        left=0
        right=0
        move0=0
        move1=0
        print("Reading")

        while 1:
            #time.sleep(5)
            if pot0.value>0.15:
                self.return_value=True
                print("touch now")
            else:
                self.return_value=False
                print(pot0.value)

    def get_value(self):
        return self.return_value
            
if __name__ == "__main__":
    p=potentio()
    p.start()
    
    sensor = HacoSensor()
    sensor.startServer()
    print("start connection")
    count=0
    while(1):
        print(p.get_value())
        if p.get_value()==True:
            print("Touch!!")
            if count==0:
                print("motion 0")
                sensor.sendToClient(u"{\"method\": \"knock\", \"position\": {\"x\": -0.28, \"y\": 1.77, \"z\": -3.5}}")
                count=1
                
            elif count==1:
                print("motion 1")
                sensor.sendToClient(u"{\"method\": \"knock\", \"position\": {\"x\": 4.9, \"y\": 0.77, \"z\": 1.6}}")
                count=2
                
            elif count==2:
                print("motion 2")
                sensor.sendToClient(u"{\"method\": \"knock\", \"position\": {\"x\": 3.55, \"y\": 0.58, \"z\": 5.95}}")
                count=0


        #time.sleep(5)
