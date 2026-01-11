from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting Server...")
    app.run(debug=True)