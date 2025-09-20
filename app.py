from flask import Flask, render_template, request, redirect, url_for
from db import cursor, db  # supondo que db.py exporte a conexão e o cursor

app = Flask(__name__)

# Rota da landing page
@app.route("/")
def index():
    return render_template("index.html")

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND senha=%s",
            (email, senha)
        )
        usuario = cursor.fetchone()

        if usuario:
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)

# Rota de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            # Verifica se o email já existe
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                erro = "Esse usuário já existe"  # mesma msg do login
            else:
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                    (nome, email, senha)
                )
                db.commit()
                return redirect(url_for("index"))
        except Exception as e:
            erro = "Erro ao cadastrar usuário: " + str(e)

    return render_template("cadastro.html", erro=erro)


if __name__ == "__main__":
    app.run(debug=True)
