from flask import Flask, render_template, request, redirect, url_for, session
from db import cursor, db  # supondo que db.py exporte a conexão e o cursor
app = Flask(__name__)
app.secret_key = "aura"  # Pode ser qualquer string segura


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

# Rota Gerar Resumo
@app.route("/geraresumo", methods=["GET", "POST"])
def geraresumo():
    # Aqui você pega os dados armazenados na sessão (ou usa valores padrão)
    pdf_url = session.get("uploaded_pdf", "/static/exemplo.pdf")  # PDF padrão
    resumo = session.get("resumo", "Aqui vai o resumo gerado automaticamente.")
    pontos_chave = session.get("pontos_chave", [
        "Ponto chave 1",
        "Ponto chave 2",
        "Ponto chave 3"
    ])
    
    # Renderiza o template passando os dados
    return render_template("geraresumo.html", pdf_url=pdf_url, resumo=resumo, pontos_chave=pontos_chave)

    # Rota para página de áudio
@app.route("/audio", methods=["GET"])
def audio():
    # PDF e áudio podem ser passados via sessão ou valores padrão
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    audio_url = session.get("audio_url", "/static/audio/exemplo.mp3")  # exemplo de áudio
    return render_template("audio.html", pdf_url=pdf_url, audio_url=audio_url)

@app.route('/selecionar', methods=['GET', 'POST'])
def selecionar_resumo():
    # Pegando valores da sessão ou definindo valores padrão
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    resumo = session.get("resumo", "Aqui vai o resumo gerado automaticamente.")
    pontos_chave = session.get("pontos_chave", ["Ponto chave 1", "Ponto chave 2", "Ponto chave 3"])

    if request.method == 'POST':
        # processar algo
        return "Resumo processado!"

    return render_template('selecionar.html', pdf_url=pdf_url, resumo=resumo, pontos_chave=pontos_chave)


if __name__ == "__main__":
    app.run(debug=True)
