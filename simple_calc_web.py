from flask import Flask, request
from calculator import PyCalc

app = Flask(__name__)
calc = PyCalc()

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>PyCalc Pro</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
            form { margin-bottom: 20px; }
            input[type="text"] { width: 70%; padding: 8px; font-size: 16px; }
            button { padding: 8px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; padding: 5px; background: #f0f0f0; }
        </style>
    </head>
    <body>
        <h1>PyCalc Web Calculator</h1>
        <form action="/calc">
            <input type="text" name="expr" placeholder="2+3*4" value="{}">
            <button>Calculate</button>
        </form>
        {}
        <h3>History</h3>
        <ul>{}</ul>
    </body>
    </html>
    '''.format(
        request.args.get('expr', ''),
        f'<p>Result: <strong>{request.args.get("result", "")}</strong></p>' if request.args.get('result') else '',
        ''.join(f'<li>{item}</li>' for item in calc.history[-5:])
    )

@app.route('/calc')
def calculate():
    expr = request.args.get('expr', '')
    result = calc.calculate(expr)
    return home() + f'<script>document.querySelector("input").value = "{expr}";</script>'

if __name__ == '__main__':
    app.run(port=5000)

    