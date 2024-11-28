import random

# def listar_exercicios_e_repeticoes():

dados_exemplo = {
    "treino_a": {
        "exercicios_costas": {
            1: "Remada Curvada Pronada",
            2: "Remada Curvada Supinada",
            3: "Barra Fixa",
            4: "Puxada alta",
            5: "Pulldown com corda segure",
            6: "Remada sentado",
            7: "Remada Unilateral (serrote)",
            8: "Remada com Halteres Banco 45º",
        },
        "repeticoes_costas": {
            1: "1x12 2x20 a cada 5 descase 10 segundos",
            2: "4x10",
            3: "3x até a falha",
            4: "Puxada alta",
            5: "2s em baixo 3x15",
            6: "4x10",
            7: "4x10",
            8: "3x12"
        },
        "exercicios_posteriorombro":{
            1: "Peck deck invertido com drop",
            2: "Remada alta Smith",
            3: "Encolhimento trapezio",
            4: "Posterior de ombro no cabo médio",
            5: "Posterior de ombro no banco 45º"
        },
        "repeticoes_posteriorombro": {
            1: "3x15/15",
            2: "3x12",
            3: "4x10",
            4: "4x12",
            5: "1x12 2x20 a cada 5 descanse 10 segundos" 
        },
        "exercicios_posteriorcoxa":{
            1: "Mesa flexora",
            2: "Cadeira flexora",
            3: "stiff",
            4: "Elevação pélvica(pode ser no smith)"
        },
        "repeticoes_posteriorcoxa": {
            1:"4x10",
            2: "3x12",
            3: "3x12",
            4: "3x8 (pesado)"
        }
    },
    "treino_b": {
        "exercicios_quadriceps": {
            1: "Agachamento Livre",
            2: "Leg Press",
            3: "Cadeira extensora",
            4: "Passada",
            5: "Bulgaro com Halter",
            6: "Afundo com Halter"
        },
        "repeticoes_quadriceps": {
            1: "4x10",
            2: "4x12",
            3: "1x20 e 3x12",
            4: "5 min",
            5: "4x10",
            6: "4x15",
            
        },
        "exercicios_panturrilha":{
            1: "Gêmeos em pé"
        },
        "repeticoes_panturrilha": {
            1: "5x12 2s alongando e 2s contraindo"
        },
        "exercicios_adutor": {
            1:"Cadeira Adutora"
        },
        "repeticoes_adutor": {
            1:"1x12 3x20 a cada 5 descase 10s"
        }
    },
    "treino_c": { 
 
        "exercicios_peito": {
            1: "Supino inclinado com halteres ou articulado",
            2: "Supino reto com barra",
            3: "Voador",
            4: "Flexão 60 rep",
            5: "Cross-over declinado",
            6: "Supino inclinado no Cross"
            
            
        },
        "repeticoes_peito": {
            1: "4x12",
            2: "1x15 3x8",
            3: "4x10",
            4: "6x10",
            5: "4x10",
            6:"5x10 2s no pico de contração",
            
        },
        "exercicios_panturrilha": {
            1:"Panturrilha no smith com degrau"
        },
        "repeticoes_panturrilha": {
            1: "5x10 15s de descanso"
        }
    },
    "treino_d": {
        "exercicios_biceps": {
            1: "Rosca Direta",
            2: "Rosca Scott Unilatral",
            3: "Biceps na polia alta unilateral",
            4: "Biceps no banco 45º martelo simultaneo",
            5: "Rosca alternada"
        },
        "repeticoes_biceps": {
            1: "4x10",
            2: "4x10 (controlado)",
            3: "3x15",
            4: "4x10",
            5: "3x12 4s descendo 2s contraindo"
        },
        "exercicios_triceps": {
            1: "Triceps com barra na polia",
            2: "Triceps com corda polia",
            3: "Triceps na polia unilateral",
            4: "Triceps testa com barra W",
            5: "Triceps no supino (pegada fechada)"
        },
        "repeticoes_triceps": {
            1: "4x8 (pesado)",
            2: "4x12",
            3: "3x15",
            4: "3x8",
            5: "4x10"
        }
    },
    "treino_e": {
        "exercicios_ombro": {
            1: "Desenvolvimento com halteres + Elevação frontal com barra",
            2: "Elevação lateral com halter drop set",
            3: "Elevação lateral na polia",
            4: "Desenvolvimento arnold"
        },
        "repeticoes_ombro": {
            1: "3x15 + 15",
            2: "3x6-8-10 3x10-8-6",
            3: "4x10",
            4: "3x12"
        },
        "exercicios_panturrilha": {
            1: "Panturrilha unilateral degrau"
        },

        "repeticoes_panturrilha": {
            1: "3x20 a cada 10 descase 10 segundos"
        }
    }
}
    

def gerar_treino_aleatorio(dados_exemplo):
    plano_treino = {}
    
    # Regras específicas de cada treino
    regras_treino = {
        "treino_a": {
            "exercicios_costas": 4,
            "exercicios_posteriorombro": 2,
            "exercicios_posteriorcoxa": 2,
        },
        "treino_b": {
            "exercicios_quadriceps": 4,
            "exercicios_panturrilha": 1,
            "exercicios_adutor": 1,
        },
        "treino_c": {
            "exercicios_peito": 4,
            "exercicios_panturrilha": 1,
        },
        "treino_d": {
            "exercicios_biceps": 3,
            "exercicios_triceps": 3,
        },
        "treino_e": {
            "exercicios_ombro": 3,  # Incluindo "Elevação lateral com halter drop set"
            "exercicios_panturrilha": 1,
        }
    }
    
    # Iterar pelos treinos e selecionar os exercícios
    for treino, grupos in regras_treino.items():
        plano_treino[treino] = {}  # Inicializa o treino
        for grupo, qtd in grupos.items():
            # Verificar se o grupo existe nos dados
            if grupo in dados_exemplo[treino]:
                # Selecionar aleatoriamente os exercícios do grupo
                exercicios = random.sample(dados_exemplo[treino][grupo].items(), qtd)
                
                # Adicionar os exercícios e suas repetições ao plano
                plano_treino[treino][grupo] = {
                    nome: dados_exemplo[treino][f"repeticoes_{grupo.split('_')[1]}"].get(idx, "Repetição não encontrada")
                    for idx, nome in exercicios
                }
            else:
                plano_treino[treino][grupo] = "Grupo não encontrado"
    
    return plano_treino

# Formatar o plano em um texto legível
# def formatar_plano_treino(plano_treino):
#     teste = {}
#     for grupo


# Teste da função
plano = gerar_treino_aleatorio(dados_exemplo)
print(plano)
#print(dados_exemplo)
#print(formatar_plano_treino(plano))
