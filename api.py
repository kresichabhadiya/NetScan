from flask import Flask, request, jsonify
from flask_cors import CORS
from netscan import scan_network, parse_network

app = Flask(__name__)
CORS(app)   # allows browser to call this API

@app.route('/scan', methods=['POST'])
def scan():
    data    = request.get_json()
    target  = data.get('network', '')
    try:
        network = parse_network(target if target else None)
        online  = scan_network(network)
        online.sort(key=lambda x: tuple(map(int, x.split('.'))))
        return jsonify({
            'network': str(network),
            'total':   network.num_addresses - 2,
            'online':  online,
            'count':   len(online)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)