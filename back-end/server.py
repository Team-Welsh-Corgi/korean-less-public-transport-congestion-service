# -*- coding: Windows-1252 -*-
from flask import Flask, request

app = Flask(__name__)

@app.route('/getCongestion', methods=['GET'])
def getCongestion():
    bus_id = request.args.get('BusID')
    station_id1 = request.args.get('StationID1')
    station_id2 = request.args.get('StationID2')

    # Æ¯Á¤ ÆÄ¶ó¹ÌÅÍ °ªÀÌ ¾ø´Â °æ¿ì
    if not bus_id or not station_id1 or not station_id2:
        return "Error: Missing parameters"

    response = predictCongestion(bus_id, station_id1, station_id2)
    str1 = str(bus_id) + " " + str(station_id1) + " "  + str(station_id2)
    return str1
    #return response

# AI ¾µ °÷ÀÓ ³ªÁß¿¡ ÀÛ¼ºÇÒ ¿¹Á¤
def predictCongestion(bus, station1, station2):
    pass

if __name__ == '__main__':
    app.run(host='localhost', port=524, debug=True)
    