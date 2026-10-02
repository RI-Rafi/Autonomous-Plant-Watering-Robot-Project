import network, socket, time, gc
from machine import UART, Pin, PWM
from water2 import water2
from pump_water import pump
from temperature import temp, run_cycle
from buzzer import buzz
from stepper import stepper
from distance import measure_distance
from dist2 import measure_dist2
No_Water = False
water_back = 0
# --------- USER: set your Wi‑Fi credentials ----------
#SSID = "Your_Network_Name"
#PASSWORD = "Your_WiFi_Password"
SSID = "uarti"
PASSWORD = "22201791"
# ------------------------------------------------------

# UART0 on GP16 (TX) / GP17 (RX) at 9600 baud — matches your prior code
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
led = Pin("LED", Pin.OUT)

# Tiny, simple HTML page (very light for the Pico W)
PAGE = b"""\
HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Cache-Control: no-store\r
Connection: close\r
\r
<!doctype html>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Pico W — Robot Controls</title>
<style>
  body{font-family:system-ui,Arial,sans-serif;margin:18px;text-align:center}
  .row{display:flex;justify-content:center;gap:12px;margin:12px 0}
  button{min-width:110px;padding:16px;font-size:16px;border-radius:10px;border:1px solid #ccc}
</style>
<h1>Robot Control</h1>
<div class=row>
  <form action="/left"><button>Left</button></form>
  <form action="/forward"><button>Forward</button></form>
  <form action="/right"><button>Right</button></form>
</div>
<div class=row>
  <form action="/back"><button>Back</button></form>
  <form action="/stop"><button>Stop</button></form>
  <form action="/water"><button>Water</button></form>
</div>
<div class=row>
  <form action="/auto"><button>auto</button></form>
  <form action="/shelter"><button>Shelter</button></form>
</div>
<p style="opacity:.7;font-size:12px">Pico W web→UART bridge</p>
"""
def pump_water(time = round(run_cycle(), 2)):
    global No_Water, water_back
    print(time, 'water_time')
    if not No_Water:
      x, y = pump(time)
      water_back = 25-y
      if not x: No_Water = True
      print("Watered for:", time, "seconds...")
    else:
        No_Water = True
        buzz()
def send(cmd: str):
    """Send a single command with newline over UART."""
    uart.write((cmd + "\n").encode())
def auto():
    print("Hello")
    #send("LINE_ON")
    send("Farward")
    #time.sleep(0.2)
    #send("Frward_Stop")
    if measure_distance() < 10:
        # creep a little more
        send("Forward"); time.sleep(0.15); send("Forward_Stop")
        if measure_distance() < 7:
            watering()

def watering():
    print("Starting...Temperature:", temp())
    #print("Time 5 seconds")
    #time.sleep(5)
    dist = measure_distance()
    print(dist, 'distance')
    if not No_Water and dist < 9:
        buzz(True)
        stepper("Up") 
        time.sleep(0.5)
        stepper("Down")
        pump_water()
        return
 
    else:
        
        print("Water Empty main.py")
        buzz()       


def connect_wifi(ssid: str, password: str, timeout_s: int = 20) -> str:
    """Connect to Wi‑Fi (STA). Returns assigned IP."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Optional: better stability/power; safe if unsupported
    try:
        wlan.config(pm=0xA11140)
    except Exception:
        pass
    wlan.connect(ssid, password)

    t0 = time.ticks_ms()
    led.value(0)
    while not wlan.isconnected():
        # Blink while connecting
        led.toggle()
        time.sleep(0.25)
        if time.ticks_diff(time.ticks_ms(), t0) > timeout_s * 1000:
            raise RuntimeError("Wi‑Fi connection timed out")
    led.value(1)
    return wlan.ifconfig()[0]

def serve():
    """Very small blocking HTTP server."""
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print("Listening on http://%s/" % ip)

    while True:
        try:
            cl, _ = s.accept()
            req = cl.recv(1024)  # small header is enough
            # Parse the first line: GET /path HTTP/1.1
            first = req.split(b"\r\n", 1)[0]
            parts = first.split()
            path = parts[1] if len(parts) >= 2 else b"/"

            # Normalize to handle '/forward' and '/forward?'
            if path.startswith(b"/forward"):
                send("Forward")
                time.sleep(0.2)
                send("Forward_Stop")
            elif path.startswith(b"/back"):
                send("Back")
                time.sleep(0.1)
                send("Back_Stop")
            elif path.startswith(b"/auto"):
                 auto()
                 send("LINE_OFF")
            elif path.startswith(b"/left"):
                send("Left")
                time.sleep(0.1)
                send("Left_Stop")
            elif path.startswith(b"/right"):
                send("Right")
                time.sleep(0.1)
                send("Right_Stop")
            elif path.startswith(b"/stop"):
                # Any *_Stop makes Arduino call stopMotors(); Forward_Stop is sufficient
                send("Forward_Stop")
            elif path.startswith(b"/shelter"):
                 water2(water_back, "Yes")
            elif path.startswith(b"/water"):
                 watering()

            elif path == b"/favicon.ico":
                cl.send(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n")
                cl.close()
                continue

            # Return the tiny UI each time
            cl.send(PAGE)
            cl.close()
            gc.collect()
        except Exception as e:
            # Best-effort cleanup; keep server running
            try:
                cl.close()
            except Exception:
                pass

# ---- Main ---------------------------------------------------------------
try:
    ip = connect_wifi(SSID, PASSWORD)
    print("Connected on:", ip)
    serve()
    

except KeyboardInterrupt:
    pass
except Exception as e:
    print("Fatal error:", e)
    led.value(1)
    


    #if pump(pumping):
     #   print("Watered for", pumping, "Seconds..")
    #else:
     #   print("No Water")
      #  No_Water = True
    
    