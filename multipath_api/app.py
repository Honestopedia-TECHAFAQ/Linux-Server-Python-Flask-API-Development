from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

def run_multipath():
    try:
        result = subprocess.run(['multipath', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode != 0:
            return None, result.stderr
        return result.stdout, None
    except Exception as e:
        return None, str(e)

def parse_multipath_output(output):
    parsed_output = {}
    lines = output.splitlines()
    key = ""
    for line in lines:
        if not line.strip():
            continue
        if not line.startswith(' '): 
            key = line.strip()
            parsed_output[key] = []
        else:
            parsed_output[key].append(line.strip())
    return parsed_output

@app.route('/multipath', methods=['GET'])
def multipath():
    output, error = run_multipath()
    if error:
        return jsonify({"error": error}), 500
    parsed_output = parse_multipath_output(output)
    return jsonify(parsed_output)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
