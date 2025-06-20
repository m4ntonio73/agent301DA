# 🤖 Agente Autônomo de Análise de Dados

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agent301.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Uma aplicação web inteligente para análise de dados CSV e Notas Fiscais usando IA generativa com Google Gemini e LangChain.

## 📋 Funcionalidades

- ✅ **Análise de CSV único** - Upload e análise de arquivos CSV simples
- ✅ **Processamento de ZIP** - Extração e mesclagem automática de múltiplos CSVs
- ✅ **Análise de Notas Fiscais** - Processamento especializado de dados fiscais (cabeçalho + itens)
- ✅ **Chat inteligente** - Perguntas em linguagem natural sobre os dados
- ✅ **Validação automática** - Garantia de análise completa do dataset
- ✅ **Interface amigável** - Design responsivo e intuitivo
- ✅ **Limpeza de arquivos** - Gerenciamento automático de arquivos temporários

## 🚀 Demo

![Demo Screenshot](https://via.placeholder.com/800x400?text=Screenshot+da+Aplicação)

*Adicione aqui uma captura de tela da sua aplicação*

## 🛠️ Tecnologias Utilizadas

- **Frontend:** Streamlit
- **IA:** Google Gemini (via LangChain)
- **Processamento:** Pandas, Python
- **Agentes:** LangChain Experimental
- **Deploy:** Streamlit Community Cloud

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Conta Google Cloud com API Gemini habilitada
- Git

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/agente-analise-dados.git
cd agente-analise-dados
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
# Crie um arquivo .env na raiz do projeto
echo "GOOGLE_API_KEY=sua_chave_api_google_aqui" > .env
```

4. **Execute a aplicação:**
```bash
streamlit run app.py
```

5. **Acesse no navegador:**
```
http://localhost:8501
```

## 🔧 Configuração

### Obtendo a API Key do Google

1. Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Adicione no arquivo `.env` como mostrado acima

### Estrutura de Arquivos

```
projeto/
├── app.py               # Aplicação principal
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não commitado)
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Este arquivo
└── temp_data/           # Diretório temporário (criado automaticamente)
```

## 📖 Como Usar

### 1. Análise de CSV Único

1. Selecione "CSV único" no seletor
2. Faça upload do seu arquivo CSV
3. Aguarde o processamento dos dados
4. Faça perguntas sobre os dados no chat

### 2. Análise de Notas Fiscais (ZIP)

1. Selecione "ZIP com múltiplos CSVs"
2. Faça upload do arquivo ZIP contendo:
   - Arquivo de cabeçalho das notas fiscais
   - Arquivo de itens das notas fiscais
3. A aplicação irá:
   - Extrair os arquivos automaticamente
   - Identificar e mesclar os dados
   - Preparar para análise
4. Faça perguntas sobre as notas fiscais

### 3. Exemplos de Perguntas

- "Qual o valor total das notas fiscais?"
- "Quantos itens únicos temos nos dados?"
- "Qual o fornecedor com maior valor de vendas?"
- "Mostre um resumo estatístico dos dados"
- "Agrupe os dados por categoria"

## 🔍 Exemplos de Uso

### Análise Básica
```
Usuário: "Quantos registros temos no total?"
Agente: "O dataset possui 1.250 registros analisados de 1.250 total."
```

### Análise Financeira
```
Usuário: "Qual o valor total das notas fiscais?"
Agente: "Analisando todos os 1.250 registros, o valor total é R$ 2.847.350,75"
```

## 🌐 Deploy

### Streamlit Community Cloud (Recomendado)

1. Faça push do código para um repositório público no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório
5. Adicione `GOOGLE_API_KEY` nos secrets
6. Deploy automático!

### Outras Opções

- **Railway:** Deploy com Docker
- **Heroku:** Plataforma tradicional
- **Google Cloud Run:** Escalabilidade automática
- **AWS EC2:** Controle total

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📋 Roadmap

- [ ] Suporte a Excel (.xlsx)
- [ ] Gráficos e visualizações
- [ ] Exportação de relatórios
- [ ] Análise de dados em tempo real
- [ ] Integração com APIs externas
- [ ] Suporte a múltiplos idiomas

## 🐛 Problemas Conhecidos

- Arquivos muito grandes (>200MB) podem causar timeout
- Alguns formatos de CSV com encoding especial podem apresentar problemas
- Análise de datasets muito complexos pode ser lenta

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Autor:** Seu Nome
- **Email:** seu.email@exemplo.com
- **LinkedIn:** [seu-perfil](https://linkedin.com/in/seu-perfil)
- **GitHub:** [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io) pela incrível framework
- [LangChain](https://langchain.com) pela facilidade de integração com IA
- [Google](https://google.com) pela API Gemini
- Comunidade open source pelos feedbacks e contribuições

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

---

*Desenvolvido com ❤️ para a comunidade de análise de dados*
