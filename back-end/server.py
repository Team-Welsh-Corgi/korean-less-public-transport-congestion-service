from flask import Flask, request

app = Flask(__name__)

@app.route('/getCongestion', methods=['GET'])
def getCongestion():
    bus_id = request.args.get('BusID')
    station_id1 = request.args.get('StationID1')
    station_id2 = request.args.get('StationID2')

    # Ư�� �Ķ���� ���� ���� ���
    if not bus_id or not station_id1 or not station_id2:
        return "Error: Missing parameters", 400

    response = predictCongestion(bus_id, station_id1, station_id2)
    return response, 200

# AI �� ���� ���߿� �ۼ��� ����
def predictCongestion(bus, station1, station2):
    pass

if __name__ == '__main__':
    app.run(host='1.254.196.34', port=524, debug=True)
    