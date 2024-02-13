from flask import Flask, jsonify
from flask_cors import CORS
#app instance :]
app = Flask(__name__)
CORS(app)

# /api/home
@app.route("/api/home", methods= ['GET'])
def return_home():
    return jsonify({
        'message': "im spongebob",
        'list': ['Hidden Gem #1', 'Hidden Gem #2', 'Hidden Gem #3']
        
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
    
    
#Server run command is python3 server.py 
# http://localhost:8080/api/home