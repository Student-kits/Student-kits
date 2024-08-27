from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Flask!"
@app.post('/costumber/topic') 
def costumber():
    r=[{"pwd"}pwd :  ]
    
if __name__ == '__main__':
    app.run(debug=True)