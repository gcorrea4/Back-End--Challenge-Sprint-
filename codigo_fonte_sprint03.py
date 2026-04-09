import json
import os

ARQUIVO_DADOS = "dados.json"

pacientes = []
dentistas = []
consultas_agendadas = []

# PERSISTÊNCIA DOS DADOS

def salvar_dados():
    dados = {
        "pacientes": pacientes,
        "dentistas": dentistas,
        "consultas_agendadas": consultas_agendadas
    }
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"❌ Erro ao salvar dados: {e}")


def carregar_dados():
    """Carrega os dados do arquivo JSON para as listas globais."""
    global pacientes, dentistas, consultas_agendadas
    if not os.path.exists(ARQUIVO_DADOS):
        return  # Primeira execução, sem arquivo ainda
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            pacientes = dados.get("pacientes", [])
            dentistas = dados.get("dentistas", [])
            consultas_agendadas = dados.get("consultas_agendadas", [])
        print("✅ Dados carregados com sucesso.\n")
    except (IOError, json.JSONDecodeError) as e:
        print(f" Erro ao carregar dados: {e}. Iniciando com dados vazios.\n")


# FUNÇÕES AUXILIARES DE VALIDAÇÃO

def obter_inteiro(mensagem):
    """Vai garantir que a entrada do usuário é um número inteiro válido."""
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print(" Entrada inválida. Por favor, digite um número inteiro.")

def obter_float(mensagem):
    """Garante que a entrada do usuário é um número decimal válido."""
    while True:
        try:
            entrada = input(mensagem).replace(',', '.')
            valor = float(entrada)
            return valor
        except ValueError:
            print(" Entrada inválida. Por favor, digite um número (Ex: 1 ou 1.5).")


def obter_tipo_dor(mensagem):
    """Valida e retorna o tipo de dor informado."""
    while True:
        tipo_dor = input(mensagem).lower()
        if tipo_dor in ["leve", "forte", "dente quebrado"]:
            return tipo_dor
        print(" Tipo de dor inválido. Escolha entre 'leve', 'forte' ou 'dente quebrado'.")


def obter_especialidade(mensagem):
    """Valida e retorna a especialidade informada."""
    especialidades_validas = ["prótese", "ortodontia", "odontopediatria", "clínico geral", "cirurgia", "endodontia"]
    while True:
        especialidade = input(mensagem).lower()
        if especialidade in especialidades_validas:
            return especialidade
        print(f" Especialidade inválida. Opções: {', '.join(especialidades_validas)}")


def calcular_urgencia(tipo_dor, tempo_dor, renda):
    """Calcula e retorna o nível de urgência do paciente."""
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

# ALGORITMO DE MATCH

def encontrar_melhor_dentista(paciente):
    """Encontra o dentista mais compatível e disponível para um paciente."""
    compatibilidade = {
        "leve": ["clínico geral", "odontopediatria"],
        "forte": ["endodontia", "clínico geral"],
        "dente quebrado": ["prótese", "cirurgia"]
    }
    melhor_dentista = None
    maior_pontuacao = -1

    for d in dentistas:
        if d["atendidos"] >= d["max_pacientes"]:
            continue
        pontos = 0
        if d["especialidade"] in compatibilidade.get(paciente["tipo_dor"], []):
            pontos += 2
        if d["bairro"].lower() == paciente["bairro"].lower():
            pontos += 3
        if paciente["urgencia"] >= 5:
            pontos += 5
        if pontos > maior_pontuacao:
            maior_pontuacao = pontos
            melhor_dentista = d
        elif pontos == maior_pontuacao and melhor_dentista and d["atendidos"] < melhor_dentista["atendidos"]:
            melhor_dentista = d

    return melhor_dentista, maior_pontuacao

# CRUD — PACIENTES

