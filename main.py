import time
import dht
from machine import Pin
from umqtt.simple import MQTTClient
import neopixel
import json
pixels = neopixel.NeoPixel(machine.Pin(48),1)

# Configuración de MQTT
mqtt_server = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic_sub = b"clima/02"
mqtt_topic_pub = b"clima/01"

# Configuración del sensor DHT11
dht_pin = Pin(12)
dht_sensor = dht.DHT11(dht_pin)

# Configuración del LED integrado
# led_pin = 2
# led = Pin(led_pin, Pin.OUT)

def read_temperature_humidity():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

def mqtt_callback(topic, msg):
    print("Mensaje recibido [{}]: {}".format(topic, msg))
    if msg == b'ON':
        pixels.fill((0,0,255))
        pixels.write()
        # led.value(1)
    elif msg == b"OFF":
        pixels.fill((0,0,0))
        pixels.write()
        # led.value(0)

def mqtt_connect():
    client = MQTTClient("esp32", mqtt_server, port=mqtt_port)
    client.connect()
    client.set_callback(mqtt_callback)
    client.subscribe(mqtt_topic_sub)
    print("Conectado al servidor MQTT")
    return client

def main():
    client = mqtt_connect()

    while True: 
        client.check_msg()

        temperature, humidity = read_temperature_humidity()
        print("Temperatura:", temperature, "°C")
        print("Humedad:", humidity, "%")

        datos = {"Temperatura": temperature, "Humedad": humidity}
        # Convertir el diccionario a una cadena JSON
        json_string = json.dumps(datos)

# Codificar la cadena JSON en bytes utilizando UTF-8
        encoded_data = json_string.encode('utf-8')
        client.publish(mqtt_topic_pub, encoded_data)

        time.sleep(5)

if __name__ == "__main__":
    main()
