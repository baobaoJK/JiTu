from services import upload_bp, pic_bp, system_bp, folder_bp

from utils import app, load_config

# 注册 Blueprint
app.register_blueprint(upload_bp)
app.register_blueprint(pic_bp)
app.register_blueprint(system_bp)
app.register_blueprint(folder_bp)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    config = load_config()
    app.run(host=config["server"]["host"], port=config["server"]["port"], debug=config["server"]["debug"],
            ssl_context=('keys/cert.pem', 'keys/key.pem'))
