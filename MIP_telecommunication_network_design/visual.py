from grafo_pronto import grafo

class visual:
    matriz_adjacencia = None
    matriz_adjacencia_fluxo = None
    matriz_adjacencia_capacidade = None
    custo = 0.0
    matriz_demandas_adjacencia = None
    matriz_aresta_modulos = None

    def __impressao_bonita(self,G):
        for i in range(len(G.nos)):
            for j in range(len(G.nos)):
                print('fluxo=',self.matriz_adjacencia_fluxo[i][j],'capacidade=',self.matriz_adjacencia_capacidade[i][j],'selec=',self.matriz_aresta_modulos[i][j],'estado=',G.matriz_adjacencia[i][j])

    def __preenche_matriz_adjacencia_capacidade(self,G):
        self.matriz_adjacencia_capacidade = [[0.0 for j in range(len(self.matriz_adjacencia[i]))] for i in range(len(self.matriz_adjacencia))]
        for i in range(len(self.matriz_aresta_modulos)):
            for j in range(len(self.matriz_aresta_modulos[i])):
                if G.matriz_adjacencia[i][j] == -1:
                    continue
                e = G.matriz_adjacencia[i][j]
                T = G.arestas[e].module_list
                for t in range(len(T)):
                    self.matriz_adjacencia_capacidade[i][j] += self.matriz_aresta_modulos[i][j][t]*T[t].capacidade

    def __preenche_matriz_adjacencia_fluxo(self, G):
        self.matriz_adjacencia_fluxo = [[0.0 for j in range(len(self.matriz_adjacencia[i]))] for i in range(len(self.matriz_adjacencia))]
        for k in range(len(self.matriz_demandas_adjacencia)):
            for i in range(len(self.matriz_demandas_adjacencia[k])):
                for j in range(len(self.matriz_demandas_adjacencia[k][i])):
                    self.matriz_adjacencia_fluxo[i][j] += float(self.matriz_demandas_adjacencia[k][i][j])* G.demandas[k].routing_value


    def __preenche_matriz_adjacencia(self):
        self.matriz_adjacencia = [[0 for j in range(len(self.matriz_demandas_adjacencia[0][i]))] for i in range(len(self.matriz_demandas_adjacencia[0]))]
        for k in range(len(self.matriz_demandas_adjacencia)):
            for i in range(len(self.matriz_demandas_adjacencia[k])):
                for j in range(len(self.matriz_demandas_adjacencia[k][i])):
                    self.matriz_adjacencia[i][j] = self.matriz_demandas_adjacencia[k][i][j] or self.matriz_adjacencia[i][j]

    def __preenche_matriz_demandas_adjacencia_matriz_aresta_modulos(self,G):
        arquivo = open(r'instancia1\Solução','r')
        modo = 0
        self.matriz_demandas_adjacencia = []
        self.matriz_aresta_modulos = [[[0 for t in range(G.tam_capacidade)] for j in range(len(G.nos))] for i in range(len(G.nos))]
        e = 0
        for linha in arquivo:
            lista = linha.split()
            if len(lista) == 0:
                modo=1
                continue
            if modo == 0:
                if lista[0] == 'demanda':
                    self.matriz_demandas_adjacencia.append([])
                    continue
                lista_int = []
                for i in lista:
                    lista_int.append(int(i))
                self.matriz_demandas_adjacencia[len(self.matriz_demandas_adjacencia)-1].append(lista_int)
            else:
                lista = linha.split()
                lista_int = []
                for i in lista:
                    lista_int.append(int(i))
                i = lista_int[0]
                j = lista_int[1]
                self.matriz_aresta_modulos[i][j]=lista_int[2:]

    def __init__(self,G):
        self.__preenche_matriz_demandas_adjacencia_matriz_aresta_modulos(G)
        self.__preenche_matriz_adjacencia()
        self.__preenche_matriz_adjacencia_fluxo(G)
        self.__preenche_matriz_adjacencia_capacidade(G)
        self.__impressao_bonita(G)
        pass

G = grafo()
teste = visual(G)
