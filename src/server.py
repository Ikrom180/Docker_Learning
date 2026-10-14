from flask import Flask

# Equivalent to: const app = express();
app = Flask(__name__)

# Equivalent to: app.get('/', (req, res) => { ... });
@app.route('/')
def home():
    # Equivalent to: res.send(...)
    return "Welcome to my awesome app!"

# Equivalent to: app.listen(3000, ...)
if __name__ == '__main__':
    print("app listening on port 3000")
    app.run(host='0.0.0.0', port=3000)