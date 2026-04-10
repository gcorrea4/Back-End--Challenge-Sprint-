# Turma do Bem - API de Triagem (Back-End)

Este é o motor do projeto, responsável pelo cálculo de urgência dos pacientes, pela integração com a Inteligência Artificial (Google Gemini) e pela persistência de dados do sistema.

---

## 🔗 Conexão com o Front-End

Este repositório contém apenas a API (servidor). Para utilizar a interface completa e visualizar o dashboard, este projeto deve ser executado em conjunto com o repositório do Front-End.

**Repositório do Front-End:** [https://github.com/gcorrea4/Challenge-Sprint](https://github.com/gcorrea4/Challenge-Sprint)

---

## ⚙️ Pré-requisitos

O sistema exige o ambiente Python configurado. Caso não possua, siga as etapas abaixo:

1. **Instalação do Python:** Acesse [python.org](https://www.python.org/) e realize o download da versão estável. 
   > **Importante:** Durante a instalação no Windows, marque a caixa **"Add Python to PATH"** para evitar erros de execução no terminal.

2. **Instalação de Dependências:** Após instalar o Python, abra o terminal do seu computador (CMD, PowerShell ou o terminal do VS Code) e execute o comando abaixo para instalar todas as bibliotecas necessárias para a API e para a Inteligência Artificial:

   ```bash
   pip install fastapi uvicorn pydantic google-generativeai
