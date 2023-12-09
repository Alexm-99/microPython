import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

ssid = ".:Wifi-Uleam:."
password = "U13aM.2022"
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    pass

print("Conexión exitosa!")
print("Dirección IP:", sta_if.ifconfig()[0])