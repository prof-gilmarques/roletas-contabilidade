import streamlit as st
import random
import time

# Configuração da página para ficar bonita no celular e PC
st.set_page_config(page_title="Simulador de Lançamentos - Contabilidade II", page_icon="📊", layout="centered")

# Título do Aplicativo
st.title("📊 Simulador de Lançamentos Contábeis")
st.markdown("---")
st.markdown("""
**Instruções:** Clique no botão abaixo para gerar o seu desafio contábil individual. 
Após o sorteio, realize o lançamento contábil correspondente conforme as instruções do seu professor.
""")

# Banco de dados das roletas
operacoes = ["COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA","COMPRA", "VENDA"]
objetos = ["Matéria-prima", "Produto", "Mercadoria", "Serviço", "Matéria-prima", "Produto", "Mercadoria", "Serviço", "Matéria-prima", "Produto", "Mercadoria", "Serviço"]
valores = [900, 400, 500, 150, 750, 600, 550, 800, 300, 950, 700, 100, 850, 650, 450, 250, 200, 350]

# Inicializa o estado da sessão para manter os valores na tela
if 'operacao_sorteada' not in st.session_state:
    st.session_state.operacao_sorteada = "👇 Clique abaixo para girar"
    st.session_state.objeto_sorteado = "👇 Clique abaixo para girar"
    st.session_state.valor_sorteado = "👇 Clique abaixo para girar"

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

# Botão para girar as roletas
if st.button("🎰 GIRAR ROLETAS SIMULTANEAMENTE", use_container_width=True):
    # Efeito visual de "carregamento/giro"
    with st.spinner('Girando as roletas...'):
        time.sleep(1) # Delay dramático de 1 segundo
        
        # Sorteio aleatório
        op = random.choice(operacoes)
        obj = random.choice(objetos)
        val = random.choice(valores)
        
        # Atualizando o estado da tela com formatação em Real brasileiro (R$)
        st.session_state.operacao_sorteada = op
        st.session_state.objeto_sorteado = obj
        st.session_state.valor_sorteado = f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
    st.balloons() # Efeito de comemoração na tela
    st.rerun()
