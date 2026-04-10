import warnings
# ISSO AQUI CALA A BOCA DO TERMINAL E ESCONDE O AVISO VERMELHO
warnings.filterwarnings("ignore") 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import google.generativeai as genai # Usando a versão estável

# 1. CRIA O APP PRIMEIRO (Evita o NameError)
app = FastAPI()

# 2. CONFIGURA O CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. VARIÁVEIS GLOBAIS E CONFIGURAÇÃO DA IA
ARQUIVO_DADOS = "dados.json"

# Configuração da IA (Versão antiga e estável)
genai.configure(api_key="AIzaSyCxibJ_weiL2zcgGjk2A7PMtkM7JdZzNjo")
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. MODELOS DE DADOS
class Paciente(BaseModel):
    nome: str
    idade: int
    tipo_dor: str
    tempo_dor: int
    renda: float
    bairro: str

class LoginSchema(BaseModel):
    usuario: str
    senha: str

class PerguntaIA(BaseModel):
    texto: str

# 5. FUNÇÕES DE LÓGICA
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


# ==========================================
# 6. ROTAS DA API
# ==========================================

@app.post("/cadastrar-paciente")
async def api_cadastrar_paciente(p: Paciente):
    urgencia_final = calcular_urgencia(p.tipo_dor, p.tempo_dor, p.renda)
    novo_p = p.dict()
    novo_p["urgencia"] = urgencia_final
    salvar_paciente_no_json(novo_p)
    return {"status": "sucesso", "urgencia": urgencia_final}

@app.get("/pacientes")
async def listar_pacientes():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("pacientes", [])
    return []

@app.post("/login")
async def login(auth: LoginSchema):
    if auth.usuario == "dentista" and auth.senha == "123":
        return {"status": "sucesso", "role": "dentista", "nome": "Dr. Gabriel"}
    if auth.usuario == "paciente" and auth.senha == "123":
        return {"status": "sucesso", "role": "paciente", "nome": "Paciente Teste"}
    return {"status": "erro", "message": "Usuário ou senha incorretos"}

@app.delete("/paciente/{nome}")
async def concluir_atendimento(nome: str):
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        dados["pacientes"] = [p for p in dados.get("pacientes", []) if p["nome"] != nome]
        
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        return {"status": "sucesso", "mensagem": f"Atendimento de {nome} concluído."}
    return {"status": "erro", "mensagem": "Arquivo não encontrado."}

@app.post("/IA/consultar")
async def consultar_ia(pergunta: PerguntaIA):
    try:
        if os.path.exists(ARQUIVO_DADOS):
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados_json = f.read()
        else:
            dados_json = '{"pacientes": []}'
        
        prompt = f"""
        Você é o 'Assistente de Dados da Turma do Bem'. Seu público-alvo são DENTISTAS voluntários.
        Seu objetivo é analisar os dados dos pacientes abaixo e responder perguntas técnicas e diretas.
        
        REGRAS:
        1. Analise o campo 'urgencia' para prioridades.
        2. Seja profissional e objetivo.
        3. Se não houver dados, diga que a fila está vazia.
        4. NÃO invente informações. Use apenas o JSON fornecido.

        DADOS ATUAIS (JSON):
        {dados_json}

        PERGUNTA DO DENTISTA: {pergunta.texto}
        """
        
        response = model.generate_content(prompt)
        return {"resposta": response.text}
    except Exception as e:
        return {"resposta": f"Erro na IA: {str(e)}"}