def cadastrar_paciente():
    """Cadastra um novo paciente."""
    print("\n--- 🦷 Cadastrar Paciente ---")
    nome = input("Nome do paciente: ").strip()
    if not nome:
        print(" Nome não pode ser vazio.")
        return

    idade = obter_inteiro("Idade: ")
    tipo_dor = obter_tipo_dor("Tipo de dor (leve/forte/dente quebrado): ")
    tempo_dor = obter_inteiro("Há quanto tempo sente a dor (dias): ")
    renda = obter_float("Renda familiar (em salários mínimos): ")
    bairro = input("Bairro/Cidade: ").strip()
    urgencia = calcular_urgencia(tipo_dor, tempo_dor, renda)

    paciente = {
        "nome": nome,
        "idade": idade,
        "tipo_dor": tipo_dor,
        "tempo_dor": tempo_dor,
        "renda": renda,
        "bairro": bairro,
        "urgencia": urgencia
    }
    pacientes.append(paciente)
    salvar_dados()
    print(f"\n Paciente '{nome}' cadastrado com urgência {urgencia}.\n")


def listar_pacientes():
    """Lista todos os pacientes cadastrados."""
    print("\n---  Lista de Pacientes ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    for i, p in enumerate(pacientes):
        print(f"[{i + 1}] Nome: {p['nome']}, Idade: {p['idade']} anos")
        print(f"    Bairro: {p['bairro']}, Renda: {p['renda']} Sal. Mín.")
        print(f"    Dor: {p['tipo_dor']} há {p['tempo_dor']} dias | Urgência: {p['urgencia']}")
        print("-" * 35)
    print(f"Total: {len(pacientes)} paciente(s).\n")


def consultar_paciente():
    """Busca um paciente pelo nome."""
    print("\n--- 🔍 Consultar Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    termo = input("Digite o nome (ou parte do nome) do paciente: ").strip().lower()
    resultados = [p for p in pacientes if termo in p["nome"].lower()]
    if not resultados:
        print("⚠️ Nenhum paciente encontrado com esse nome.\n")
        return
    print(f"\n{len(resultados)} resultado(s) encontrado(s):")
    for p in resultados:
        print(f"  • {p['nome']} | Idade: {p['idade']} | Bairro: {p['bairro']} | Urgência: {p['urgencia']}")
    print()


def editar_paciente():
    """Edita os dados de um paciente existente."""
    print("\n--- ✏ Editar Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    listar_pacientes()
    while True:
        escolha = obter_inteiro("Número do paciente a editar (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(pacientes):
            break
        print(" Número inválido. Tente novamente.")

    p = pacientes[escolha]
    print(f"\nEditando: {p['nome']} (pressione Enter para manter o valor atual)\n")

    nome = input(f"Nome [{p['nome']}]: ").strip()
    if nome:
        p["nome"] = nome

    entrada_idade = input(f"Idade [{p['idade']}]: ").strip()
    if entrada_idade:
        try:
            p["idade"] = int(entrada_idade)
        except ValueError:
            print(" Idade inválida, mantendo valor anterior.")

    print(f"Tipo de dor atual: {p['tipo_dor']}")
    nova_dor = input("Novo tipo de dor (leve/forte/dente quebrado) ou Enter para manter: ").strip().lower()
    if nova_dor in ["leve", "forte", "dente quebrado"]:
        p["tipo_dor"] = nova_dor

    entrada_tempo = input(f"Tempo de dor em dias [{p['tempo_dor']}]: ").strip()
    if entrada_tempo:
        try:
            p["tempo_dor"] = int(entrada_tempo)
        except ValueError:
            print(" Valor inválido, mantendo anterior.")

    entrada_renda = input(f"Renda [{p['renda']}]: ").strip().replace(',', '.')
    if entrada_renda:
        try:
            p["renda"] = float(entrada_renda)
        except ValueError:
            print(" Valor inválido, mantendo anterior.")

    bairro = input(f"Bairro [{p['bairro']}]: ").strip()
    if bairro:
        p["bairro"] = bairro

    p["urgencia"] = calcular_urgencia(p["tipo_dor"], p["tempo_dor"], p["renda"])
    salvar_dados()
    print(f"\n Paciente '{p['nome']}' atualizado com sucesso. Nova urgência: {p['urgencia']}.\n")


def excluir_paciente():
    """Remove um paciente da lista."""
    print("\n--- 🗑️ Excluir Paciente ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    listar_pacientes()
    while True:
        escolha = obter_inteiro("Número do paciente a excluir (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(pacientes):
            break
        print(" Número inválido. Tente novamente.")

    nome = pacientes[escolha]["nome"]
    confirmacao = input(f"Tem certeza que deseja excluir '{nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        pacientes.pop(escolha)
        salvar_dados()
        print(f"\n Paciente '{nome}' excluído com sucesso.\n")
    else:
        print(" Exclusão cancelada.\n")

# CRUD — DENTISTAS

def cadastrar_dentista():
    """Cadastra um novo dentista voluntário."""
    print("\n Cadastrar Dentista ")
    nome = input("Nome do dentista: ").strip()
    if not nome:
        print(" Nome não pode ser vazio.")
        return

    especialidade = obter_especialidade(
        "Especialidade (prótese/ortodontia/odontopediatria/clínico geral/cirurgia/endodontia): "
    )
    bairro = input("Bairro/Cidade: ").strip()
    max_pacientes = obter_inteiro("Número máximo de pacientes por mês: ")

    dentista = {
        "nome": nome,
        "especialidade": especialidade,
        "bairro": bairro,
        "max_pacientes": max_pacientes,
        "atendidos": 0
    }
    dentistas.append(dentista)
    salvar_dados()
    print(f"\nDentista '{nome}' cadastrado.\n")


def listar_dentistas():
    """Lista todos os dentistas cadastrados."""
    print("\n--- 🧑‍⚕️ Lista de Dentistas ---")
    if not dentistas:
        print("Nenhum dentista cadastrado.\n")
        return
    for i, d in enumerate(dentistas):
        print(f"[{i + 1}] Nome: {d['nome']} | Especialidade: {d['especialidade']}")
        print(f"    Bairro: {d['bairro']} | Atendidos: {d['atendidos']}/{d['max_pacientes']}")
        print("-" * 35)
    print(f"Total: {len(dentistas)} dentista(s).\n")


def consultar_dentista():
    """Busca um dentista pelo nome ou especialidade."""
    print("\n--- 🔍 Consultar Dentista ---")
    if not dentistas:
        print("Nenhum dentista cadastrado.\n")
        return
    print("Buscar por:\n1. Nome\n2. Especialidade")
    opcao = obter_inteiro("Escolha: ")
    if opcao == 1:
        termo = input("Digite o nome (ou parte): ").strip().lower()
        resultados = [d for d in dentistas if termo in d["nome"].lower()]
    elif opcao == 2:
        termo = input("Digite a especialidade: ").strip().lower()
        resultados = [d for d in dentistas if termo in d["especialidade"].lower()]
    else:
        print(" Opção inválida.\n")
        return

    if not resultados:
        print(" Nenhum dentista encontrado.\n")
        return
    print(f"\n{len(resultados)} resultado(s):")
    for d in resultados:
        disponivel = d["max_pacientes"] - d["atendidos"]
        print(f"  • {d['nome']} | {d['especialidade']} | {d['bairro']} | Vagas: {disponivel}")
    print()


def editar_dentista():
    """Edita os dados de um dentista existente."""
    print("\n---  Editar Dentista ---")
    if not dentistas:
        print("Nenhum dentista cadastrado.\n")
        return
    listar_dentistas()
    while True:
        escolha = obter_inteiro("Número do dentista a editar (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(dentistas):
            break
        print(" Número inválido. Tente novamente.")

    d = dentistas[escolha]
    print(f"\nEditando: {d['nome']} (pressione Enter para manter o valor atual)\n")

    nome = input(f"Nome [{d['nome']}]: ").strip()
    if nome:
        d["nome"] = nome

    print(f"Especialidade atual: {d['especialidade']}")
    nova_esp = input("Nova especialidade ou Enter para manter: ").strip().lower()
    if nova_esp in ["prótese", "ortodontia", "odontopediatria", "clínico geral", "cirurgia", "endodontia"]:
        d["especialidade"] = nova_esp
    elif nova_esp:
        print(" Especialidade inválida, mantendo anterior.")

    bairro = input(f"Bairro [{d['bairro']}]: ").strip()
    if bairro:
        d["bairro"] = bairro

    entrada_max = input(f"Máximo de pacientes [{d['max_pacientes']}]: ").strip()
    if entrada_max:
        try:
            d["max_pacientes"] = int(entrada_max)
        except ValueError:
            print(" Valor inválido, mantendo anterior.")

    salvar_dados()
    print(f"\n Dentista '{d['nome']}' atualizado com sucesso.\n")


def excluir_dentista():
    """Remove um dentista da lista."""
    print("\n--- ️ Excluir Dentista ---")
    if not dentistas:
        print("Nenhum dentista cadastrado.\n")
        return
    listar_dentistas()
    while True:
        escolha = obter_inteiro("Número do dentista a excluir (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(dentistas):
            break
        print(" Número inválido. Tente novamente.")

    nome = dentistas[escolha]["nome"]
    confirmacao = input(f"Tem certeza que deseja excluir '{nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        dentistas.pop(escolha)
        salvar_dados()
        print(f"\n✅ Dentista '{nome}' excluído com sucesso.\n")
    else:
        print(" Exclusão cancelada.\n")



# FUNCIONALIDADES DE MATCH E CONSULTAS

def match_paciente_dentista():
    """Realiza o match entre paciente e dentista."""
    print("\n Match Paciente ↔ Dentista ")
    if not pacientes or not dentistas:
        print("Cadastre pelo menos um paciente e um dentista primeiro.\n")
        return

    listar_pacientes()
    while True:
        escolha = obter_inteiro("Escolha o número do paciente: ") - 1
        if 0 <= escolha < len(pacientes):
            break
        print(" Número de paciente inválido. Tente novamente.")

    paciente = pacientes[escolha]
    melhor_dentista, maior_pontuacao = encontrar_melhor_dentista(paciente)

    if melhor_dentista and maior_pontuacao > 0:
        melhor_dentista["atendidos"] += 1
        salvar_dados()
        print(f"\n Paciente '{paciente['nome']}' (Urgência: {paciente['urgencia']}) "
              f"combinado com '{melhor_dentista['nome']}' (Pontuação: {maior_pontuacao}).\n")
    else:
        print("⚠️ Nenhum dentista disponível e compatível no momento.\n")


def agendar_consulta():
    """Agendamento de consulta com match automático."""
    print("\n Agendar Consulta ")
    if not pacientes:
        print("Cadastre um paciente primeiro.\n")
        return

    listar_pacientes()
    while True:
        escolha = obter_inteiro("Número do paciente para agendar (0 para cancelar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(pacientes):
            break
        print(" Número inválido. Tente novamente.")

    paciente = pacientes[escolha]
    data = input("Data da consulta (DD/MM/AAAA): ").strip()
    hora = input("Hora da consulta (HH:MM): ").strip()

    dentista_nome_input = input("Nome do dentista (ou Enter para Match automático): ").strip()

    if not dentista_nome_input:
        print("Iniciando Match automático...")
        if not dentistas:
            print("⚠️ Nenhum dentista cadastrado.")
            dentista_final = "Aguardando Dentista"
        else:
            melhor_dentista, pontuacao = encontrar_melhor_dentista(paciente)
            if melhor_dentista and pontuacao > 0:
                melhor_dentista["atendidos"] += 1
                dentista_final = melhor_dentista["nome"]
                print(f"✅ Match realizado! Dentista: {dentista_final} (Pontuação: {pontuacao}).")
            else:
                dentista_final = "Aguardando Match"
                print("⚠️ Nenhum dentista compatível encontrado.")
    else:
        dentista_final = dentista_nome_input

    consulta = {
        "paciente": paciente["nome"],
        "data": data,
        "hora": hora,
        "dentista": dentista_final
    }
    consultas_agendadas.append(consulta)
    salvar_dados()
    print(f"\n✅ Consulta agendada para '{paciente['nome']}' em {data} às {hora}. Dentista: {dentista_final}.\n")


def listar_consultas():
    """Lista todas as consultas agendadas."""
    print("\n--- 📄 Consultas Agendadas ---")
    if not consultas_agendadas:
        print("Nenhuma consulta agendada.\n")
        return
    for i, c in enumerate(consultas_agendadas):
        print(f"[{i + 1}] Paciente: {c['paciente']}")
        print(f"    Data/Hora: {c['data']} às {c['hora']}")
        print(f"    Dentista: {c['dentista']}")
        print("-" * 35)
    print(f"Total: {len(consultas_agendadas)} consulta(s).\n")


def excluir_consulta():
    """Remove uma consulta agendada."""
    print("\n Cancelar Consulta ")
    if not consultas_agendadas:
        print("Nenhuma consulta agendada.\n")
        return
    listar_consultas()
    while True:
        escolha = obter_inteiro("Número da consulta a cancelar (0 para voltar): ") - 1
        if escolha == -1:
            return
        if 0 <= escolha < len(consultas_agendadas):
            break
        print(" Número inválido.")

    c = consultas_agendadas[escolha]
    confirmacao = input(f"Cancelar consulta de '{c['paciente']}' em {c['data']}? (s/n): ").strip().lower()
    if confirmacao == "s":
        consultas_agendadas.pop(escolha)
        salvar_dados()
        print(" Consulta cancelada com sucesso.\n")
    else:
        print(" Cancelamento abortado.\n")

# MENUS

def menu_pacientes():
    """Submenu de CRUD para pacientes."""
    while True:
        print("\n===  Gerenciar Pacientes ===")
        print("1. Cadastrar paciente")
        print("2. Listar pacientes")
        print("3. Consultar paciente por nome")
        print("4. Editar paciente")
        print("5. Excluir paciente")
        print("0. Voltar ao menu principal")
        print("-" * 30)
        opcao = obter_inteiro("Escolha uma opção: ")
        if opcao == 1:
            cadastrar_paciente()
        elif opcao == 2:
            listar_pacientes()
        elif opcao == 3:
            consultar_paciente()
        elif opcao == 4:
            editar_paciente()
        elif opcao == 5:
            excluir_paciente()
        elif opcao == 0:
            break
        else:
            print(" Opção inválida.\n")


def menu_dentistas():
    """Submenu de CRUD para dentistas."""
    while True:
        print("\n===  Gerenciar Dentistas ===")
        print("1. Cadastrar dentista")
        print("2. Listar dentistas")
        print("3. Consultar dentista")
        print("4. Editar dentista")
        print("5. Excluir dentista")
        print("0. Voltar ao menu principal")
        print("-" * 30)
        opcao = obter_inteiro("Escolha uma opção: ")
        if opcao == 1:
            cadastrar_dentista()
        elif opcao == 2:
            listar_dentistas()
        elif opcao == 3:
            consultar_dentista()
        elif opcao == 4:
            editar_dentista()
        elif opcao == 5:
            excluir_dentista()
        elif opcao == 0:
            break
        else:
            print(" Opção inválida.\n")


def menu_consultas():
    """Submenu para agendamentos."""
    while True:
        print("\n Gerenciar Consultas ")
        print("1. Agendar consulta")
        print("2. Listar consultas")
        print("3. Cancelar consulta")
        print("0. Voltar ao menu principal")
        print("-" * 30)
        opcao = obter_inteiro("Escolha uma opção: ")
        if opcao == 1:
            agendar_consulta()
        elif opcao == 2:
            listar_consultas()
        elif opcao == 3:
            excluir_consulta()
        elif opcao == 0:
            break
        else:
            print(" Opção inválida.\n")


def menu():
    """Menu principal do sistema."""
    carregar_dados()
    while True:
        print("=" * 40)
        print("    DENTISTA NA NUVEM — Sprint 3  ")
        print("=" * 40)
        print("1.  Gerenciar Pacientes")
        print("2.   Gerenciar Dentistas")
        print("3.  Match Paciente ↔ Dentista")
        print("4.  Gerenciar Consultas")
        print("0.  Sair")
        print("-" * 40)
        opcao = obter_inteiro("Escolha uma opção: ")

        if opcao == 1:
            menu_pacientes()
        elif opcao == 2:
            menu_dentistas()
        elif opcao == 3:
            match_paciente_dentista()
        elif opcao == 4:
            menu_consultas()
        elif opcao == 0:
            print("\nEncerrando... Obrigado por usar o Dentista na Nuvem! \n")
            break
        else:
            print(" Opção inválida. Tente novamente.\n")

# EXECUÇÃO
menu()
