from grafo_pronto import grafo
class visual:
    matriz_adjacencia = None
    matriz_adjacencia_fluxo = None
    matriz_adjacencia_capacidade = None
    custo = 0.0
    vx = None
    vy = None
    G = None
    def __teste_fluxo_capacidade(self):
        for i in range(len(self.matriz_adjacencia_fluxo)):
            for j in range(len(self.matriz_adjacencia_fluxo[i])):
                if self.matriz_adjacencia_fluxo[i][j] > self.matriz_adjacencia_capacidade[i][j]:
                    print('Não passou no teste fluxo capacidade')
                    return False
        print('passou no teste fluxo capacidade')
        return True

    def __preeche(self):
        self.matriz_adjacencia = [[0 for j in range(len(self.G.nos))] for i in range(len(self.G.nos))]
        self.matriz_adjacencia_fluxo = [[0.0 for j in range(len(self.G.nos))] for i in range(len(self.G.nos))]
        self.matriz_adjacencia_capacidade = [[0 for j in range(len(self.G.nos))] for i in range(len(self.G.nos))]

        for k in range(len(self.vx)):
            for i in range(len(self.vx[k])):
                for j in range(len(self.vx[k][i])):
                    self.matriz_adjacencia[i][j] += self.vx[k][i][j]
                    self.matriz_adjacencia_fluxo[i][j] += float(self.vx[k][i][j])*self.G.demandas[k].routing_value

        for i in range(len(self.matriz_adjacencia)):
            for j in range(len(self.matriz_adjacencia[i])):
                print(self.matriz_adjacencia[i][j],end=' ')
            print('')
        print('')
        for i in range(len(self.matriz_adjacencia_fluxo)):
            for j in range(len(self.matriz_adjacencia_fluxo[i])):
                print(self.matriz_adjacencia_fluxo[i][j],end=' ')
            print('')
        print('')
        for i in range(len(self.vy)):
            for j in range(len(self.vy[i])):
                value = 0.0
                if self.G.matriz_adjacencia[i][j] != -1:
                    e = self.G.matriz_adjacencia[i][j]
                    for t in range(len(self.vy[i][j])):
                        value += self.vy[i][j][t]*self.G.arestas[e].module_list[t].capacidade
                self.matriz_adjacencia_capacidade[i][j] = value

        for i in range(len(self.matriz_adjacencia_capacidade)):
            for j in range(len(self.matriz_adjacencia_capacidade[i])):
                print(self.matriz_adjacencia_capacidade[i][j],end=' ')
            print('')

    def __init__(self,G,vx,vy):
        self.vx = vx
        self.vy = vy
        self.G = G
        self.__preeche()
        self.__teste_fluxo_capacidade()


# G = grafo()
# teste = visual(G)
