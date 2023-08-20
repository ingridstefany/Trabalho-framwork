from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ingrid:1234@localhost:3306/trabalho'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))

    def __init__(self, nome, email, senha, end):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.end = end

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id



class Venda(db.Model):
    __tablename__ = "ven"
    id = db.Column('ven_id', db.Integer, primary_key=True)
    nome = db.Column('ven_nome', db.String(256))
    qtd = db.Column('ven_qtd', db.Integer)
    preco = db.Column('ven_preco', db.Float)
    total = db.Column('ven_total', db.Float)
    data = db.Column('ven_data', db.date)
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, qtd, preco, total, data, usu_id):
        self.nome = nome
        self.qtd = qtd
        self.preco = preco
        self.total = total
        self.data = data
        self.usu_id = usu_id

    class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column('compra_id', db.Integer, primary_key=True)
    nome = db.Column('compra_nome', db.String(256))
    desc = db.Column('compra_desc', db.String(256))
    qtd = db.Column('compra_qtd', db.Integer)
    preco = db.Column('compra_preco', db.Float)
    ven = db.Column('compra_ven', db.string(256))
    total = db.Column('compra_total', db.Float)
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, ven, total, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.ven_id = ven
        self.total_id = total
        self.usu_id = usu_id





@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar")
def criarusuario():
    usuario = Usuario(request.form.get('user'), request.form.get('email'),request.form.get('passwd'),request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>")
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        usuario.end = request.form.get('end')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('eusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar")
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncios/compra")
def compra():
    print("anuncio comprado")
    return ""


@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar")
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relvendas.html', vendas = Venda.query.all(), categorias = Categoria.query.all(), titulo="venda")

@app.route("/vendas/criar")
def criarvenda():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('total'),request.form.get('data'),request.form.get('uso'))
    db.session.add(venda)
    db.session.commit()
    return redirect(url_for('venda'))

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html', compras = Venda.query.all(), categorias = Categoria.query.all(), titulo="compra")

@app.route("/compras/criar")
def criarcompra():
    anuncio = Compra(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('ven'),request.form.get('total'),request.form.get('uso'))
    db.session.add(compra)
    db.session.commit()
    return redirect(url_for('compra'))

if __name__ == '__main__':
    print("trabalho")
    db.create_all()
    app.run()

    db.create_all()
    app.run()
