import PySimpleGUI as sg
from numpy import linalg
from numpy import array
from random import randint

# Tema utilizado
sg.theme('Light Green 3')

# Função para tela inicial
def pagina_inicial(name, backgroundColor):
    
    layout = [
        [sg.Text(name, size=(15, 0), border_width=3, background_color=backgroundColor, justification='center', font='monospace', text_color='#1f1f1f')],
        [sg.Text('Linhas', colors='black'), sg.Push(), sg.Text('Colunas', colors='black')],
        [sg.InputText(size=(3,1), border_width=2, background_color='#fff', selected_text_color='white', font='monospace', key=f'-LINHAS_{name}-'),
        sg.Push(),
        sg.InputText(size=(3,1), border_width=2, background_color='#fff', selected_text_color='white', font='monospace', key=f'-COLUNAS_{name}-')]
    ]

    return layout

# Inicializo as seções A e B da tela inicial
matrizA_layout = pagina_inicial('Matriz A', '#cfede3')
matrizB_layout = pagina_inicial('Matriz B', '#cfede3')

dados_A_frame = [
    [sg.Frame('', matrizA_layout, size=(170, 100), border_width=1)]
]

dados_B_frame = [
    [sg.Frame('', matrizB_layout, size=(170, 100), border_width=1)]
]

# Layout inicial
layout = [
    [sg.Column(dados_A_frame, element_justification='center'), sg.Column(dados_B_frame, element_justification='center')],
    [sg.Text(''), sg.Button('GERAR', size=(10, 1), pad=((130, 0), (10, 10)), button_color=('black', '#a7a7a7'), key='-BUTTON-', bind_return_key=True)]
]

# Crio a janela
window = (sg.Window('Linhas e Colunas', layout = layout))

# Função para criar as caixas da matriz
def criar_campos_matriz(chave, valores):
    
    segunda_pagina = []  # Lista para armazenar as linhas da matriz
    
    for i in range(int(valores[f'-LINHAS_{chave}-'])):
        row = []
        for j in range(int(valores[f'-COLUNAS_{chave}-'])):
            msg = f'{chave}_{i}_{j}'
            input_element = sg.InputText(size=(6, 1), key=msg, background_color='#fff', justification='center')
            row.append(input_element)
        segunda_pagina.append(row)

    return segunda_pagina

# Função responsavel pela segunda pagina
def segunda_pagina(valores):
    
    layoutButton = [
        [sg.Button('Voltar', key='-VOLTAR-')]
    ]
    
    layoutMatrizA = [
        [sg.Text('Matriz A', size=(15, 0), border_width=3, justification='center', font='monospace')],
        *criar_campos_matriz('Matriz A', valores),
        [sg.Button('Transp. A', size=(7, 1), key='-TRANSPOSTA_A-', button_color=('black', '#a7a7a7')), sg.Button('Det A', size=(7, 1), key='-DETERMINANTE_A-', button_color=('black', '#a7a7a7'))],
    ]
    layoutA_frame = [
        [sg.Frame('', layoutMatrizA, border_width=1)]
    ]
    
    layoutMatrizB = [
        [sg.Text('Matriz B', size=(15, 0), border_width=3, justification='center', font='monospace')],
        *criar_campos_matriz('Matriz B', valores),
        [sg.Button('Transp. B', size=(7, 1), key='-TRANSPOSTA_B-', button_color=('black', '#a7a7a7')), sg.Button('Det B', size=(7, 1), key='-DETERMINANTE_B-', button_color=('black', '#a7a7a7'))]
    ]
    layoutB_frame = [
        [sg.Frame('', layoutMatrizB, border_width=1)]
    ]
    
    layoutButtonMenu = [
        [sg.Button('Soma', size=(12, 1), button_color=('black', '#a7a7a7'), key='-SOMA-')],
        [sg.Button('Subtração', size=(12, 1), button_color=('black', '#a7a7a7'), key='-SUBTRACAO-')],
        [sg.Button('Multiplicação', size=(12, 1), button_color=('black', '#a7a7a7'), key='-MULTIPLICA-')],
        [sg.Button('Matriz Mágica', size=(12, 1), button_color=('black', '#a7a7a7'), key='-MAGICSQUARE-')],
    ]

    layout = [
        [sg.Column(layoutButton)],
        [sg.Column(layoutA_frame, element_justification='center'),
         sg.Column(layoutButtonMenu, element_justification='center'),
        sg.Column(layoutB_frame, element_justification='center')],
    ]
    
    return layout

