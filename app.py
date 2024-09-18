from flask import Flask, render_template, request
import pandas as pd
import pickle
import recommender
app = Flask(__name__)


# Load login credentials from file into a dictionary
def load_login_credentials():
    credentials = {}
    with open('login_credentials.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            credentials[username] = password
    return credentials


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login_credentials = load_login_credentials()
        # Check if the credentials match
        if username in login_credentials and login_credentials[username] == password:
            return render_template('index.html', username=username)
        else:
            return 'Invalid username or password'

    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    song_results = []
    song_name=""
    if request.method == 'POST':
        # Get the user input song name
        song_name = request.form['song_name']

        with open('model.pkl', 'rb') as file:
            # Load the data from the pickle file
            model = pickle.load(file)

        with open('dict1.pkl', 'rb') as file:
            # Load the data from the pickle file
            dict1 = pickle.load(file)

        with open('dict2.pkl', 'rb') as file:
            # Load the data from the pickle file
            dict2 = pickle.load(file)

        # Determine which search was selected
        if 'collab_search' in request.form:
            # Collaborative search
            song_results = model.make_recommendation(song_name, 10)
        elif 'similar_search' in request.form:
            # Similar search
            if song_name in dict2:
                label =dict2[song_name];
                song_results=dict1[label]


    # Render the template with the search results and song name
    return render_template('index.html', song_results=song_results, song_name=song_name)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('login_credentials.txt', 'a') as file:
            file.write(username + ',' + password + '\n')

        return render_template('login.html')


    return render_template('signup.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        username=""
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
