import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello, {name}!")

@app.command()
def goodbye(name: str):
    if formal: 
        print(f"Goodbye, Ms. {name}. have a good day!")
    else:
        print(f"bye {name}!")
    
if __name__ == "__main__":
    app()