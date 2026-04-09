from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Configuração de CORS para permitir que o React (porta 5173) acesse o Python (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARQUIVO_DADOS = "dados.json"

# Modelo de dados baseado na função cadastrar_paciente do colega
class Paciente(BaseModel):
    nome: str
    idade: int
    tipo_dor: str
    tempo_dor: int
    renda: float
    bairro: str

# Lógica de Urgência original
def calcular_urgencia(tipo_dor, tempo_dor, renda):
    urgencia = 0
    if tipo_dor == "forte":
        urgencia += 3
    elif tipo_dor == "dente quebrado":
        urgencia += 4
    else:
        urgencia += 1
    
    if tempo_dor > 7:
        urgencia += 2
    if renda <= 2:
        urgencia += 1
    return urgencia

# Função para salvar no JSON mantendo a estrutura do projeto
def salvar_paciente_no_json(paciente_data):
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            try:
                conteudo = json.load(f)
            except:
                conteudo = {"pacientes": [], "dentistas": [], "consultas_agendadas": []}
    else:
        conteudo = {"pacientes": [], "dentistas": [], "consultas_agendadas": []}

    conteudo["pacientes"].append(paciente_data)
    
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, ensure_ascii=False, indent=4)

@app.post("/cadastrar-paciente")
async def api_cadastrar_paciente(p: Paciente):
    # Executa o algoritmo de urgência
    urgencia_final = calcular_urgencia(p.tipo_dor, p.tempo_dor, p.renda)
    
    # Prepara o dicionário para salvar
    novo_p = p.dict()
    novo_p["urgencia"] = urgencia_final
    
    # Salva no arquivo JSON
    salvar_paciente_no_json(novo_p)
    
    print(f"✅ Paciente {p.nome} salvo com urgência {urgencia_final}")
    return {"status": "sucesso", "urgencia": urgencia_final}

@app.get("/pacientes")
async def listar_pacientes():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            # Retorna a lista de pacientes (ou lista vazia se não houver nenhum)
            return dados.get("pacientes", [])
    return []

class LoginSchema(BaseModel):
    usuario: str
    senha: str

@app.post("/login")
async def login(auth: LoginSchema):
    # Simulação de base de dados
    if auth.usuario == "dentista" and auth.senha == "123":
        return {"status": "sucesso", "role": "dentista", "nome": "Dr. Gabriel"}
    
    if auth.usuario == "paciente" and auth.senha == "123":
        return {"status": "sucesso", "role": "paciente", "nome": "Paciente Teste"}
    
    return {"status": "erro", "message": "Usuário ou senha incorretos"}

# Adicione isso no final do seu main.py
@app.delete("/paciente/{nome}")
async def concluir_atendimento(nome: str):
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        # Filtra a lista mantendo apenas quem NÃO tem o nome escolhido
        dados["pacientes"] = [p for p in dados.get("pacientes", []) if p["nome"] != nome]
        
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        return {"status": "sucesso", "mensagem": f"Atendimento de {nome} concluído."}
    return {"status": "erro", "mensagem": "Arquivo de dados não encontrado."}