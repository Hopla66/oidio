import websocket

def on_message(wsapp, message):
    print(message)

wsapp = websocket.WebSocketApp("ws://localhost:8000/ws", on_message = on_message)
wsapp.run_forever()