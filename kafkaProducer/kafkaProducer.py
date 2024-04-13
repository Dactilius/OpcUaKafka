from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        json_data = request.json
        print("Received JSON data:")
        print(json.dumps(json_data, indent=4))
        return "Data received successfully", 200
    except Exception as e:
        print("Error processing received data:", e)
        return "Error processing data", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
