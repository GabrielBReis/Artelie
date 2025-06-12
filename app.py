from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Mude esta chave em produção!


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Renderiza a página de login e processa as submissões do formulário de login.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário
        username = request.form['username']
        password = request.form['password']

        if username == 'user' and password == 'password':
            flash('Login realizado com sucesso!', 'success') # Mensagem de sucesso
            return redirect(url_for('success')) # Redireciona para a página de sucesso
        else:
            flash('Usuário ou senha inválidos.', 'error') 
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('cadastro.html')
        elif len(new_password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('cadastro.html')
        else:
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login')) # Redireciona para a página de login após o cadastro
    return render_template('cadastro.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')  # Crie esse arquivo .html


if __name__ == '__main__':
    # Define o modo de depuração para True (útil para desenvolvimento, desative em produção)
    app.run(debug=True)
