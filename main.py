from flask import Flask, render_template, request


app = Flask(__name__)
df = pd.read_csv('assets/vector.csv')


@app.route('/', method=['GET', 'POST'])
def hello():
    if
    char = request.args.get('char')

    res = []
    if char is not None:
        pass

    return render_template('index.html', res=res)


if __name__ == "__main__":
    app.run(debug=True)
