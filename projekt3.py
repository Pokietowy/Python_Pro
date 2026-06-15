from flask import Flask
import random

app = Flask("test")

@app.route("/")
def hello_world():
    return '''
        <h1>Witaj świecie!</h1>
        <a href="/random">Wyświetl losowy fakt!</a><br/>
        <a href="/generatorpass">Wygeneruj losowe hasło!</a>
    '''

@app.route("/random")
def random_fact():
    facts_list = ["Test", "Test2"]
    return f'<p>{random.choice(facts_list)}</p>'

@app.route("/generatorpass")
def gen_pass():
    pass_length = 12
    elements = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

app.run(debug=True)
