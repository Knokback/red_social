from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "123"

# Banco simples (memória)
alunos = []
presencas = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        if user:
            session["user"] = user
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    resposta_ia = ""

    if request.method == "POST":

        # Adicionar aluno
        if "nome" in request.form:
            nome = request.form["nome"]
            if nome and nome not in alunos:
                alunos.append(nome)
                presencas[nome] = "Faltou"

        # Marcar presença
        if "presenca" in request.form:
            nome = request.form["presenca"]
            presencas[nome] = "Presente"

        # Assistente IA melhorado
        if "pergunta" in request.form:
            pergunta = request.form["pergunta"].lower()

            if "quantos alunos" in pergunta:
                resposta_ia = f"Tem {len(alunos)} alunos cadastrados."

            elif "quem faltou" in pergunta:
                faltaram = [a for a, p in presencas.items() if p == "Faltou"]
                resposta_ia = "Faltaram: " + ", ".join(faltaram) if faltaram else "Todos presentes."

            elif "quem está presente" in pergunta:
                presentes = [a for a, p in presencas.items() if p == "Presente"]
                resposta_ia = "Presentes: " + ", ".join(presentes) if presentes else "Ninguém presente."

            elif "presença" in pergunta:
                resposta_ia = str(presencas)

            else:
                resposta_ia = "Posso responder sobre alunos e presença."

    # Dashboard (estatísticas)
    total = len(alunos)
    presentes = list(presencas.values()).count("Presente")
    faltas = total - presentes

    return render_template(
        "dashboard.html",
        alunos=alunos,
        presencas=presencas,
        resposta_ia=resposta_ia,
        total=total,
        presentes=presentes,
        faltas=faltas
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
