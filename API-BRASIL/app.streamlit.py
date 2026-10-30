import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Consulta BrasilAPI",
    page_icon="🇧🇷",
    layout="wide"
)

# URL da sua API Flask local
API_FLASK_URL = "http://127.0.0.1:5000"

st.title("🇧🇷 Painel de Consultas - BrasilAPI")
st.markdown("Interface visual conectada ao seu backend em **Flask**.")

# Navegação por abas
aba_cep, aba_cnpj, aba_ddd, aba_bancos = st.tabs(["📌 CEP", "🏢 CNPJ", "📞 DDD", "🏦 Bancos"])

# --- ABA 1: CEP ---
with aba_cep:
    st.header("Consulta de CEP")
    cep_input = st.text_input("Digite o CEP (somente números ou formatado):", placeholder="01310-100")
    
    if st.button("Buscar CEP", type="primary"):
        if cep_input:
            with st.spinner("Consultando..."):
                try:
                    res = requests.get(f"{API_FLASK_URL}/cep/{cep_input}")
                    if res.status_code == 200:
                        dados = res.json()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"**Logradouro:** {dados.get('street', 'N/A')}")
                            st.info(f"**Bairro:** {dados.get('neighborhood', 'N/A')}")
                        with col2:
                            st.info(f"**Cidade/UF:** {dados.get('city', 'N/A')} - {dados.get('state', 'N/A')}")
                            st.info(f"**CEP:** {dados.get('cep', 'N/A')}")
                    else:
                        st.error(res.json().get("erro", "Erro ao buscar CEP."))
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão: Verifique se a sua API Flask está rodando!")
        else:
            st.warning("Por favor, digite um CEP.")

# --- ABA 2: CNPJ ---
with aba_cnpj:
    st.header("Consulta de CNPJ")
    cnpj_input = st.text_input("Digite o CNPJ:", placeholder="00.000.000/0001-91")
    
    if st.button("Buscar CNPJ", type="primary"):
        if cnpj_input:
            with st.spinner("Consultando..."):
                try:
                    res = requests.get(f"{API_FLASK_URL}/cnpj/{cnpj_input}")
                    if res.status_code == 200:
                        dados = res.json()
                        st.success(f"**Razão Social:** {dados.get('razao_social')}")
                        st.write(f"**Nome Fantasia:** {dados.get('nome_fantasia', 'N/A')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Situação Cadastral:** {dados.get('descricao_situacao_cadastral')}")
                            st.write(f"**Data de Abertura:** {dados.get('data_inicio_atividade')}")
                        with col2:
                            st.write(f"**UF:** {dados.get('uf')} | **Município:** {dados.get('municipio')}")
                            st.write(f"**CNAE Principal:** {dados.get('cnae_fiscal_descricao')}")
                    else:
                        st.error(res.json().get("erro", "Erro ao buscar CNPJ."))
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão: Verifique se a sua API Flask está rodando!")
        else:
            st.warning("Por favor, digite um CNPJ.")

# --- ABA 3: DDD ---
with aba_ddd:
    st.header("Consulta de DDD")
    ddd_input = st.text_input("Digite o DDD (2 dígitos):", placeholder="47")
    
    if st.button("Buscar DDD", type="primary"):
        if ddd_input:
            with st.spinner("Consultando..."):
                try:
                    res = requests.get(f"{API_FLASK_URL}/ddd/{ddd_input}")
                    if res.status_code == 200:
                        dados = res.json()
                        st.success(f"**Estado (UF):** {dados.get('state')}")
                        st.subheader("Cidades Atendidas:")
                        cidades = dados.get("cities", [])
                        st.write(", ".join(cidades))
                    else:
                        st.error(res.json().get("erro", "Erro ao buscar DDD."))
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão: Verifique se a sua API Flask está rodando!")
        else:
            st.warning("Por favor, digite um DDD.")

# --- ABA 4: BANCOS ---
with aba_bancos:
    st.header("Lista de Bancos do Brasil")
    
    if st.button("Carregar Lista de Bancos"):
        with st.spinner("Carregando bancos..."):
            try:
                res = requests.get(f"{API_FLASK_URL}/bancos")
                if res.status_code == 200:
                    bancos = res.json()
                    st.dataframe(bancos, use_container_width=True)
                else:
                    st.error("Erro ao carregar lista de bancos.")
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão: Verifique se a sua API Flask está rodando!")