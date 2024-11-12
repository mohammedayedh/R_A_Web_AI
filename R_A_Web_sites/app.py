from flask import Flask, render_template, request, session
import google.generativeai as genai
import random

app = Flask(__name__)
app.secret_key = str(random.randint(1000000, 9999999)) 

def commands_go(command):
    try:
        api_key = "AIzaSyDKLz26KhfzsjnM0eVe8WWq-zmqBSzzy0k"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        
        response = model.generate_content(command)
        return response.text
    except Exception as e:
        return f"There is an Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'messages' not in session:
        session['messages'] = [{'type': 'ai', 'content': "مرحبا بما يمكنني مساعدتك اليوم  . . ."}]
    
    if request.method == 'POST':
        user_input = request.form.get('command')
        
        session['messages'].append({'type': 'user', 'content': user_input})
        
        
        result = commands_go(user_input)
        
        session['messages'].append({'type': 'ai', 'content': result})

    return render_template('index.html', messages=session['messages'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
