from ._jsoncommands import JSON_COMMANDS


class TvController:
    def __init__(self, x):
        self.volume = x
        pass

    async def setVolume(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('volume'))

    async def adjustVolume(self, jsn, callback):
        self.volume += jsn.get(JSON_COMMANDS.get('VALUE')).get('volume')
        if self.volume > 100:
            self.volume = 100
        elif self.volume < 0:
            self.volume = 0
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), self.volume)

    async def setMute(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), )

    async def mediaControl(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('control'))

    async def selectInput(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('input'))

    async def changeChannel(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get('value').get('channel').get('name'))

    async def skipChannels(self, jsn, callback):
        return callback(jsn.get(JSON_COMMANDS.get('DEVICEID')), jsn.get(JSON_COMMANDS.get('VALUE')).get('channelCount'))
