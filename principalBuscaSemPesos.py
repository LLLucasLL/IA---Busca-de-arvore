from BuscaNP import buscaNP
import F_auxiliares as fa
from os import system

op = 1
while(op!='3'):
    system("cls")
    print("**** TIPO DE EXECUÇÃO ****\n")
    print("1. GRAFO")
    print("2. GRID")
    print("3. SAIR")
    op = input("Sua opção: ")
    
    flag_menu = True
    if op=='1':
        #---------------- Executa Grafo -----------------------------
        arquivo = "Grafo_Exe_1.txt"
        nos, grafo = fa.Gera_Problema_Grafo(arquivo)
        print("======== Lista de nós ========\n",nos)
        #print("\n======== Lista de Adjacência ========\n",grafo)
        origem  = input("\nOrigem......: ").upper()
        destino = input("Destino.....: ").upper()
        flag_origem  = origem in nos
        flag_destino = destino in nos
        flag_dados = flag_origem and flag_destino
        flag_grafo = True
        #------------------------------------------------------------
    elif op=='2':
        #---------------- Executa Grid ------------------------------
        arquivo = "mapa1.txt"
        mapa,dx,dy = fa.Gera_Problema_Grid_Fixo(arquivo)
        #nx, ny, qtd = 15, 12, 80
        #mapa,dx,dy = fa.Gera_Problema_Grid_Ale(nx, ny, qtd) 
        print(mapa)
        # Entrada de dados para busca em grid
        origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
        destino = tuple(map(int, input("Digite o destino (x y): ").split()))
        #destino_str = input("Digite as coordenadas de destino no formato x y, separadas por vírgula: ")
        #destino = [tuple(map(int, coord.split())) for coord in destino_str.split(",")]
        flag_origem  = (0<=origem[0]<dx)  and (0<=origem[1]<dy)  and (mapa[origem[0]][origem[1]]==0)
        flag_destino = (0<=destino[0]<dx) and (0<=destino[1]<dy) and (mapa[destino[0]][destino[1]]==0)
        #flag_destino = all(0<=x<dx and 0<=y<dy for x,y in destino)
        flag_dados = flag_origem and flag_destino
        flag_grafo = False
    else:
        flag_menu = False      
        #------------------------------------------------------------

    if flag_menu:
        if flag_dados:
            sol = buscaNP()

            # AMPLITUDE
            if flag_grafo:
                caminho = sol.amplitude_grafo(origem,destino,nos,grafo)
            else:
                caminho = sol.amplitude_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("AMPLITUDE", caminho, len(caminho))
            else:
                print("AMPLITUDE\nCAMINHO NÃO ENCONTRADO")

            # PROFUNDIDADE
            if flag_grafo:
                caminho = sol.profundidade_grafo(origem,destino,nos,grafo)
            else:
                caminho = sol.profundidade_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNDIDADE", caminho, len(caminho))
            else:
                print("PROFUNDIDADE\nCAMINHO NÃO ENCONTRADO")    
            
            # PROFUNDIDADE LIMITADA
            limite = 10
            if flag_grafo:
                caminho = sol.prof_limitada_grafo(origem,destino,nos,grafo,limite)
            else:
                caminho = sol.prof_limitada_grid(origem,destino,dx,dy,mapa,limite)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNIDADE LIMITADA", caminho, len(caminho))
            else:
                print("PROFUNDIDADE LIMITADA\nCAMINHO NÃO ENCONTRADO")

            # APROFUNDAMENTO ITERATIVO
            if flag_grafo:
                l_max = len(nos)
                caminho = sol.aprof_iterativo_grafo(origem,destino,nos,grafo,l_max)
            else:
                l_max = dx + dy
                caminho = sol.aprof_iterativo_grid(origem,destino,dx,dy,mapa,l_max)
            if caminho!=None:
                fa.imprimeCaminho("APROFUNDAMENTO ITERATIVO", caminho, len(caminho))
            else:
                print("APROFUNDAMENTO ITERATIVO\nCAMINHO NÃO ENCONTRADO")

            # BIDIRECIONAL
            if flag_grafo:
                caminho = sol.bidirecional_grafo(origem,destino,nos,grafo)
            else:
                caminho = sol.bidirecional_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("BIDIRECIONAL", caminho, len(caminho))
            else:
                print("BIDIRECIONAL\nCAMINHO NÃO ENCONTRADO")

        else:
            print("Estados inválidos!")
        op = input("Pressione ENTER para continuar!")
