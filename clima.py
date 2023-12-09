from machine import Pin
from time import sleep
import dht
from pymongo import MongoClient

# Conectarse a la base de datos MongoDB
client = MongoClient('mongodb+srv://usuario:password@cluster0.ncqopcc.mongodb.net/')
db = client['uni']
collection = db['clima']

#sensor = dht.DHT22(Pin(25))
sensor = dht.DHT11(Pin(12))

while True:
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print('Temperature: %3.1f C' % temp)
        print('Humidity: %3.1f %%' % hum)
        
        # Guardar los datos en la base de datos
        data = {
            'temperature': temp,
            'humidity': hum
        }
        collection.insert_one(data)
        print('Data saved to MongoDB.')
        
    except OSError as e:
        print('Failed to read sensor.')
