import google.generativeai as genai


genai.configure(api_key="SUA API KEY")

print(" Buscando modelos disponíveis para esta chave...\n")


for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f" NOME EXATO: {m.name}")