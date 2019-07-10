import websockets
import json
from sinric._mainqueue import queue
from sinric._cbhandler import CallBackHandler
from sinric._jsoncommands import JSON_COMMANDS
from datetime import datetime as dt


class SinricProSocket:

    def __init__(self, apiKey, deviceId, callbacks):
        self.apiKey = apiKey
        self.deviceIds = deviceId
        self.connection = None
        self.callbacks = callbacks
        self.callbackHandler = CallBackHandler(self.callbacks)
        self.enableTrace = False

    def enableRequestPrint(self, bool2):
        self.enableTrace = bool2

    async def connect(self):  # Producer
        self.connection = await websockets.client.connect('ws://23.95.122.232:3001',
                                                          extra_headers={'Authorization': self.apiKey,
                                                                         'deviceids': self.deviceIds},
                                                          ping_interval=30000, ping_timeout=10000)
        if self.connection.open:
            print('Client Connected')
            return self.connection

    # async def sendMessage(self, message):
    #     await self.connection.send(json.dumps(message))

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                if self.enableTrace:
                    print(message)
                requestJson = json.loads(message)
                requestJson[JSON_COMMANDS['TIMESTAMP']] = int(
                    requestJson[JSON_COMMANDS['TIMESTAMP']]) - dt.now().microsecond
                queue.put([requestJson, True, False])
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def handle(self, udp_client):
        while True:
            while queue.qsize() > 0:
                await self.callbackHandler.handleCallBacks(queue.get(), self.connection, udp_client)