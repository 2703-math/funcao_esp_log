import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Exponencial & Logaritmo",
    page_icon="📈",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .equation-box {
        background: #1a1a2e;
        color: #fff;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Courier New', monospace;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE PLOTAGEM (PLOTLY)
# ============================================
def criar_layout_cartesiano(fig, title="Plano Cartesiano", range_x=[-10, 10], range_y=[-10, 10]):
    """Aplica o estilo de 'papel milimetrado' com eixos fixos"""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        plot_bgcolor='#fafafa',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        height=500,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)")
    )
    fig.update_xaxes(
        range=range_x, zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=1
    )
    fig.update_yaxes(
        range=range_y, zeroline=True, zerolinewidth=2, zerolinecolor='#2c3e50',
        gridcolor='#e0e0e0', dtick=1
    )
    return fig

def plot_exponencial(a, b, c):
    fig = go.Figure()
    
    x = np.linspace(-10, 10, 400)
    y = a * (b**x) + c
    
    cor_linha = '#e74c3c' if b > 1 else '#f39c12'
    nome = 'Crescimento' if b > 1 else 'Decaimento'
    
    # Gráfico da Função
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines', name=f'f(x) ({nome})',
        line=dict(color=cor_linha, width=4)
    ))
    
    # Assíntota Horizontal
    fig.add_trace(go.Scatter(
        x=[-10, 10], y=[c, c], mode='lines', name=f'Assíntota (y={c})',
        line=dict(color='#7f8c8d', width=2, dash='dot')
    ))
    
    # Ponto de Corte no Eixo Y (x=0)
    corte_y = a + c
    if -10 <= corte_y <= 10:
        fig.add_trace(go.Scatter(
            x=[0], y=[corte_y], mode='markers+text', name='Corte Y',
            marker=dict(color='#3498db', size=12, line=dict(color='white', width=2)),
            text=[f' (0, {corte_y:.1f})'], textposition='middle right',
            textfont=dict(color='#2980b9', size=13, family="Arial Black")
        ))
        
    return criar_layout_cartesiano(fig)

def plot_logaritmica(a, b, c):
    fig = go.Figure()
    
    # Domínio do log: x > 0. Para o gráfico ficar bonito, usamos um offset bem pequeno.
    x = np.linspace(0.001, 10, 400)
    # Mudança de base: log_b(x) = ln(x) / ln(b)
    y = a * (np.log(x) / np.log(b)) + c
    
    cor_linha = '#2980b9' if b > 1 else '#8e44ad'
    
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='lines', name='f(x) = a·log_b(x) + c',
        line=dict(color=cor_linha, width=4)
    ))
    
    # Assíntota Vertical (Eixo Y)
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[-10, 10], mode='lines', name='Assíntota Vertical (x=0)',
        line=dict(color='#7f8c8d', width=2, dash='dot')
    ))
    
    # Raiz (onde corta o eixo X, f(x) = 0)
    raiz_x = b**(-c/a)
    if 0 < raiz_x <= 10:
        fig.add_trace(go.Scatter(
            x=[raiz_x], y=[0], mode='markers+text', name='Raiz',
            marker=dict(color='#e74c3c', size=12, line=dict(color='white', width=2)),
            text=[f' ({raiz_x:.2f}, 0)'], textposition='top center',
            textfont=dict(color='#c0392b', size=13, family="Arial Black")
        ))
        
    return criar_layout_cartesiano(fig)

def plot_inversas(b, x_ponto):
    fig = go.Figure()
    
    # Eixo espelho (y = x)
    fig.add_trace(go.Scatter(
        x=[-10, 10], y=[-10, 10], mode='lines', name='Espelho (y = x)',
        line=dict(color='#95a5a6', width=2, dash='dash')
    ))
    
    # Exponencial
    x_exp = np.linspace(-10, 10, 400)
    y_exp = b**x_exp
    fig.add_trace(go.Scatter(
        x=x_exp, y=y_exp, mode='lines', name=f'y = {b}^x',
        line=dict(color='#e74c3c', width=3)
    ))
    
    # Logaritmo
    x_log = np.linspace(0.001, 10, 400)
    y_log = np.log(x_log) / np.log(b)
    fig.add_trace(go.Scatter(
        x=x_log, y=y_log, mode='lines', name=f'y = log_{b}(x)',
        line=dict(color='#3498db', width=3)
    ))
    
    # Pontos Espelhados
    y_ponto = b**x_ponto
    
    if -10 <= y_ponto <= 10:
        # Ponto na Exponencial (x, y)
        fig.add_trace(go.Scatter(
            x=[x_ponto], y=[y_ponto], mode='markers+text', name='Ponto Exp',
            marker=dict(color='#c0392b', size=12),
            text=[f' ({x_ponto:.1f}, {y_ponto:.1f})'], textposition='top left',
            textfont=dict(family="Arial Black", color='#c0392b')
        ))
        
        # Ponto no Logaritmo (y, x) -> As coordenadas se invertem!
        fig.add_trace(go.Scatter(
            x=[y_ponto], y=[x_ponto], mode='markers+text', name='Ponto Log',
            marker=dict(color='#2980b9', size=12),
            text=[f' ({y_ponto:.1f}, {x_ponto:.1f})'], textposition='bottom right',
            textfont=dict(family="Arial Black", color='#2980b9')
        ))
        
        # Linha de conexão mostrando a reflexão
        fig.add_trace(go.Scatter(
            x=[x_ponto, y_ponto], y=[y_ponto, x_ponto], mode='lines',
            showlegend=False, line=dict(color='#7f8c8d', width=1, dash='dot')
        ))

    return criar_layout_cartesiano(fig, title="O Espelho das Funções Inversas")

