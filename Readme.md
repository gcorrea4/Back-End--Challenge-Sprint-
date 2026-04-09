---

## Conexão com o Front-End

Este repositório contém apenas a API (servidor). Para utilizar a interface completa e visualizar o dashboard, este projeto deve ser executado em conjunto com o repositório do Front-End.

**Repositório do Front-End:** [https://github.com/gcorrea4/Challenge-Sprint]

---

# Turma do Bem - API de Triagem (Back-End)

Este é o motor do projeto, responsável pelo cálculo de urgência dos pacientes e pela persistência de dados do sistema.

---

## Pre-requisitos

O sistema exige o ambiente Python configurado. Caso não possua, siga as etapas abaixo:

1. Instalação do Python: Acesse python.org e realize o download da versão estável. 
   Importante: Durante a instalação, ative a opção "Add Python to PATH" para evitar erros de execução no terminal.

2. Instalação de dependências: Após instalar o Python, execute o comando abaixo no terminal (CMD ou PowerShell) para instalar as bibliotecas necessárias:
   ```bash
   pip install fastapi uvicorn pydantic


  -- Instruções para Execução --

Abra a pasta do projeto no VS Code.

Acesse um novo terminal dentro do ambiente.

Comando de inicialização: Utilize o comando abaixo para rodar o servidor (ajustado para o caminho padrão de instalação no Windows):

 -- CMD -- ( Funciona melhor no CMD padrão do windows )

C:\Users\gabri\AppData\Local\Python\bin\python.exe -m uvicorn main:app --reload


O sistema estará ativo quando a mensagem "Application startup complete" for exibida.



 -- Funcionalidades da API --
Cálculo de Urgência: Processa os dados de cadastro e define a prioridade (Alta, Média ou Baixa) com base nos critérios de dor e renda.

Persistência de Dados: As informações são armazenadas localmente no arquivo dados.json. Caso o arquivo seja removido, a base de dados será resetada.

Controle de Acesso: Gerencia as permissões entre perfis de Dentista (acesso a prontuários) e Paciente (visualização de impacto social).



 -- Estrutura de Arquivos --
main.py: Lógica central e definição de rotas.

dados.json: Armazenamento dos dados em formato JSON.




Challenge Turma do Bem - FIAP 2026