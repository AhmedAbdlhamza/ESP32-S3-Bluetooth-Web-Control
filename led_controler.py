import bluetooth
import network
import machine

# define LED strip control pins
LED_PIN = 13
LED_COUNT = 30

# create Bluetooth service
service = bluetooth.BluetoothService(uuid="1234", service_name="LED Control")

# define LED control characteristic
led_char = bluetooth.Characteristic(
    uuid="5678",
    value=bytes([0]),
    properties=(bluetooth.FLAG_READ | bluetooth.FLAG_WRITE),
    write_callback=lambda value: machine.Pin(LED_PIN, machine.Pin.OUT).value(value[0])
)
service.add_characteristic(led_char)

# start Bluetooth service
bluetooth.start_service(service)

# connect to mobile device and get Internet connection
bt = bluetooth.Bluetooth()
bt.advertise_service(service)
while not bt.connected:
    pass
print("Connected to mobile device via Bluetooth!")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
while not sta_if.isconnected():
    sta_if.scan()
    sta_if.connect()
print("Connected to Internet via mobile device!")

# create web server and landing page
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>LED Control</title>
    </head>
    <body>
        <h1>LED Control</h1>
        <p>Current LED status: <span id="led_status"></span></p>
        <button onclick="turn_on()">Turn On</button>
        <button onclick="turn_off()">Turn Off</button>
        <script>
            var led_status = document.getElementById("led_status");
            var led_char = null;

            function connect() {
                navigator.bluetooth.requestDevice({filters: [{services: ['1234']}]})
                    .then(device => device.gatt.connect())
                    .then(server => server.getPrimaryService('1234'))
                    .then(service => service.getCharacteristic('5678'))
                    .then(char => {
                        led_char = char;
                        char.readValue().then(value => {
                            led_status.innerHTML = value.getUint8(0) ? "On" : "Off";
                        });
                        char.startNotifications().then(_ => {
                            char.addEventListener('characteristicvaluechanged', event => {
                                led_status.innerHTML = event.target.value.getUint8(0) ? "On" : "Off";
                            });
                        });
                    })
                    .catch(error => console.log(error));
            }

            function turn_on() {
                if (led_char) {
                    led_char.writeValue(Uint8Array.of(1));
                }
            }

            function turn_off() {
                if (led_char) {
                    led_char.writeValue(Uint8Array.of(0));
                }
            }

            connect();
        </script>
    </body>
</html>
"""
html_len = len(html)

# define HTTP request handler
def http_handler(request):
    request.send(b"HTTP/1.1 200 OK\r\n")
    request.send(b"Content-Type: text/html\r\n")
    request.send(b"Content-Length: " + str(html_len).encode() + b"\r\n")
    request.send(b"\r\n")
    request.send(html.encode())

# create HTTP server
s = socket.socket()
s.bind(('', 80))
s.listen(1)
print("HTTP server started!")

# serve HTTP requests
while True:
    conn, addr = s.accept()
    print("Received connection from:", addr)
    request = conn.recv(1024)
    http_handler(conn)
    conn.close()
