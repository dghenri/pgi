from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Base, Ativo, Peca, Chamado

app = Flask(__name__)

# -------- Conexão com SQLite --------
engine = create_engine("postgresql://dbit_1rq1_user:w6xBxZorJABAPzs2J5YhhFRAmsSsDtlS@dpg-d2m935ruibrs7380fh90-a.virginia-postgres.render.com/dbit_1rq1", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(bind=engine)

#---------------------------------------------Cria rotas da aplicação---------------------------------------------
# ---------------- FRONT ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- ATIVOS ----------------
@app.route("/api/ativos", methods=["GET"])
def listar_ativos():
    ativos = session.query(Ativo).all()
    return jsonify([{
        "id": a.id,
        "tipo": a.tipo,
        "patrimonio": a.patrimonio,
        "marca": a.marca,
        "serial": a.serial,
        "disco": a.disco,
        "hostname": a.hostname,
        "nome": a.nome,
        "login": a.login,
        "setor": a.setor,
        "local": a.local,
        "os": a.os,
        "status": a.status
    } for a in ativos])


@app.route("/api/ativos", methods=["POST"])
def adicionar_ativo():
    data = request.json
    novo = Ativo(
        tipo=data.get("tipo", "Notebook"),
        patrimonio=data.get("patrimonio"),
        marca=data.get("marca"),
        serial=data.get("serial"),
        disco=data.get("disco"),
        hostname=data.get("hostname"),
        nome=data.get("nome"),
        login=data.get("login"),
        setor=data.get("setor"),
        local=data.get("local"),
        os=data.get("os"),
        status=data.get("status", "Em uso"),
    )
    session.add(novo)
    session.commit()
    return jsonify({"message": "Ativo adicionado"})


@app.route("/api/ativos/<int:id>", methods=["DELETE"])
def deletar_ativo(id):
    ativo = session.query(Ativo).filter_by(id=id).first()
    if not ativo:
        return jsonify({"error": "Ativo não encontrado"}), 404
    session.delete(ativo)
    session.commit()
    return jsonify({"message": "Ativo deletado"})


# ---------------- PEÇAS ----------------
@app.route("/api/pecas", methods=["GET"])
def listar_pecas():
    pecas = session.query(Peca).all()
    return jsonify([{
        "id": p.id,
        "nome": p.nome,
        "categoria": p.categoria,
        "quantidade": p.quantidade,
        "observacao": p.observacao
    } for p in pecas])


@app.route("/api/pecas", methods=["POST"])
def adicionar_peca():
    data = request.json
    nova = Peca(
        nome=data["nome"],
        categoria=data["categoria"],
        quantidade=data["quantidade"],
        observacao=data.get("observacao", "")
    )
    session.add(nova)
    session.commit()
    return jsonify({"message": "Peça adicionada"})


# ---------------- CHAMADOS ----------------
@app.route("/api/chamados", methods=["GET"])
def listar_chamados():
    chamados = session.query(Chamado).all()
    return jsonify([{
        "id": c.id,
        "nome": c.nome,
        "numero": c.numero,
        "assunto": c.assunto,
        "tipo": c.tipo,
        "tecnico": c.tecnico,
        "grupo": c.grupo,
        "data": c.data.isoformat() if c.data else None
    } for c in chamados])


@app.route("/api/chamados", methods=["POST"])
def adicionar_chamado():
    data = request.json
    novo = Chamado(
        nome=data["nome"],
        numero=data["numero"],
        assunto=data["assunto"],
        tipo=data.get("tipo", "Remoto"),
        tecnico=data.get("tecnico"),
        grupo=data.get("grupo"),
        data=date.fromisoformat(data["data"]) if data.get("data") else date.today()
    )
    session.add(novo)
    session.commit()
    return jsonify({"message": "Chamado adicionado"})


if __name__ == "__main__":
    app.run(debug=True)
