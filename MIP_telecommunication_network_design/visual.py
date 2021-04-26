from grafo_pronto import grafo
class visual:
    matriz_adjacencia = None
    matriz_adjacencia_fluxo = None
    matriz_adjacencia_capacidade = None
    custo = 0.0
    vx = None
    vy = None
    G = None
    def __dfs(self,s,dk,k,vis):
        if s == dk:
            return 1
        soma = 0
        for i in range(len(self.G.nos)):
            if self.vx[s][i][k] and not vis[i]:
                soma+=self.__dfs(i,dk,k,vis)
        return soma

    def __verifica_caminho_unico(self):
        for k in range(len(self.G.demandas)):
            ok = self.G.demandas[k].idx_i
            dk = self.G.demandas[k].idx_j
            vis = [0 for j in range(len(self.G.nos))]
            ret = self.__dfs(ok,dk,k,vis)
            if(ret != 1):
                print('FALHOU NO TESTE DE CAMINHO ÚNICO')
                return False
        print('PASSOU NO TESTE DE CAMINHO ÚNICO')
        return True

    def __calculo_custo(self):
        for i in range(len(self.vy)):
            for j in range(len(self.vy[i])):
                for t in range(len(self.vy[i][j])):
                    self.custo+=self.vy[i][j][t]*self.G.matriz_adjacencia_custo[i][j][t]
        print('custo::::',self.custo)

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
        self.matriz_adjacencia_capacidade = [[0.0 for j in range(len(self.G.nos))] for i in range(len(self.G.nos))]

        for i in range(len(self.vx)):
            for j in range(len(self.vx[i])):
                for k in range(len(self.vx[i][j])):
                    self.matriz_adjacencia[i][j] += self.vx[i][j][k]
                    self.matriz_adjacencia_fluxo[i][j] += float(self.vx[i][j][k])*self.G.matriz_adjacencia_demanda[i][j][k]

        for i in range(len(self.vy)):
            for j in range(len(self.vy[i])):
                value = 0.0
                for t in range(len(self.vy[i][j])):
                    value += self.vy[i][j][t]*self.G.matriz_adjacencia_capacidade[i][j][t]
                self.matriz_adjacencia_capacidade[i][j] = value

    def __init__(self,G,vx,vy):
        self.vx = vx
        self.vy = vy
        self.G = G
        self.__preeche()
        self.__teste_fluxo_capacidade()
        self.__calculo_custo()
        self.__verifica_caminho_unico()


# G = grafo()
# teste = visual(G)
