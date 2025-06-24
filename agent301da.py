import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
import pandas as pd
import os
import zipfile
import tempfile
import shutil
from dotenv import load_dotenv

st.set_page_config(
    page_title="Agent 301 DA",
    page_icon="🤖"
)

# Carregar variáveis do arquivo .env
load_dotenv()

st.markdown('<h1 style="font-size: 2.5rem; text-align: center;">Agente Autônomo de Análise de Dados</h1>', unsafe_allow_html=True)
st.markdown("---")

# Botão para limpar arquivos temporários
if st.button("🗑️ Limpar arquivos temporários"):
    if os.path.exists("temp_data"):
        shutil.rmtree("temp_data")
        st.success("Arquivos temporários removidos!")
    else:
        st.info("Nenhum arquivo temporário encontrado.")

st.markdown("---")

# Seletor do tipo de arquivo
file_type = st.selectbox(
    "📁 Tipo de arquivo:",
    ["CSV único", "ZIP com múltiplos CSVs"]
)

if file_type == "CSV único":
    uploaded_file = st.file_uploader("📦 Carregue um arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        csv_file_path = uploaded_file.name
        
        with open(csv_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        df = pd.read_csv(csv_file_path)
        st.write("✅ Arquivo CSV carregado")
        st.dataframe(df.head())
        st.write("📊 Total de registros:", len(df))

else:  # ZIP com múltiplos CSVs
    uploaded_file = st.file_uploader("📦 Carregue o arquivo ZIP", type="zip")
    
    if uploaded_file is not None:
        # Criar diretório de trabalho permanente
        work_dir = "temp_data"
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        
        # Salvar o arquivo ZIP
        zip_path = os.path.join(work_dir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extrair o arquivo ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(work_dir)
            extracted_files = zip_ref.namelist()
        
        st.write("✅ Arquivo ZIP extraído com sucesso!")
        st.write("📁 Arquivos encontrados:", extracted_files)
        
        # Procurar pelos arquivos de cabeçalho e itens
        cabecalho_file = None
        itens_file = None
        
        for file in extracted_files:
            file_path = os.path.join(work_dir, file)
            if 'cabecalho' in file.lower() or 'cabeçalho' in file.lower():
                cabecalho_file = file_path
            elif 'itens' in file.lower() or 'item' in file.lower():
                itens_file = file_path
        
        if cabecalho_file and itens_file:
            # Carregar os DataFrames
            df_cabecalho = pd.read_csv(cabecalho_file)
            df_itens = pd.read_csv(itens_file)
            
            st.write("### 📋 Dados do Cabeçalho das Notas Fiscais")
            st.dataframe(df_cabecalho.head())
            st.write("📊 Total de notas fiscais (cabeçalho):", len(df_cabecalho))
            
            st.write("### 📝 Dados dos Itens das Notas Fiscais")
            st.dataframe(df_itens.head())
            st.write("📊 Total de itens:", len(df_itens))
            
            # Verificar colunas comuns para mesclagem
            st.write("### 🔗 Preparando Mesclagem dos Dados")
            
            colunas_cabecalho = set(df_cabecalho.columns)
            colunas_itens = set(df_itens.columns)
            colunas_comuns = colunas_cabecalho.intersection(colunas_itens)
            
            st.write("🔍 Colunas comuns encontradas:", list(colunas_comuns))
            
            # Tentar identificar a chave de junção automaticamente
            possible_keys = ['id', 'numero', 'nf', 'nota_fiscal', 'documento', 'chave']
            merge_key = None
            
            for key in possible_keys:
                matching_cols = [col for col in colunas_comuns if key.lower() in col.lower()]
                if matching_cols:
                    merge_key = matching_cols[0]
                    break
            
            if not merge_key and colunas_comuns:
                merge_key = list(colunas_comuns)[0]
            
            if merge_key:
                st.write("🔑 Chave de mesclagem identificada:", merge_key)
                
                # Realizar a mesclagem
                df_merged = pd.merge(df_cabecalho, df_itens, on=merge_key, how='inner')
                
                st.write("### ✅ Dados Mesclados (Cabeçalho + Itens)")
                st.dataframe(df_merged.head())
                st.write("📊 Total de registros mesclados:", len(df_merged))
                
                # Salvar o arquivo mesclado
                merged_file_path = os.path.join(work_dir, "notas_fiscais_mescladas.csv")
                df_merged.to_csv(merged_file_path, index=False)
                csv_file_path = merged_file_path
                df = df_merged
                
            else:
                st.error("❌ Não foi possível identificar uma chave comum para mesclagem.")
                st.write("💡 Colunas do Cabeçalho:", list(df_cabecalho.columns))
                st.write("💡 Colunas dos Itens:", list(df_itens.columns))
                st.stop()
                
        else:
            st.error("❌ Não foram encontrados os arquivos de cabeçalho e itens esperados.")
            st.write("💡 Arquivos encontrados:", extracted_files)
            st.stop()

# Se chegou até aqui, temos os dados prontos para análise
if uploaded_file is not None and 'df' in locals():
    
    # Função para validar e corrigir queries do agente
    def enhance_query_for_full_dataset(original_query, df_info):
        """Adiciona validações automáticas para garantir uso do dataset completo"""
        
        enhanced_query = f"""
IMPORTANTE: Você está analisando um dataset com {df_info['total_rows']} registros e {df_info['total_cols']} colunas.

REGRAS OBRIGATÓRIAS:
1. SEMPRE use df.shape[0] para confirmar o número total de registros
2. NUNCA use apenas .head() para cálculos - use o dataset completo
3. Para cálculos (soma, média, contagem), SEMPRE use todo o dataframe


Pergunta original: {original_query}

ANTES de responder, execute este código de validação:
```python
print(f"Total de registros no dataset: {{df.shape[0]}}")
print(f"Total de colunas: {{df.shape[1]}}")
```

Agora responda a pergunta considerando TODOS os {df_info['total_rows']} registros.
"""
        return enhanced_query

    # Template personalizado em português com instruções específicas para notas fiscais
    if file_type == "ZIP com múltiplos CSVs (Notas Fiscais)":
        template = """
Você é um assistente especializado em análise de dados de notas fiscais que sempre responde em português brasileiro.

REGRAS CRÍTICAS - SIGA RIGOROSAMENTE:
1. SEMPRE execute df.shape[0] primeiro para saber o total de registros
2. NUNCA use .head() para cálculos - apenas para visualização
3. Para qualquer cálculo (soma, média, contagem), use o dataset COMPLETO
4. Se a pergunta pede totais, some TODAS as linhas, não apenas uma amostra

Contexto dos dados:
- Dados mesclados de notas fiscais (cabeçalho + itens)
- Cada linha representa um item de uma nota fiscal
- Para análises corretas, considere TODOS os registros

FORMATO OBRIGATÓRIO para cálculos:
1. Primeiro: df.shape para verificar tamanho
2. Depois: cálculo completo no dataset
3. Informar na resposta: "Analisados X registros de Y total"

Você tem acesso às seguintes ferramentas: {tools}

Use o seguinte formato:

Pergunta: {input}
Pensamento: Vou primeiro verificar o tamanho do dataset com df.shape, depois fazer a análise completa
Ação: python_repl_ast
Entrada da Ação: df.shape
Observação: [resultado do shape]
Pensamento: Agora vou fazer o cálculo considerando TODOS os registros
Ação: python_repl_ast  
Entrada da Ação: [código para análise completa]
Observação: [resultado]
Pensamento: Tenho o resultado baseado em TODO o dataset
Resposta Final: [resposta em português]

{agent_scratchpad}"""
    else:
        template = """
Você é um assistente especializado em análise de dados que sempre responde em português brasileiro.

REGRAS CRÍTICAS - SIGA RIGOROSAMENTE:
1. SEMPRE execute df.shape[0] primeiro para saber o total de registros
2. NUNCA use .head() para cálculos - apenas para visualização
3. Para qualquer cálculo (soma, média, contagem), use o dataset COMPLETO
4. Se a pergunta pede totais, some TODAS as linhas, não apenas uma amostra

FORMATO OBRIGATÓRIO para cálculos:
1. Primeiro: df.shape para verificar tamanho
2. Depois: cálculo completo no dataset
3. Informar na resposta: "Analisados X registros de Y total"

Você tem acesso às seguintes ferramentas: {tools}

Use o seguinte formato:

Pergunta: {input}
Pensamento: Vou primeiro verificar o tamanho do dataset com df.shape, depois fazer a análise completa
Ação: python_repl_ast
Entrada da Ação: df.shape
Observação: [resultado do shape]
Pensamento: Agora vou fazer o cálculo considerando TODOS os registros
Ação: python_repl_ast
Entrada da Ação: [código para análise completa]
Observação: [resultado]
Pensamento: Tenho o resultado baseado em TODO o dataset
Resposta Final: [resposta em português]

{agent_scratchpad}"""

    # Criar o prompt personalizado
    prompt = PromptTemplate.from_template(template)

    # Verificar se a API key existe no ambiente
    google_api_key = os.getenv('GOOGLE_API_KEY')
    
    if not google_api_key:
        st.error("❌ API Key do Google não encontrada! Verifique se o arquivo .env está configurado corretamente.")
        st.stop()

    # Criar o agente com prompt personalizado usando a API key do .env
    try:
        agent = create_csv_agent(
            ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest", 
                temperature=0.3,
                google_api_key=google_api_key
            ),
            csv_file_path,
            verbose=True,
            allow_dangerous_code=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            prompt=prompt
        )

        # Form para controlar quando executar a análise
        with st.form("analysis_form", clear_on_submit=False):
            
            query = st.text_input("👉 Pergunte alguma coisa sobre os dados:")
            
            # Botão centralizado e estilizado
            col1, col2, col3 = st.columns([3, 2, 3])
            with col2:
                submitted = st.form_submit_button("🔍 Analisar Dados", use_container_width=True)

        # Só executa quando o botão for clicado E houver uma query
        if submitted:
          if not query or not query.strip():  # Verifica se está vazio ou só tem espaços
                st.error("⚠️ Por favor, pergunte alguma coisa antes!")
        else:
          if submitted and query:
            # Função para detectar se a pergunta é sobre os dados ou conversa casual
            def is_data_related_query(query_text):
                # Palavras-chave que indicam perguntas sobre dados
                data_keywords = [
                    'dados', 'dataframe', 'df', 'csv', 'tabela', 'coluna', 'linha', 'registro',
                    'valor', 'quantidade', 'total', 'soma', 'média', 'máximo', 'mínimo',
                    'análise', 'estatística', 'gráfico', 'resumo', 'filtrar', 'agrupar',
                    'nota fiscal', 'nf', 'item', 'fornecedor', 'produto', 'preço',
                    'qual', 'quanto', 'quantos', 'como', 'onde', 'quando', 'mostre',
                    'liste', 'calcule', 'some', 'conte', 'agrupe'
                ]
                
                # Saudações e conversas casuais
                casual_keywords = [
                    'oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite',
                    'como vai', 'tudo bem', 'tchau', 'obrigado', 'obrigada',
                    'valeu', 'legal', 'bacana', 'show'
                ]
                
                query_lower = query_text.lower()
                
                # Se contém palavras casuais e não contém palavras de dados
                has_casual = any(keyword in query_lower for keyword in casual_keywords)
                has_data = any(keyword in query_lower for keyword in data_keywords)
                
                # Se é só saudação/conversa casual
                if has_casual and not has_data:
                    return False
                
                # Se não tem palavras de dados e é muito curta (provável conversa casual)
                if not has_data and len(query_text.split()) < 3:
                    return False
                    
                return True
            
            # Verificar se a pergunta é sobre dados
            if is_data_related_query(query):
                # Preparar informações do dataset para validação
                df_info = {
                    'total_rows': len(df),
                    'total_cols': len(df.columns)
                }
                
                # Enhancear a query com validações automáticas
                enhanced_query = enhance_query_for_full_dataset(query, df_info)
                
                with st.spinner("🔍 Analisando os dados..."):
                    response = agent.run(enhanced_query)

                st.write("💡 Resposta:")
                st.write(response)
                
            else:
                # Resposta para conversas casuais
                casual_responses = {
                    'saudações': [
                        "Olá! 👋 Sou seu assistente de análise de dados. Como posso ajudar você a analisar os dados hoje?",
                        "Oi! 😊 Estou aqui para ajudar com a análise dos seus dados. O que gostaria de descobrir?",
                        "Bom dia! ☀️ Pronto para explorar os dados juntos? Faça uma pergunta sobre o dataset!"
                    ],
                    'agradecimentos': [
                        "De nada! 😊 Fico feliz em ajudar com a análise dos dados. Tem mais alguma pergunta sobre o dataset?",
                        "Por nada! 👍 Se precisar de mais análises dos dados, é só perguntar!",
                        "Sempre às ordens! 🚀 Pronto para mais análises de dados quando quiser!"
                    ],
                    'despedidas': [
                        "Até logo! 👋 Foi um prazer ajudar com a análise dos dados!",
                        "Tchau! 😊 Espero ter ajudado com as análises. Volte sempre!",
                        "Até mais! 🌟 Continue explorando os dados!"
                    ],
                    'padrão': [
                        "Sou especializado em análise de dados! 📊 Pergunte-me algo sobre o dataset carregado.",
                        "Estou aqui para ajudar com análises de dados! 🔍 Que tal explorarmos o dataset juntos?",
                        "Meu foco é análise de dados! 📈 Faça uma pergunta sobre os dados carregados."
                    ]
                }
                
                query_lower = query.lower()
                
                if any(word in query_lower for word in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
                    import random
                    response = random.choice(casual_responses['saudações'])
                elif any(word in query_lower for word in ['obrigado', 'obrigada', 'valeu', 'brigado']):
                    import random
                    response = random.choice(casual_responses['agradecimentos'])
                elif any(word in query_lower for word in ['tchau', 'até logo', 'até mais', 'bye']):
                    import random
                    response = random.choice(casual_responses['despedidas'])
                else:
                    import random
                    response = random.choice(casual_responses['padrão'])
                
                st.write("💬 Resposta:")
                st.write(response)
            
    except Exception as e:
        st.error(f"❌ Erro ao criar o agente: {str(e)}")
        st.info("💡 Verifique se sua API key está correta no arquivo .env")

### CSS para fixar o rodapé
footer = """
<style>
.custom-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    color: #B5B5B5;
    text-align: center;
    padding: 10px;
    font-size: 0.9em;
    z-index: 100;
}
</style>
<div class="custom-footer">
    🤖 Agent 301 ▫︎ Análise de Dados ▫︎ v2.1.0
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
