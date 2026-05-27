import streamlit as st
import random
import time
import requests # Necessário para enviar o e-mail via API

# Configuração da página para ficar bonita no celular e PC
st.set_page_config(page_title="Simulador de Lançamentos - Contabilidade II", page_icon="📊", layout="centered")

# Título do Aplicativo
#st.title("📊 Simulador de Lançamentos Contábeis")
#st.markdown("---")

# --- CABEÇALHO INSTITUCIONAL PERSONALIZADO ---
st.markdown("### 🎓 UNIDAVI — Administração de Empresas")
st.markdown("**Turma:** `ADE12026T1` | **Disciplina:** Legislação e Planejamento Tributário")
st.markdown("**Professor:** Prof. Me. Gilmarques Agapito Costa")
st.title("📊 Simulador de Lançamentos")
st.markdown("---")

# --- GERENCIAMENTO DE ESTADO (SESSION STATE) ---
if 'rodadas' not in st.session_state:
    st.session_state.rodadas = []  # Guarda o histórico das 10 rodadas
if 'operacao_sorteada' not in st.session_state:
    st.session_state.operacao_sorteada = "👇 Clique abaixo para girar"
    st.session_state.objeto_sorteado = "👇 Clique abaixo para girar"
    st.session_state.valor_sorteado = "👇 Clique abaixo para girar"
if 'email_enviado' not in st.session_state:
    st.session_state.email_enviado = False

# --- FUNÇÃO PARA ENVIAR E-MAIL VIA RESEND ---
def enviar_email_resend(nome_aluno, historico_rodadas):
    # Seu e-mail de professor onde quer receber as respostas
    email_professor = "gilmarques.costa@unidavi.edu.br" 
    
    # Busca a chave de API cadastrada com segurança no Streamlit
    resend_api_key = st.secrets["RESEND_API_KEY"]
    
    # Monta o texto do e-mail em HTML
    linhas_tabela = ""
    for r in historico_rodadas:
        linhas_tabela += f"<tr><td>{r['Numero']}</td><td>{r['Operação']}</td><td>{r['Objeto']}</td><td>{r['Valor']}</td></tr>"
        
    html_conteudo = f"""
    <h3>Desafio Concluído - Contabilidade II</h3>
    <p><strong>Aluno:</strong> {nome_aluno}</p>
    <table border='1' cellpadding='5' style='border-collapse: collapse;'>
        <thead>
            <tr style='background-color: #f2f2f2;'>
                <th>Rodada</th><th>Operação</th><th>Objeto</th><th>Valor</th>
            </tr>
        </thead>
        <tbody>
            {linhas_tabela}
        </tbody>
    </table>
    <br><p><em>E-mail gerado automaticamente pelo Simulador de Lançamentos.</em></p>
    """
    
    # Requisição para a API do Resend
    headers = {
        "Authorization": f"Bearer {resend_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "from": "Simulador <onboarding@resend.dev>",
        "to": [email_professor],
        "subject": f"🎯 10 Rodadas Concluídas: {nome_aluno}",
        "html": html_conteudo
    }
    
    response = requests.post("https://api.resend.com/emails", headers=headers, json=data)
    return response.status_code == 200

# --- INTERACTION: ENTRADA DE DADOS ---
nome_aluno = st.text_input("✍️ Digite seu nome completo antes de começar:", value="", placeholder="Seu nome aqui...")

st.markdown("""
**Instruções:** Digite seu nome, clique no botão para girar as roletas e repita o processo por **10 vezes**. 
Ao finalizar a 10ª rodada, seus dados serão enviados diretamente para o professor.
""")

# Banco de dados das roletas
operacoes = ["COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA"]
objetos = ["Matéria-prima", "Produto", "Mercadoria", "Serviço", "Matéria-prima", "Produto", "Mercadoria", "Serviço", "Matéria-prima", "Produto", "Mercadoria", "Serviço"]
valores = [900, 400, 500, 150, 750, 600, 550, 800, 300, 950, 700, 100, 850, 650, 450, 250, 200, 350]

st.markdown("### 🎲 Suas Roletas:")

# Criação do layout visual para o sorteio
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Operação")
    st.info(f"**{st.session_state.operacao_sorteada}**")

with col2:
    st.subheader("2. Objeto")
    st.warning(f"**{st.session_state.objeto_sorteado}**")

with col3:
    st.subheader("3. Valor")
    st.success(f"**{st.session_state.valor_sorteado}**")

st.markdown("---")

# Controla o total de rodadas atuais
total_rodadas = len(st.session_state.rodadas)
st.metric(label="Progresso do Aluno", value=f"{total_rodadas} / 10 Rodadas")

# --- LÓGICA DO BOTÃO E JOGO ---
# Bloqueia o botão se o nome estiver vazio ou se já chegou a 10 rodadas
botao_desabilitado = total_rodadas >= 10 or nome_aluno.strip() == ""

if st.button("🎰 GIRAR ROLETAS SIMULTANEAMENTE", use_container_width=True, disabled=botao_desabilitado):
    with st.spinner('Girando as roletas...'):
        time.sleep(0.8) 
        
        # Sorteio aleatório
        op = random.choice(operacoes)
        obj = random.choice(objetos)
        val = random.choice(valores)
        valor_formatado = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Atualizando o estado da tela
        st.session_state.operacao_sorteada = op
        st.session_state.objeto_sorteado = obj
        st.session_state.valor_sorteado = valor_formatado
        
        # Salva a rodada no histórico
        st.session_state.rodadas.append({
            "Numero": total_rodadas + 1,
            "Operação": op,
            "Objeto": obj,
            "Valor": valor_formatado
        })
        
    st.rerun()

# Se atingiu 10 rodadas, faz o envio automático do e-mail
if total_rodadas == 10 and not st.session_state.email_enviado:
    with st.spinner('Enviando seu relatório ao professor...'):
        sucesso = enviar_email_resend(nome_aluno, st.session_state.rodadas)
        if sucesso:
            st.session_state.email_enviado = True
            st.success("🎉 Parabéns! Suas 10 rodadas foram concluídas e enviadas com sucesso para o e-mail do professor!")
            st.balloons()
        else:
            st.error("Erro ao enviar o e-mail automático. Avise seu professor ou tire um print da tela.")

# Exibe o histórico na tela para o aluno acompanhar
if total_rodadas > 0:
    st.markdown("### 📋 Seu Histórico de Rodadas")
    st.table(st.session_state.rodadas)
    
    # Botão secreto/opcional caso o aluno queira reiniciar o jogo do zero
    if st.button("🔄 Reiniciar tudo (Limpar histórico)"):
        st.session_state.rodadas = []
        st.session_state.email_enviado = False
        st.session_state.operacao_sorteada = "👇 Clique abaixo para girar"
        st.session_state.objeto_sorteado = "👇 Clique abaixo para girar"
        st.session_state.valor_sorteado = "👇 Clique abaixo para girar"
        st.rerun()
