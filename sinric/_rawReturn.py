"""
 *  Copyright (c) 2019 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""


class RawReturn:
    def __init__(self):
        pass

    async def rawCallback(self, jsn, raw_):
    	return raw_(jsn)
    	