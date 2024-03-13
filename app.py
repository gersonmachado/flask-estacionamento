from flask import Flask, jsonify, render_template, request 
from flask_sqlalchemy import SQLAlchemy
import datetime


# Configurações básicas do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 'TipoDoBanco://SuperUser:LocalDoDB/NomeDoDB' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estacionamento.db' # URI do banco de dados

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

#Criar model
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    placa = db.Column(db.String(11), unique=True, nullable=False)
    dt_entrada = db.Column(db.DateTime, nullable=False)
    dt_saida = db.Column(db.DateTime, nullable=True)

    def __init__(self, nome, placa, dt_entrada):
        self.nome = nome
        self.placa = placa
        self.dt_entrada = dt_entrada

@app.route("/")
def hello_world():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def formulario_cadastro():
    return render_template('cadastro.html')

# Rota para adicionar uma nova pessoa ao banco de dados
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    # nome = data['nome']
    # placa = data['placa']
    nome = request.form['nome']
    placa = request.form['placa']
    novo_cadastro = Pessoa(nome=nome, placa=placa, dt_entrada=datetime.datetime.now())

    try:
        db.session.add(novo_cadastro)
        db.session.commit()
        return jsonify({'message': 'Pessoa adicionada com sucesso!'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao adicionar pessoa'}), 500



# Rodar o server
if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no banco de dados, se não existirem
        db.create_all()
    app.run(port=8000)