# Função responsavel por possibilitar a inserção de valores
def inserir_valores(cell_info_dict, matriz_type):
    info_matriz = []
    max_linha, max_coluna = 0, 0

    # Preenche a lista info_matriz com as informações de linha, coluna e valor
    for key, value in cell_info_dict.items():
        if matriz_type in key:
            linha, coluna = map(int, key.split('_')[-2:])
            info_matriz.append((linha, coluna, float(value)))
            max_linha = max(max_linha, linha)
            max_coluna = max(max_coluna, coluna)

    # Determina o número de linhas e colunas da matriz
    linhas = max_linha + 1
    colunas = max_coluna + 1

    # Inicializa a matriz com zeros
    matriz = [[0] * colunas for _ in range(linhas)]

    # Preenche a matriz com os valores extraídos do dicionário
    for i, j, value in info_matriz:
        matriz[i][j] = value

    return matriz

def tela_resultado(title, matriz):
    # Cria a grade para exibir os valores da matriz
    grid = []
    for i in range(len(matriz)):
        row = []
        for j in range(len(matriz[0])):
            cell = sg.Text(f'{matriz[i][j]:<4}', size=(6, 2), font=('Helvetica', 14), justification='center', relief=sg.RELIEF_RAISED, background_color='#fff')
            row.append(cell)
        grid.append(row)

    # Define o layout da janela
    layout = [
        [sg.Column(grid, size=(None, None), scrollable=True, expand_x=True, expand_y=True, background_color="#4CAF50", justification='center')],
        [sg.Button('Fechar', button_color=('black', '#a7a7a7'), font=('Helvetica', 10), size=(8, 1), pad=(10, 10))]
    ]

    # Cria a janela
    window = sg.Window(title, layout, finalize=True, resizable=True)

    # Loop de eventos da janela
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break

    # Fecha a janela ao sair do loop
    window.close()
    
def determinante(matriz):
    det = linalg.det(matriz)
    
    layout = [
        [sg.Frame("", [[sg.Text(f"{round(det, 2)}", background_color="#fff")]], pad=(60, 20))],
        [sg.Push(), sg.Button('Fechar', button_color=('black', '#a7a7a7'), auto_size_button=True)]
    ]
    
    window = sg.Window("Determinante", layout, finalize=True)
    
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Fechar':
            break
    window.close()
    
