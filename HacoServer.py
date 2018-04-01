# -*- coding: utf-8 -*-
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import HacoMotor

"""
Hacoのサーバクラス
"""
class HacoServer(WebSocket):
    def __init__(self, server, sock, address):
        # スーパークラスのコンストラクタの再利用
        super(HacoServer, self).__init__(server, sock, address)
        self.motor = HacoMotor.HacoMotor()

    """
    メッセージ受信時の処理
    ・クライアントにセンサ情報を要求する
    ・クライアントにセンサ情報を送信する
    ・クライアントから要求された情報を送信する
    ・クライアントから送信された情報を処理する
    ・開発用(echo)
    """
    def handleMessage(self):
        try:
            jsonData = json.loads(self.data)
            self.motor.printMessage(jsonData)
            self.sendMessage(self.data)
        except Exception as e:
            print(e.args)
            raise(e)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

    """
    メッセージの内容を解釈して次のアクションを決める
    """
    def controller(self):
        pass

    """
    クライアントにセンサ情報を要求する
    """
    def requestParameters(self):
        pass

    """
    クライアントにセンサ情報を送信する
    クライアントから要求される/サーバが自発的に送信する場合両方ある想定
    """
    def postParameters(self):
        pass

    """
    開発用
    :param * message
    """
    def printMessage(self, message):
        print("[START] message from HacoServer")
        print(message)
        print("[END] message from HacoServer")

if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8000, HacoServer)
    server.serveforever()
