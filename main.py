import requests
from flask import *
import os
import openai

data = None
image_url = None
prompt = None
content = None

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
api_key = os.environ.get('AI_API_KEY')
openai.api_key = os.environ.get('gptkey')
@app.route('/')
def home():
    return render_template('index.html', data=data, image=image_url, prompt=prompt, content=content)

@app.route('/ask', methods = ['POST', 'GET'])
def ask():
    global content, data
    if request.method == 'POST':
        content = request.form.get('content')

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"{content}"
        }]
    )

    data = completion.choices[0].message['content']
    return redirect(url_for('home'))


@app.route('/image', methods=['POST', 'GET'])
def image():
    global prompt, image_url
    if request.method == 'POST':
        prompt = request.form.get('prompt')

    url = "https://openai80.p.rapidapi.com/images/generations"

    payload = {
        "prompt": f"{prompt}",
        "n": 2,
        "size": "1024x1024"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "openai80.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    image_url = response.json()['data'][0]['url']
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)




