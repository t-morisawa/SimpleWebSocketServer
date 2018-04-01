# -*- coding: utf-8 -*-
import json
import HacoServer, HacoMotor
import threading
import time
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

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

if __name__ == "__main__":
    sensor = HacoSensor()
    sensor.startServer()
    while(1):
        sensor.sendToClient(u"{\"method\": \"knock\", \"position\": {\"x\": -0.28, \"y\": 1.77, \"z\": -3.5}}")
        time.sleep(5)
        sensor.sendToClient(u"{\"method\": \"knock\", \"position\": {\"x\": 4.9, \"y\": 0.77, \"z\": 1.6}}")
        time.sleep(5)
