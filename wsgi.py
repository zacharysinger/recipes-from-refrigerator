from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port='3600', host='127.0.0.1', debug=True)
    # app.run(host='0.0.0.0', debug=True)
