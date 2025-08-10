from flask import Flask, request
from calculator import PyCalc

app = Flask(__name__)
calc = PyCalc()

@app.route('/')
def home():
    return '''
    <h1>PyCalc Web</h1>
    <form action="/calc">
        <input type="text" name="expr" value="2+3*4">
        <button>Calculate</button>
    </form>
    <p>Result: {}</p>
    <h3>History</h3>
    <ul>{}</ul>
    '''.format(
        request.args.get('result', ''),
        ''.join(f'<li>{item}</li>' for item in calc.history[-5:])
    )

@app.route('/calc')
def calculate():
    expr = request.args.get('expr', '')
    result = calc.calculate(expr)
    return home() + f'<script>document.querySelector("input").value = "{expr}";</script>'

if __name__ == '__main__':
    app.run(port=5000)  # Using a different port