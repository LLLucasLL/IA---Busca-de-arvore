import F_auxiliares as fa
import sys
from os import system       
from BuscaP import buscaP   
#--------------------------------------------------------------------------
# MÓDULO PRINCIPAL
#--------------------------------------------------------------------------
while(True):
    system("cls")
    print("**** TIPO DE EXECUÇÃO ****\n")
    print("1. GRAFO")
    print("2. GRID")
    print("3. SAIR")
    op = input("Sua opção:")
    
    if(op=='1'):
        nos, grafo = fa.Gerar_Problema_Grafo_P("Romenia_Com_Pesos.txt")
        origem  = input("\nOrigem......: ").upper()
        destino = input("Destino.....: ").upper()
        flag_origem  = origem in nos
        flag_destino = destino in nos
        flag = flag_origem and flag_destino
        flag_grafo = True
        #------------------------------------------------------------
    elif op=='2':
        #---------------- Executa Grig ------------------------------
        arquivo = "mapa.txt"
        mapa,dx,dy = fa.Gera_Problema_Grid_Fixo_P(arquivo)
        #nx, ny, qtd = 15, 12, 80
        #mapa,dx,dy = fa.Gera_Problema_Grid_Ale_P(nx, ny, qtd) 
        print(mapa)
        # Entrada de dados para busca em grid
        origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
        destino = tuple(map(int, input("Digite o destino (x y): ").split()))
        #destino_str = input("Digite as coordenadas de destino no formato x y, separadas por vírgula: ")
        #destino = [tuple(map(int, coord.split())) for coord in destino_str.split(",")]
        flag_origem  = (0<=origem[0]<dx)  and (0<=origem[1]<dy)  and (mapa[origem[0]][origem[1]]==0)
        flag_destino = (0<=destino[0]<dx) and (0<=destino[1]<dy) and (mapa[destino[0]][destino[1]]==0)
        #flag_destino = all(0<=x<dx and 0<=y<dy for x,y in destino)
        flag = flag_origem and flag_destino
        flag_grafo = False
    else:
        sys.exit()
    
        #------------------------------------------------------------
    if flag:
        system("cls")
        sol = buscaP()
        if flag_grafo:
            caminho, custo = sol.custo_uniforme_grafo(origem,destino,nos,grafo)
        else:
            caminho, custo = sol.custo_uniforme_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("*** CUSTO UNIFORME ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")
        
        if flag_grafo:
            caminho, custo = sol.greedy_grafo(origem,destino,nos,grafo)
        else:
            caminho, custo = sol.greedy_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** GREEDY ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")
        
        if flag_grafo:
            caminho, custo = sol.a_estrela_grafo(origem,destino,nos,grafo)
        else:
            caminho, custo = sol.a_estrela_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** A ESTRELA ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")
        
        if flag_grafo:
            caminho, custo = sol.aia_estrela_grafo(origem,destino,nos,grafo)
        else:
            caminho, custo = sol.aia_estrela_grid(origem,destino,mapa,dx,dy)
        if caminho!=None:
            print("\n*** AIA ESTRELA ****")
            print("Caminho...: ",caminho)
            print("Custo.....:",custo)
        else:
            print("Caminho não encontrado")
        input("\nPressione ENTER para continuar.")