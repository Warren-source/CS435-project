from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

#this is where we run the app. To run, type on command line python3 main.py    
