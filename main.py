import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from models import Base, Ativo, Peca, Chamado

app = Flask(__name__)
CORS(app)

# ------------------------------------------ Conexão com Banco de dados ------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definido. Defina a variável de ambiente DATABASE_URL antes de iniciar a aplicação.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
engine = create_engine(DATABASE_URL, echo=True)
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
        "tipoEquip": a.tipoEquip,
        "patrimonio": a.patrimonio,
        "marca": a.marca,
        "serial": a.serial,
        "disco": a.disco,
        "hostname": a.hostname,
        "nome": a.nome,
        "login": a.login,
        "setor": a.setor,
        "local": a.local,
        "sistemaOperacional": a.sistemaOperacional,
        "status": a.status
    } for a in ativos])

@app.route("/api/ativos", methods=["POST"])
def adicionar_ativo():
    data = request.json
    novo = Ativo(
        tipoEquip=data.get("tipoEquip", "Notebook"),
        patrimonio=data.get("patrimonio"),
        marca=data.get("marca"),
        serial=data.get("serial"),
        disco=data.get("disco"),
        hostname=data.get("hostname"),
        nome=data.get("nome"),
        login=data.get("login"),
        setor=data.get("setor"),
        local=data.get("local"),
        sistemaOperacional=data.get("sistemaOperacional"),
        status=data.get("status", "Em uso"),
    )
    session.add(novo)
    session.commit()
    return jsonify({"message": "Ativo adicionado"})

@app.route("/api/ativos/<int:id>", methods=["PUT"])
def atualizar_ativo(id):
    try:
        data = request.json
        ativo = session.query(Ativo).filter_by(id=id).first()
        if not ativo:
            return jsonify({"error": "Ativo não encontrado"}), 404
        
        ativo.tipoEquip = data.get("tipoEquip", ativo.tipoEquip)
        ativo.patrimonio = data.get("patrimonio", ativo.patrimonio)
        ativo.marca = data.get("marca", ativo.marca)
        ativo.serial = data.get("serial", ativo.serial)
        ativo.disco = data.get("disco", ativo.disco)
        ativo.hostname = data.get("hostname", ativo.hostname)
        ativo.nome = data.get("nome", ativo.nome)
        ativo.login = data.get("login", ativo.login)
        ativo.setor = data.get("setor", ativo.setor)
        ativo.local = data.get("local", ativo.local)
        ativo.sistemaOperacional = data.get("sistemaOperacional", ativo.sistemaOperacional)
        ativo.status = data.get("status", ativo.status)
        
        session.commit()
        return jsonify({"message": "Ativo atualizado com sucesso"}), 200
    
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

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

@app.route("/api/pecas/<int:id>", methods=["PUT"])
def atualizar_peca(id):
    try:
        data = request.json
        peca = session.query(Peca).filter_by(id=id).first()
        if not peca:
            return jsonify({"error": "Peça não encontrada"}), 404
        
        peca.nome = data.get("nome", peca.nome)
        peca.categoria = data.get("categoria", peca.categoria)
        peca.quantidade = data.get("quantidade", peca.quantidade)
        peca.observacao = data.get("observacao", peca.observacao)
        
        session.commit()
        return jsonify({"message": "Peça atualizada com sucesso"}), 200
    
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
    
@app.route("/api/pecas/<int:id>", methods=["DELETE"])
def deletar_peca(id):
    peca = session.query(Peca).filter_by(id=id).first()
    if not peca:
        return jsonify({"error": "Peça não encontrada"}), 404
    session.delete(peca)
    session.commit()
    return jsonify({"message": "Peça deletada"})


# ---------------- CHAMADOS ----------------
@app.route("/api/chamados", methods=["GET"])
def listar_chamados():
    chamados = session.query(Chamado).all()
    return jsonify([{
        "id": c.id,
        "nome": c.nome,
        "numero": c.numero,
        "assunto": c.assunto,
        "tipoChamado": c.tipoChamado,
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
        tipoChamado=data.get("tipoChamado", "Remoto"),
        tecnico=data.get("tecnico"),
        grupo=data.get("grupo"),
        data=date.fromisoformat(data["data"]) if data.get("data") else date.today()
    )
    session.add(novo)
    session.commit()
    return jsonify({"message": "Chamado adicionado"})

#---------------------------------------------Inicia a aplicação---------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

