from api.app import app


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, host='0.0.0.0')  # For external traffic