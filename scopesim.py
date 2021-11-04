# Python 3 server example
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import time

import random
import numpy as np

hostName = "localhost"
serverPort = 5022
t_wall = 0.0
bl = np.sin(2*np.pi*2.0e3*t_wall)

class MyServer(SimpleHTTPRequestHandler):
    def __init__(self):
        super().__init__(self)
        self.shutter_open = False
    def do_GET(self):
        bl = int(10.0*np.sin(2*np.pi*2.0e3*t_wall))
        t_wall = t_wall + 1.0/0.8e-7
        if self.path.find('SHUT') >= 0 :
            if self.path.find('OPEN') >= 0 :
                self.shutter_open = True
            else :
                self.shutter_open = False
        if self.path.find('curve?') >= 0 :
            self.wav = []
            datfile = 'raw_bkg.dat'
            if self.shutter_open :
                datfile = 'raw_sig.dat'      
            with open(datfile) as ff:
                for line in ff: # read rest of lines
                    self.wav.append(int(line))
            sc = random.randint(0,2)
            msg = ''
            for sample in self.wav:
                msg = msg + str(int(sample + sc + bl))
                msg = msg + ','
            msg = msg[:-1] + '\n'
            print(msg)
            self.send_response(200,message=None)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(msg, "utf-8"))
        if self.path.find('wfmpre?') >= 0 :
            msg = '1;8;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";8.0E-4;0.0E0;-5.4E1;"V"\n'
            self.send_response(200,message=None)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(msg, "utf-8"))

        time.sleep(1.0)

if __name__ == "__main__":        
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


