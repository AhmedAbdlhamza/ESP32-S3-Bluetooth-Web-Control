# ESP32-S3-Bluetooth-Web-Control
The code defines a Bluetooth service with a single characteristic that controls the LED strip. The characteristic can be read and written to, and when written to, it sets the value of a pin that controls the LED strip

# Here's how the code works:
 
The code starts advertising the Bluetooth service and waits for a connection from a mobile device.

When a connection is established, the code enables the Wi-Fi interface on the ESP32 and connects to the Internet via the mobile device.

The code creates an HTML landing page that displays the current status of the LED strip and provides buttons to turn it on and off.

The code defines an HTTP request handler that serves the landing page when a request is received on port 80.

The code starts an HTTP server and waits for incoming connections.

When a connection is received, the code serves the landing page and closes the connection.

To use the code, you'll need to modify the LED_PIN and LED_COUNT constants to match your specific LED strip configuration. You may also need to adjust the UUIDs for the Bluetooth service and characteristic if you're using a custom Bluetooth profile.

To run the code on your ESP32-S3, you'll need to save it as a 'CircuitPython ' script and upload it to the board. Once the script is running, you should be able to pair your mobile device with the ESP32-S3 over Bluetooth and control the LED strip via the landing page served by the ESP32-S3's HTTP server.
