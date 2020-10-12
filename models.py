from gerenciador_matriculas import db
from datetime import datetime
from slugify import slugify


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(35), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.Boolean(35), default=False)
    dataNascimento = db.Column(db.DateTime, nullable=False)

    matriculas = db.relationship('Matricula', backref='aluno', lazy=True)

    def __repr__(self):
        return f"Aluno('{self.nome}', '{self.cpf}', '{self.email}', '{self.status}', '{self.dataNascimento}')"


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(35), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(35), unique=True, nullable=False)
    sequencia = db.Column(db.Integer, nullable=False)
    precoVenda = db.Column(db.Float)
    dataCadastro = db.Column(db.DateTime, default=datetime.utcnow)

    matriculas = db.relationship('Matricula', backref='curso', lazy=True)

    def __repr__(self):
        return f"Curso('{self.nome}', '{self.status}', '{self.slug}', '{self.sequencia}', '{self.dataCadastro}')"

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


db.event.listen(Curso.nome, 'set', Curso.slugify, retval=False)


class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default='bloqueado')
    ano = db.Column(db.String(5), nullable=False)
    dataCadastro = db.Column(db.DateTime, default=datetime.utcnow())

    alunoId = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    def __repr__(self):
        return f"Matricula('{self.nome}', '{self.status}', '{self.slug}', '{self.sequencia}', '{self.dataCadastro}')"