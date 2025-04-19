from flask import render_template, request, redirect, url_for, flash, send_file
from app import app, db
from app.models import User, Transacao, Lembrete, Badge, Meta
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from datetime import datetime
import pdfkit
import io
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Função para conceder badges
def conceder_badge(user_id, nome, descricao):
    badge_existente = Badge.query.filter_by(user_id=user_id, nome=nome).first()
    if not badge_existente:
        badge = Badge(user_id=user_id, nome=nome, descricao=descricao)
        db.session.add(badge)
        db.session.commit()
        flash(f'Parabéns! Você conquistou o badge "{nome}"! 🏆', 'success')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        senha = request.form['senha']
        logging.debug(f"Tentativa de login com e-mail: {email}")
        
        user = User.query.filter_by(email=email).first()
        if user:
            logging.debug(f"Usuário encontrado: {user.email}, hash da senha: {user.senha}")
            if user.check_password(senha):
                logging.debug("Senha válida! Logando usuário...")
                login_user(user)
                flash('Bem-vindo de volta ao Finanças99! 🎉', 'success')
                return redirect(url_for('dashboard'))
            else:
                logging.debug("Senha inválida!")
                flash('E-mail ou senha inválidos. Tente novamente! 😕', 'error')
        else:
            logging.debug(f"Usuário com e-mail {email} não encontrado!")
            flash('E-mail ou senha inválidos. Tente novamente! 😕', 'error')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email'].strip()
        senha = request.form['senha']
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está cadastrado. Tente outro ou faça login! 😕', 'error')
            return redirect(url_for('cadastro'))
        
        try:
            user = User(nome=nome, email=email)
            user.set_password(senha)
            db.session.add(user)
            db.session.commit()
            logging.debug(f"Usuário {email} cadastrado com sucesso!")
            flash('Cadastro concluído com sucesso! Vamos organizar suas finanças? 💸', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao cadastrar usuário: {str(e)}")
            flash('Ocorreu um erro ao realizar o cadastro. Tente novamente mais tarde! 😓', 'error')
            return redirect(url_for('cadastro'))
    return render_template('cadastro.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    # Filtros
    ano_filtro = request.form.get('ano', '2025')
    tipo_filtro = request.form.get('tipo', 'todos')
    
    # Buscar transações do usuário atual
    query = Transacao.query.filter_by(user_id=current_user.id)
    if ano_filtro:
        query = query.filter(Transacao.ano == int(ano_filtro))
    if tipo_filtro != 'todos':
        query = query.filter(Transacao.tipo == tipo_filtro)
    
    transacoes = query.all()
    categorias = db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()
    categorias = [cat[0] for cat in categorias]
    
    # Inicializar dicionários para os totais
    total_despesas = {mes: 0 for mes in meses}
    total_receitas = {mes: 0 for mes in meses}
    
    # Calcular totais por mês
    for transacao in transacoes:
        if transacao.tipo == 'despesa':
            total_despesas[transacao.mes] += float(transacao.valor)
        elif transacao.tipo == 'receita':
            total_receitas[transacao.mes] += float(transacao.valor)
    
    # Arredondar os valores
    total_despesas = {mes: round(valor, 2) for mes, valor in total_despesas.items()}
    total_receitas = {mes: round(valor, 2) for mes, valor in total_receitas.items()}
    
    # Calcular total livre
    total_livre = {mes: round(total_receitas[mes] - total_despesas[mes], 2) for mes in meses}
    
    # Buscar lembretes do mês atual
    hoje = datetime.now()
    mes_atual = meses[hoje.month - 1]
    dia_atual = hoje.day
    lembretes = Lembrete.query.filter_by(user_id=current_user.id, mes=mes_atual, dia=dia_atual).all()
    
    # Verificar badges
    if total_livre[mes_atual] > 0:
        conceder_badge(current_user.id, "Economizador do Mês", "Você terminou o mês com saldo positivo!")
    if len(categorias) >= 5:
        conceder_badge(current_user.id, "Mestre das Categorias", "Você criou 5 ou mais categorias!")
    if Lembrete.query.filter_by(user_id=current_user.id).count() >= 3:
        conceder_badge(current_user.id, "Planejador Nato", "Você configurou 3 ou mais lembretes!")
    
    badges = Badge.query.filter_by(user_id=current_user.id).all()
    
    # Verificar metas
    metas = Meta.query.filter_by(user_id=current_user.id).all()
    alertas_metas = []
    for meta in metas:
        if meta.mes == mes_atual and meta.ano == int(ano_filtro):
            if meta.tipo == 'despesa' and total_despesas[mes_atual] > meta.valor:
                alertas_metas.append(f'⚠️ Atenção! Suas despesas em {mes_atual} excederam a meta de R$ {meta.valor:.2f}')
            elif meta.tipo == 'receita' and total_receitas[mes_atual] < meta.valor:
                alertas_metas.append(f'⚠️ Atenção! Suas receitas em {mes_atual} estão abaixo da meta de R$ {meta.valor:.2f}')
    
    # Verificar alertas de gastos excessivos
    media_despesas = sum(total_despesas.values()) / len(total_despesas)
    if total_despesas[mes_atual] > media_despesas * 1.5:
        alertas_metas.append(f'⚠️ Atenção! Seus gastos em {mes_atual} estão 50% acima da média mensal')
    
    return render_template('dashboard.html', transacoes=transacoes, meses=meses, categorias=categorias, 
                          total_despesas=total_despesas, total_receitas=total_receitas, total_livre=total_livre, 
                          lembretes=lembretes, badges=badges, ano_filtro=ano_filtro, tipo_filtro=tipo_filtro, 
                          alertas=alertas_metas)

@app.route('/adicionar_transacao', methods=['GET', 'POST'])
@login_required
def adicionar_transacao():
    if request.method == 'POST':
        categoria = request.form['categoria']
        valor = float(request.form['valor'])
        mes = request.form['mes']
        ano = int(request.form['ano'])
        tipo = request.form['tipo']
        transacao = Transacao(user_id=current_user.id, categoria=categoria, valor=valor, mes=mes, ano=ano, tipo=tipo)
        db.session.add(transacao)
        db.session.commit()
        flash('Transação adicionada com sucesso! 💰', 'success')
        return redirect(url_for('dashboard'))
    
    categorias = db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()
    categorias = [cat[0] for cat in categorias]
    
    if not categorias:
        flash('Você precisa criar pelo menos uma categoria antes de adicionar uma transação! 🏷️', 'error')
        return redirect(url_for('gerenciar_categorias'))
    
    return render_template('adicionar_transacao.html', categorias=categorias)

@app.route('/gerenciar_categorias', methods=['GET', 'POST'])
@login_required
def gerenciar_categorias():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            nova_categoria = request.form['nova_categoria']
            if nova_categoria and nova_categoria not in [cat[0] for cat in db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()]:
                transacao = Transacao(user_id=current_user.id, categoria=nova_categoria, valor=0, mes='Janeiro', ano=2025, tipo='despesa')
                db.session.add(transacao)
                db.session.commit()
                flash('Categoria adicionada com sucesso! 🏷️', 'success')
            else:
                flash('Categoria já existe ou é inválida! 😕', 'error')
        elif action == 'edit':
            antiga_categoria = request.form['antiga_categoria']
            nova_categoria = request.form['nova_categoria']
            transacoes = Transacao.query.filter_by(user_id=current_user.id, categoria=antiga_categoria).all()
            for transacao in transacoes:
                transacao.categoria = nova_categoria
            db.session.commit()
            flash('Categoria editada com sucesso! ✏️', 'success')
        elif action == 'delete':
            categoria = request.form['categoria']
            Transacao.query.filter_by(user_id=current_user.id, categoria=categoria).delete()
            db.session.commit()
            flash('Categoria excluída com sucesso! 🗑️', 'success')
        return redirect(url_for('gerenciar_categorias'))

    categorias = db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()
    categorias = [cat[0] for cat in categorias]
    return render_template('gerenciar_categorias.html', categorias=categorias)

@app.route('/lembretes', methods=['GET', 'POST'])
@login_required
def lembretes():
    if request.method == 'POST':
        categoria = request.form['categoria']
        valor = float(request.form['valor'])
        dia = int(request.form['dia'])
        mes = request.form['mes']
        mensagem = request.form['mensagem']
        
        lembrete = Lembrete(user_id=current_user.id, categoria=categoria, valor=valor, dia=dia, mes=mes, mensagem=mensagem)
        db.session.add(lembrete)
        db.session.commit()
        flash('Lembrete criado com sucesso! ⏰', 'success')
        return redirect(url_for('lembretes'))
    
    categorias = db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()
    categorias = [cat[0] for cat in categorias]
    lembretes = Lembrete.query.filter_by(user_id=current_user.id).all()
    return render_template('lembretes.html', categorias=categorias, lembretes=lembretes)

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        
        existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_user:
            flash('Este e-mail já está cadastrado. Tente outro! 😕', 'error')
            return redirect(url_for('perfil'))
        
        current_user.nome = nome
        current_user.email = email
        db.session.commit()
        flash('Perfil atualizado com sucesso! 😊', 'success')
        return redirect(url_for('perfil'))
    
    transacoes_count = Transacao.query.filter_by(user_id=current_user.id).count()
    lembretes_count = Lembrete.query.filter_by(user_id=current_user.id).count()
    badges_count = Badge.query.filter_by(user_id=current_user.id).count()
    
    return render_template('perfil.html', transacoes_count=transacoes_count, lembretes_count=lembretes_count, badges_count=badges_count)

# Configurar o caminho do wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

@app.route('/exportar_relatorio')
@login_required
def exportar_relatorio():
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    transacoes = Transacao.query.filter_by(user_id=current_user.id).all()
    categorias = db.session.query(Transacao.categoria).filter_by(user_id=current_user.id).distinct().all()
    categorias = [cat[0] for cat in categorias]
    
    total_despesas = {}
    total_receitas = {}
    for mes in meses:
        total_despesas[mes] = round(db.session.query(func.sum(Transacao.valor)).filter_by(user_id=current_user.id, tipo='despesa', mes=mes).scalar() or 0, 2)
        total_receitas[mes] = round(db.session.query(func.sum(Transacao.valor)).filter_by(user_id=current_user.id, tipo='receita', mes=mes).scalar() or 0, 2)
    
    total_livre = {mes: total_receitas[mes] - total_despesas[mes] for mes in meses}
    
    # Renderiza o template HTML para o relatório
    html = render_template('relatorio.html', transacoes=transacoes, meses=meses, categorias=categorias, 
                           total_despesas=total_despesas, total_receitas=total_receitas, total_livre=total_livre)
    
    # Gera o PDF
    pdf = pdfkit.from_string(html, False, configuration=config)
    
    # Envia o PDF como download
    return send_file(io.BytesIO(pdf), as_attachment=True, download_name='relatorio_financas99.pdf', mimetype='application/pdf')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta. Até logo! 👋', 'success')
    return redirect(url_for('login'))

@app.route('/metas', methods=['GET', 'POST'])
@login_required
def metas():
    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = float(request.form['valor'])
        mes = request.form['mes']
        ano = int(request.form['ano'])
        descricao = request.form['descricao']
        
        meta = Meta(user_id=current_user.id, tipo=tipo, valor=valor, mes=mes, ano=ano, descricao=descricao)
        db.session.add(meta)
        db.session.commit()
        flash('Meta adicionada com sucesso! 🎯', 'success')
        return redirect(url_for('metas'))
    
    metas = Meta.query.filter_by(user_id=current_user.id).all()
    return render_template('metas.html', metas=metas)

@app.route('/editar_meta/<int:meta_id>', methods=['GET', 'POST'])
@login_required
def editar_meta(meta_id):
    meta = Meta.query.get_or_404(meta_id)
    if meta.user_id != current_user.id:
        flash('Você não tem permissão para editar esta meta!', 'error')
        return redirect(url_for('metas'))
    
    if request.method == 'POST':
        meta.tipo = request.form['tipo']
        meta.valor = float(request.form['valor'])
        meta.mes = request.form['mes']
        meta.ano = int(request.form['ano'])
        meta.descricao = request.form['descricao']
        db.session.commit()
        flash('Meta atualizada com sucesso! ✏️', 'success')
        return redirect(url_for('metas'))
    
    return render_template('editar_meta.html', meta=meta)

@app.route('/excluir_meta/<int:meta_id>')
@login_required
def excluir_meta(meta_id):
    meta = Meta.query.get_or_404(meta_id)
    if meta.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta meta!', 'error')
        return redirect(url_for('metas'))
    
    db.session.delete(meta)
    db.session.commit()
    flash('Meta excluída com sucesso! 🗑️', 'success')
    return redirect(url_for('metas'))