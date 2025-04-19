from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    transacoes = db.relationship('Transacao', backref='user', lazy=True)
    lembretes = db.relationship('Lembrete', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)
    metas = db.relationship('Meta', backref='user', lazy=True)

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'

    def __repr__(self):
        return f'<Transacao {self.categoria} - {self.mes}/{self.ano} - {self.tipo}>'

class Lembrete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    dia = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Lembrete {self.categoria} - {self.mes}>'

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_conquista = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Badge {self.nome}>'

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    valor = db.Column(db.Float, nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())