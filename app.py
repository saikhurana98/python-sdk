import json
from sinric import SinricPro
from sinric import SinricProUdp
from credentials import (
    appKey,
    secretKey,
    deviceIdArr,
    blynkIdArr,
    pwrPinArr,
    rgbPinArr,
    slidePinArr,
    thermpPinArr,
    acId,
)
from time import sleep
import requests

ac_temp = 24

def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    index = deviceIdArr.index(did)
    changePwrState(blynkIdArr[index], pwrPinArr[index], state)
    return True, state


def onSetBrightness(did, state):
    # Alexa set device brightness to 40%
    # print(did, 'BrightnessLevel : ', state)
    return True, state


def onAdjustBrightness(did, state):
    # Alexa increase/decrease device brightness by 44
    index = deviceIdArr.index(did)
    changeBrighness(blynkIdArr[index], slidePinArr[index], state)
    return True, state


def onSetColor(did, r, g, b):
    # Alexa set device color to Red/Green
    index = deviceIdArr.index(did)
    writeColor(blynkIdArr[index], rgbPinArr[index], [r, g, b])
    return True


def onSetColorTemperature(did, value):
    index = deviceIdArr.index(did)
    writeColor(blynkIdArr[index], rgbPinArr[index], [255, 255, 255])
    return True


def onIncreaseColorTemperature(deviceId, value):
    return True, value


def onDecreaseColorTemperature(deviceId, value):
    return True, value


def onTargetTemperature(deviceId, value):
    index = deviceIdArr.index(deviceId)
    ac_temp = value
    setTemp(blynkIdArr[index], thermpPinArr[index], value)
    return True, value

def onCustom(jsn):
    print("************Request Recieved from Sinric Pro Server*********")
    print(json.dumps(dict(jsn), indent=2))
    return True

def Events():
    pass
        # client.event_handler.raiseEvent(acId, 'targetTemperature', data={'value': ac_temp})
        # client.event_handler.raiseEvent(acId, 'currentTemperature', data={'value':ac_temp})

event_callback = {"Events": Events}

callbacks = {
    "powerState": onPowerState,
    "setBrightness": onSetBrightness,
    "adjustBrightness": onAdjustBrightness,
    "setColor": onSetColor,
    "setColorTemperature": onSetColorTemperature,
    "increaseColorTemperature": onIncreaseColorTemperature,
    "decreaseColorTemperature": onDecreaseColorTemperature,
    "targetTemperature": onTargetTemperature,
    "raw": onCustom,
}


def changePwrState(blynk_auth, pin, state):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"

    if state == "On":
        state = 1
    else:
        state = 0
    # print(state)
    querystring = {"value": state}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def changeBrighness(blynk_auth, pin, state):
    url = f"http://188.166.206.43/{blynkIdArr}/update/{pin}"

    querystring = {"value": state}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def writeColor(blynk_auth, pin, rgb):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"
    querystring = {"value": rgb}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Postman-Token": "d001f97e-0181-4e40-8518-56d8890142ec,256ed8fa-93bb-4a16-ad34-96929283b2b0",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def setTemp(blynk_auth, pin, temp):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"

    querystring = {"value": temp}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Postman-Token": "d001f97e-0181-4e40-8518-56d8890142ec,256ed8fa-93bb-4a16-ad34-96929283b2b0",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

if __name__ == "__main__":
    client = SinricPro(
        appKey,
        deviceIdArr,
        callbacks,
        event_callbacks=event_callback,
        enable_log=False,
        restore_states=False,
        secretKey=secretKey,
    )
    # Set it to True to start logging request Offline Request/Response
    udp_client = SinricProUdp(callbacks, deviceIdArr, enable_trace=False)
    client.handle_all(udp_client)
