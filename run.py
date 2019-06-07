from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))

#$ gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:8000 run:app
