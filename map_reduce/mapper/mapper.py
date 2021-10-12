import requests
from flask import Flask

app = Flask(__name__)

@app.route("/get_data")
def get_data():
    return 'working'


@app.route("/health")
def health():
    return 'Am up !'

if __name__ == "__main__":
    '''
    - read the data from file
    - split the file into bag of words
    - compute number of reducers
    - split the bag of words between this reducers
    '''

    app.run("localhost", 8080)