def transposta(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    
    matriz_transposta = []
    for i in range(0, colunas):
        matriz_transposta.append([0] * linhas)
        
    for i in range(linhas):
        for j in range(colunas):
            matriz_transposta[j][i] = matriz[i][j]
            
    tela_resultado("Matriz Transposta", matriz_transposta) 
   
def multiplicacao(matriz_a, matriz_b):
    
    linha_a = len(matriz_a)
    coluna_a = len(matriz_a[0])
    linha_b = len(matriz_b)
    coluna_b = len(matriz_b[0])
    
    if coluna_a != linha_b:
        return sg.popup_error("O número de colunas da matriz A deve ser igual ao número de linhas da matriz B.", no_titlebar=True, text_color='black')
    
    matriz_multiplicacao = []
    for i in range(linha_a):
        linha = []
        for j in range(coluna_b):
            position = 0
            for k in range(coluna_a):
                position += matriz_a[i][k] * matriz_b[k][j]
            linha.append(round(position, 2))
            
        matriz_multiplicacao.append(linha)
        
    tela_resultado('Multiplicação de Matrizes', matriz_multiplicacao)
    
def is_decimal(num):
    return isinstance(num, int) or isinstance(num, float)

def all_decimal(valores):
    for element in valores.values():
        try:
            if not is_decimal(float(element)):
                return False
        except ValueError:
            return False
    return True

# Função para criar a janela de soma de matrizes
def soma(matriz_a, matriz_b):
    
    if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
        return sg.popup_error("As matrizes devem ter as mesmas dimensões para realizar a soma.", no_titlebar=True, text_color='black')

    # Inicializa a matriz de soma com zeros
    matriz_soma = [[0] * len(matriz_a[0]) for _ in range(len(matriz_a))]

    for i in range(len(matriz_a)):
        for j in range(len(matriz_a[0])):
            matriz_soma[i][j] = matriz_a[i][j] + matriz_b[i][j]

    # Exibe o resultado em uma janela
    tela_resultado('Soma de Matrizes', matriz_soma)
            
def subtracao(matriz_a, matriz_b):
    
    if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
        return sg.popup_error("As matrizes devem ter as mesmas dimensões para realizar a soma.", no_titlebar=True, text_color='black')

    matriz_subtracao = [[0] * len(matriz_a[0]) for _ in range(len(matriz_a))]

    for i in range(len(matriz_a)):
        for j in range(len(matriz_a[0])):
            matriz_subtracao[i][j] = matriz_a[i][j] - matriz_b[i][j]

    tela_resultado('Subtração de Matrizes', matriz_subtracao)

def gerarMatrizMagica(ordem_matriz):
    matriz_magica_padrao = None

    if ordem_matriz % 2 == 0 or ordem_matriz > 7:
        sg.popup_error("Erro", "A ordem da Matriz Mágica deve ser Ímpar! (Limitado até 7)")
        return None

    try:
        if ordem_matriz == 1:
            num_aleatorio = randint(1, 100)
            matriz_magica_padrao = [[num_aleatorio]]
        elif ordem_matriz == 2:
            i = randint(-3, 10)
            matriz_magica_padrao = [
                [4+i, 4+i],
                [4+i, 4+i]
            ]
        elif ordem_matriz == 3:
            i = randint(-12, 12)
            matriz_magica_padrao = [
                [8+i, 1+i, 6+i],
                [3+i, 5+i, 7+i],
                [4+i, 9+i, 2+i]
            ]
        elif ordem_matriz == 4:
            i = randint(-8, 10)
            matriz_magica_padrao = [
                [1+i, 14+i, 14+i, 4+i],
                [12+i, 7+i, 6+i, 9+i],
                [8+i, 11+i, 10+i, 5+i],
                [13+i, 2+i, 3+i, 16+i]
            ]
        elif ordem_matriz == 5:
            i = randint(-15, 15)
            matriz_magica_padrao = [
                [17+i, 24+i, 1+i, 8+i, 15+i],
                [23+i, 5+i, 7+i, 14+i, 16+i],
                [4+i, 6+i, 13+i, 20+i, 22+i],
                [10+i, 12+i, 19+i, 21+i, 3+i],
                [11+i, 18+i, 25+i, 2+i, 9+i]
            ]
        elif ordem_matriz == 6:
            i = randint(-7, 7)
            matriz_magica_padrao = [
                [35+i, 1+i, 6+i, 26+i, 19+i, 24+i],
                [3+i, 32+i, 7+i, 21+i, 23+i, 25+i],
                [31+i, 9+i, 2+i, 22+i, 27+i, 20+i],
                [8+i, 28+i, 33+i, 17+i, 10+i, 15+i],
                [30+i, 5+i, 34+i, 12+i, 14+i, 16+i],
                [4+i, 36+i, 29+i, 13+i, 18+i, 11+i]
            ]
        elif ordem_matriz == 7:
            i = randint(-6, 16)
            matriz_magica_padrao = [
                [30+i, 39+i, 48+i, 1+i, 10+i, 19+i, 28+i],
                [38+i, 47+i, 7+i, 9+i, 18+i, 27+i, 29+i],
                [46+i, 6+i, 8+i, 17+i, 26+i, 35+i, 37+i],
                [5+i, 14+i, 16+i, 25+i, 34+i, 36+i, 45+i],
                [13+i, 15+i, 24+i, 33+i, 42+i, 44+i, 4+i],
                [21+i, 23+i, 32+i, 41+i, 43+i, 3+i, 12+i],
                [22+i, 31+i, 40+i, 49+i, 2+i, 11+i, 20+i]
            ]
        else:
            sg.popup_error('Apenas Números Impares!', no_titlebar=True, text_color='black')

    except ValueError as ve:
        sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')

    return matriz_magica_padrao
    
def exibir_matriz_magica(ordem):
    tela_resultado("Matriz Mágica", gerarMatrizMagica(ordem))

while True:
    event, valores = window.read()
    
    match(event):
        case '-BUTTON-':
            if all(v.isdecimal() for v in valores.values()):
                novo_layout = segunda_pagina(valores)
                window.close()
                window = sg.Window('Matrizes', layout = novo_layout)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-TRANSPOSTA_A-':
            if all_decimal(valores):
                matriz_A = inserir_valores(valores, 'Matriz A')
                transposta(matriz_A)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-TRANSPOSTA_B-':
            if all_decimal(valores):
                matriz_B = inserir_valores(valores, 'Matriz B')
                transposta(matriz_B)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-DETERMINANTE_A-':
            if all_decimal(valores):
                matriz_A = inserir_valores(valores, 'Matriz A')
                determinante(matriz_A)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-DETERMINANTE_B-':
            if all_decimal(valores):
                matriz_B = inserir_valores(valores, 'Matriz B')
                determinante(matriz_B)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-SOMA-':
            if all_decimal(valores):
                matriz_A = inserir_valores(valores, 'Matriz A')
                matriz_B = inserir_valores(valores, 'Matriz B')
                soma(matriz_A, matriz_B)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-SUBTRACAO-':
            if all_decimal(valores):
                matriz_A = inserir_valores(valores, 'Matriz A')
                matriz_B = inserir_valores(valores, 'Matriz B')
                subtracao(matriz_A, matriz_B)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-MULTIPLICA-':
            if all_decimal(valores):
                matriz_A = inserir_valores(valores, 'Matriz A')
                matriz_B = inserir_valores(valores, 'Matriz B')
                multiplicacao(matriz_A, matriz_B)
            else:
                sg.popup_error('Apenas números inteiros!', no_titlebar=True, text_color='black')
        case '-VOLTAR-':
            novo_layout_A = pagina_inicial('Matriz A', '#cfede3')
            novo_layout_B = pagina_inicial('Matriz B', '#cfede3')
            window.close()
            dados_A_frame = [
                [sg.Frame('', novo_layout_A, size=(170, 100), border_width=1)]
            ]
            dados_B_frame = [
                [sg.Frame('', novo_layout_B, size=(170, 100), border_width=1)]
            ]

            layout = [
                [sg.Column(dados_A_frame, element_justification='center'), sg.Column(dados_B_frame, element_justification='center')],
                [sg.Button('GERAR', size=(10, 1), pad=((130, 0), (10, 10)), button_color=('black', '#a7a7a7'), key='-BUTTON-', bind_return_key=True)]
            ]
            window = sg.Window('Linhas e Colunas', layout = layout)
        case '-MAGICSQUARE-':
            newLayout = [
                [sg.Text('Ordem da Matriz', size=(15, 1), border_width=3, background_color='#fff', justification='center', font='monospace')],
                [sg.InputText(size=(6, 1), key='-ORDEM-', background_color='#fff', justification='center')],
                [sg.Button('Gerar', size=(4, 1), button_color=('black', '#a7a7a7'))]
            ]
            
            newWindow = sg.Window('Matriz Mágica', layout=newLayout, element_justification="center")
            while True:
                newEvent, novos_valores = newWindow.read()

                if newEvent == sg.WINDOW_CLOSED:
                    break
                elif newEvent == 'Gerar':
                    try:
                        ordem = int(novos_valores['-ORDEM-']) if is_decimal(int(novos_valores['-ORDEM-'])) else 0
                    except ValueError:
                        ordem = 0
                    if ordem > 0:
                        exibir_matriz_magica(ordem)
                    else:
                        sg.popup_error("Por favor, insira um valor válido para a ordem da matriz.")
        case None:
            break
        
window.close()