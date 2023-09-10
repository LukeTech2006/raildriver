import socket, time, json
print("RailDriver64 Listener\n")

with socket.create_connection(("Lukas-PC", 22223)) as sock:
    while True:
        message = json.loads(sock.recv(65535).decode("utf-8"))

        keysToSwallow = []
        for key in message.keys():
            for forbiddenKey in ["SpeedometerKPH", "MainReservoirPressureBAR", "TrainBrakeCylinderPressureBAR", "BrakePipePressureBAR", "RPM", "RPMDelta", "VirtualThrottle", "TractiveEffort", "Oil", "PZBWACH", "TrainBrakeControl"]:
                if key == forbiddenKey: keysToSwallow.append(key)
        for key in keysToSwallow: del(message[key])

        if message: print(f'[{time.asctime()}] Messages: {message}')