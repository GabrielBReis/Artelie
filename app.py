# Importa o Flask, render_template (para renderizar HTML) e request (para acessar dados de requisições)
from flask import Flask, render_template, request, redirect, url_for, flash

# Cria uma instância da aplicação Flask
app = Flask(__name__)
# Define uma chave secreta para a sessão, usada para flash messages (mensagens temporárias)
app.secret_key = 'supersecretkey' # Mude esta chave em produção!

# --- Rota para a página de Login ---
# Esta rota responde a requisições GET para a raiz ('/') e para '/login'
@app.route('/', methods=['GET', 'POST'])
@app.route('/Artelie\apresentacao\view\templates\login.html', methods=['GET', 'POST'])
def login():
    """
    Renderiza a página de login e processa as submissões do formulário de login.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário
        username = request.form['username']
        password = request.form['password']

        # --- Lógica de Autenticação Simplificada (APENAS PARA EXEMPLO) ---
        # Em uma aplicação real, você verificaria o usuário e senha em um banco de dados
        if username == 'user' and password == 'password':
            flash('Login realizado com sucesso!', 'success') # Mensagem de sucesso
            return redirect(url_for('success')) # Redireciona para a página de sucesso
        else:
            flash('Usuário ou senha inválidos.', 'error') # Mensagem de erro
            # Permanece na página de login para que o usuário possa tentar novamente
            return render_template('login.html')
    # Se for uma requisição GET, apenas renderiza o formulário de login
    return render_template('Artelie\apresentacao\view\templates\login.html')

# --- Rota para a página de Cadastro ---
# Esta rota responde a requisições GET e POST para '/register'
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renderiza a página de cadastro e processa as submissões do formulário de cadastro.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário de cadastro
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # --- Lógica de Cadastro Simplificada (APENAS PARA EXEMPLO) ---
        # Em uma aplicação real, você faria validações mais complexas
        # e salvaria os dados no banco de dados.
        if new_password != confirm_password:
            flash('As senhas não coincidem.', 'error')
            return render_template('cadastro.html') # Permanece na página de cadastro
        elif len(new_password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('cadastro.html')
        else:
            # Simula um cadastro bem-sucedido
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login')) # Redireciona para a página de login após o cadastro
    # Se for uma requisição GET, apenas renderiza o formulário de cadastro
    return render_template('cadastro.html')

# --- Rota para a página de Sucesso ---
@app.route('/success')
def success():
    """
    Página simples para indicar que o login foi bem-sucedido.
    """
    return render_template('cadastro.html')

# --- Executa a aplicação ---
# Isso só acontece se o script for executado diretamente (não importado como módulo)
if __name__ == '__main__':
    # Define o modo de depuração para True (útil para desenvolvimento, desative em produção)
    app.run(debug=True)