def plot_escala(dados_nome, dados_val, titulo):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Escala Linear (Realidade)", "Escala Logarítmica (Visualização)"))
    
    # Gráfico 1: Escala Linear
    fig.add_trace(go.Bar(
        x=dados_nome, y=dados_val, marker_color='#e74c3c', text=dados_val, texttemplate='%{text:.1e}', textposition='outside'
    ), row=1, col=1)
    
    # Gráfico 2: Escala Log
    log_vals = [math.log10(v) for v in dados_val]
    fig.add_trace(go.Bar(
        x=dados_nome, y=log_vals, marker_color='#3498db', text=log_vals, texttemplate='%{text:.1f}', textposition='outside'
    ), row=1, col=2)
    
    fig.update_layout(height=450, showlegend=False, plot_bgcolor='white', title=titulo)
    fig.update_yaxes(showgrid=True, gridcolor='#ecf0f1')
    return fig

# ============================================
# MENU LATERAL E NAVEGAÇÃO
# ============================================
st.markdown('<div class="main-title">📈 Universos Exponenciais e Logarítmicos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Entenda o crescimento acelerado, as curvas inversas e a escala do mundo real</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Módulos")
    topico = st.radio(
        "Navegue pelos temas:",
        [
            "1. Função Exponencial", 
            "2. Função Logarítmica",
            "3. O Espelho (Funções Inversas)",
            "4. Escalas Logarítmicas (Mundo Real)"
        ],
        index=0
    )

# ============================================
# TÓPICO 1: FUNÇÃO EXPONENCIAL
# ============================================
if topico == "1. Função Exponencial":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>O Crescimento Acelerado:</b> Na função exponencial <b>f(x) = a · bˣ + c</b>, a variável x está no expoente! 
        Isso faz com que ela cresça (ou diminua) de forma explosiva. A base <b>b</b> define a taxa de multiplicação.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_graf = st.columns([1, 2.5])
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        b = st.slider("Base (b)", 0.1, 5.0, 2.0, step=0.1)
        if b == 1.0:
            st.error("A base não pode ser 1! (1 elevado a qualquer coisa é 1, viraria uma reta reta).")
            st.stop()
        a = st.slider("Multiplicador (a)", -5.0, 5.0, 1.0, step=0.5)
        c = st.slider("Deslocamento Vertical (c)", -8.0, 8.0, 0.0, step=1.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        sinal_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
        st.markdown(f"<div class='equation-box'>f(x) = {a} · ({b:.1f})ˣ {sinal_c}</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-box">
            <b>Desafio Visual:</b><br>
            1. Mova a base <b>b</b> para menor que 1 (ex: 0.5). Veja a curva inverter (Decaimento radioativo).<br>
            2. Mova <b>c</b> para ver a Assíntota Horizontal (a linha que a curva tenta tocar, mas nunca consegue).
        </div>
        """, unsafe_allow_html=True)
        
    with col_graf:
        fig = plot_exponencial(a, b, c)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TÓPICO 2: FUNÇÃO LOGARÍTMICA
# ============================================
elif topico == "2. Função Logarítmica":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>O Freio Matemático:</b> A função logarítmica <b>f(x) = a · log_b(x) + c</b> é exatamente o oposto da exponencial. 
        Enquanto a exponencial cresce rápido demais, o logaritmo cresce devagar demais. Ele possui uma <b>Assíntota Vertical</b> e só existe para x > 0.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_graf = st.columns([1, 2.5])
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        b = st.slider("Base (b)", 0.1, 5.0, 2.0, step=0.1)
        if b == 1.0:
            st.error("A base do logaritmo não pode ser 1!")
            st.stop()
        a = st.slider("Multiplicador (a)", -5.0, 5.0, 1.0, step=0.5)
        if a == 0:
            st.error("O multiplicador 'a' não pode ser 0.")
            st.stop()
        c = st.slider("Deslocamento Vertical (c)", -8.0, 8.0, 0.0, step=1.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        sinal_c = f"+ {c}" if c >= 0 else f"- {abs(c)}"
        st.markdown(f"<div class='equation-box'>f(x) = {a} · log_{b:.1f}(x) {sinal_c}</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-box">
            <b>Desafio Visual:</b><br>
            1. Note que a curva não cruza para a esquerda do eixo Y. Valores negativos não existem no logaritmo real!<br>
            2. Veja como o crescimento despenca à medida que x aumenta.
        </div>
        """, unsafe_allow_html=True)
        
    with col_graf:
        fig = plot_logaritmica(a, b, c)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TÓPICO 3: FUNÇÕES INVERSAS
# ============================================
elif topico == "3. O Espelho (Funções Inversas)":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>A Prova Geométrica:</b> Uma função é o inverso da outra. Isso significa que se a exponencial transforma o ponto <b>X</b> no ponto <b>Y</b>, 
        o logaritmo pegará o ponto <b>Y</b> e o devolverá para o <b>X</b>! No gráfico, isso se parece com um reflexo perfeito através da linha diagonal (y = x).
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_graf = st.columns([1, 2.5])
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        b = st.slider("Base (b) para ambas", 1.1, 4.0, 2.0, step=0.1)
        st.markdown("---")
        x_ponto = st.slider("Deslize um Ponto X", -2.0, 3.0, 1.0, step=0.2)
        st.markdown("</div>", unsafe_allow_html=True)
        
        y_ponto = b**x_ponto
        
        st.markdown(f"""
        <div style="font-size:1.1rem; line-height:2;">
        <b>1. Na Exponencial:</b><br>
        Se x = {x_ponto:.1f} <br>
        y = {b:.1f}<sup>{x_ponto:.1f}</sup> = <b>{y_ponto:.2f}</b><br>
        Coordenada: <span style="color:#c0392b; font-weight:bold;">({x_ponto:.1f}, {y_ponto:.2f})</span>
        <hr>
        <b>2. No Logaritmo:</b><br>
        Pegamos o resultado e jogamos no eixo X:<br>
        Se x = {y_ponto:.2f} <br>
        y = log<sub>{b:.1f}</sub>({y_ponto:.2f}) = <b>{x_ponto:.1f}</b><br>
        Coordenada: <span style="color:#2980b9; font-weight:bold;">({y_ponto:.2f}, {x_ponto:.1f})</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_graf:
        fig = plot_inversas(b, x_ponto)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TÓPICO 4: ESCALAS LOGARÍTMICAS
# ============================================
elif topico == "4. Escalas Logarítmicas (Mundo Real)":
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2c3e50;">
        <b>Por que inventaram o Logaritmo?</b> No mundo real, algumas coisas crescem de forma tão absurda que não cabem em um gráfico normal (linear). 
        A escala logarítmica "espreme" os números gigantes, transformando multiplicações em somas.
    </div>
    """, unsafe_allow_html=True)
    
    fenomeno = st.selectbox(
        "Escolha um exemplo real:",
        ["Terremotos (Escala Richter)", "Acidez Química (Escala de pH)", "Intensidade Sonora (Decibéis)"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if fenomeno == "Terremotos (Escala Richter)":
        st.markdown("Na Escala Richter, um terremoto grau 6 não é o 'dobro' de um grau 3. Ele tem uma amplitude de ondas sísmicas **1.000 vezes maior**! Como grafar 1.000 e 1.000.000 no mesmo papel? Usamos o logaritmo (base 10) para transformar as grandezas 10³, 10⁵ e 10⁷ em simples 3, 5 e 7.")
        
        nomes = ["Grau 3 (Leve)", "Grau 5 (Médio)", "Grau 7 (Devastador)"]
        amplitudes = [10**3, 10**5, 10**7]
        fig = plot_escala(nomes, amplitudes, "Amplitude Sísmica Relativa")
        st.plotly_chart(fig, use_container_width=True)

    elif fenomeno == "Acidez Química (Escala de pH)":
        st.markdown("O pH mede a concentração de íons de Hidrogênio. A fórmula é `pH = -log10[H+]`. Um líquido com pH 4 tem **100 vezes** mais íons de hidrogênio (mais ácido) que um líquido com pH 6. O gráfico linear mostra como a concentração explode quando o pH cai!")
        
        nomes = ["pH 6 (Leite)", "pH 5 (Café)", "pH 4 (Suco de Tomate)"]
        concentracoes = [10**-6, 10**-5, 10**-4]
        # Inverter para mostrar a "quantidade" crescente visualmente no bar chart
        conc_visual = [1, 10, 100] 
        fig = plot_escala(nomes, conc_visual, "Concentração de [H+] relativa ao Leite (Linear x Log)")
        st.plotly_chart(fig, use_container_width=True)

    elif fenomeno == "Intensidade Sonora (Decibéis)":
        st.markdown("O ouvido humano escuta desde um alfinete caindo até um motor a jato. A energia acústica do motor é **10 Trilhões** de vezes maior! Usamos a escala logarítmica (Bel/Decibel) para não enlouquecer com os zeros.")
        
        nomes = ["Sussurro (30 dB)", "Conversa (60 dB)", "Tráfego (90 dB)"]
        energias = [10**3, 10**6, 10**9]
        fig = plot_escala(nomes, energias, "Energia Sonora Relativa")
        st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    📈 <b>Matemática Visual</b> — Ferramenta educacional para o ensino médio
</div>
""", unsafe_allow_html=True)