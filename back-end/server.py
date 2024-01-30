from flask import Flask, request

app = Flask(__name__)

@app.route('/getCongestion', methods=['GET'])
def getCongestion():
    bus_id = request.args.get('BusID')
    station_id1 = request.args.get('StationID1')
    station_id2 = request.args.get('StationID2')

    # 특정 파라미터 값이 없는 경우
    if not bus_id or not station_id1 or not station_id2:
        return "Error: Missing parameters", 400

    response = predictCongestion(bus_id, station_id1, station_id2)
    return response, 200

# AI 쓸 곳임 나중에 작성할 예정
def predictCongestion(bus, station1, station2):
    pass

if __name__ == '__main__':
    app.run(host='1.254.196.34', port=524, debug=True)
    