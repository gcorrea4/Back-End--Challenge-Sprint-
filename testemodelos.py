import google.generativeai as genai

# Configura com a sua chave
genai.configure(api_key="AIzaSyCxibJ_weiL2zcgGjk2A7PMtkM7JdZzNjo")

print("🔍 Buscando modelos disponíveis para esta chave...\n")

# Lista todos os modelos que suportam geração de texto
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ NOME EXATO: {m.name}")