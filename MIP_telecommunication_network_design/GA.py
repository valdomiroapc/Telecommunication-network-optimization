from grafo_pronto import grafo
import random
import asyncio as asy
G = grafo('pdh.txt')
random.seed(None)
class cromossomo:
    demanda_caminho = None
    fluxo_aresta = None
    custo = None
    soma_tam_caminhos= None

    def __gera_cromossomo(self):
        candidato = [0 for i in range(len(G.demandas))]
        while True:
            tam = len(G.demandas)
            for i in range(tam):
                candidato[i] = random.randint(0,len(G.caminhos[i])-1)
            a=[0.0 for i in range(len(G.arestas))]
            for i in range(tam):
                tam1 = len(G.caminhos[i][candidato[i]])
                for e in range(tam1):
                    if G.caminhos[i][candidato[i]][e] == 1:
                        a[e] += G.demandas[i].routing_value
            deu = True
            for e in range(len(G.arestas)):
                if a[e] > G.array_max_cap[e]:
                    deu = False
                    break
            if deu:
                self.demanda_caminho= [[] for i in range(tam)]
                for i in range(tam):
                    caminho = []+G.caminhos[i][candidato[i]]
                    tam1 = len(caminho)
                    for j in range(tam1):
                        if caminho[j] == 1:
                            self.demanda_caminho[i].append(j)
                self.fluxo_aresta = a
                break

    def __f(self,modulo,aresta,quant_modulos,custo,capacidade,dp):
        if modulo == quant_modulos:
            if capacidade>=self.fluxo_aresta[aresta]:
                return float(custo)
            else:
                return 10000000000000.0
        testa = (modulo,custo,capacidade)
        if testa in dp.keys():
            return dp[(modulo,custo,capacidade)]
        nao_pega = self.__f(modulo+1,aresta,quant_modulos,custo,capacidade,dp)
        pega = self.__f(modulo+1,aresta,quant_modulos,custo+G.arestas[aresta].module_list[modulo].cost,capacidade+G.arestas[aresta].module_list[modulo].capacidade,dp)
        dp[(modulo,custo,capacidade)] = min(nao_pega,pega)
        return dp[(modulo,custo,capacidade)]

    def __calcula_custo(self):
        tam = len(G.arestas)
        self.custo = 0.0
        for e in range(tam):
            dp={}
            val = self.__f(0,e,len(G.arestas[e].module_list), G.arestas[e].pre_installed_capacity_cost,G.arestas[e].pre_installed_capacity,dp)
            self.custo += val
    def __f_dif(self,modulo,aresta,quant_modulos,custo,capacidade,dp,fluxo_aresta):
        if modulo == quant_modulos:
            if capacidade>=fluxo_aresta[aresta]:
                return float(custo)
            else:
                return 10000000000000.0
        testa = (modulo,custo,capacidade)
        if testa in dp.keys():
            return dp[(modulo,custo,capacidade)]
        nao_pega = self.__f_dif(modulo+1,aresta,quant_modulos,custo,capacidade,dp,fluxo_aresta)
        pega = self.__f_dif(modulo+1,aresta,quant_modulos,custo+G.arestas[aresta].module_list[modulo].cost,capacidade+G.arestas[aresta].module_list[modulo].capacidade,dp,fluxo_aresta)
        dp[(modulo,custo,capacidade)] = min(nao_pega,pega)
        return dp[(modulo,custo,capacidade)]

    def __calcula_custo_dif(self,fluxo_aresta):
        tam = len(G.arestas)
        custo = 0.0
        for e in range(tam):
            dp={}
            val = self.__f_dif(0,e,len(G.arestas[e].module_list), G.arestas[e].pre_installed_capacity_cost,G.arestas[e].pre_installed_capacity,dp,fluxo_aresta)
            custo += val
        return custo

    def __calcula_soma_tamanho_caminhos(self):
        tam = len(self.demanda_caminho)
        self.soma_tam_caminhos=0
        for i in range(tam):
            self.soma_tam_caminhos+=len(self.demanda_caminho[i])

    def __imprime_cromossomo(self):
        print('-------------')
        for d in range(len(self.demanda_caminho)):
            for e in range(len(self.demanda_caminho[d])):
                print(self.demanda_caminho[d][e],end=' ')
            print()
        print('-------------')
    def __busca_local(self):
        continua = 1
        while continua:
            demanda_idx = 0
            continua = 0
            while demanda_idx < len(self.demanda_caminho):
                demanda_caminho = [] + self.demanda_caminho
                fluxo_aresta = [] + self.fluxo_aresta
                custo = 0.0
                soma_tam_caminho = 0
                conjunto_caminho = []+G.caminhos[demanda_idx]
                for e in demanda_caminho[demanda_idx]:#remove fluxo do caminho atual
                    fluxo_aresta[e] -= G.demandas[demanda_idx].routing_value
                ref_fluxo_aresta = []+fluxo_aresta
                for cmh in conjunto_caminho:#para cada caminho do conjunto de caminhos
                    cmh_formatado = []
                    for i in range(len(cmh)):
                        if cmh[i] == 1:
                            cmh_formatado.append(i)
                    demanda_caminho[demanda_idx] = []+cmh_formatado
                    for e in cmh_formatado:
                        fluxo_aresta[e] += G.demandas[demanda_idx].routing_value
                    custo = self.__calcula_custo_dif(fluxo_aresta)
                    for c in demanda_caminho:
                        soma_tam_caminho += len(c)
                    #if (custo < self.custo and soma_tam_caminho <= self.soma_tam_caminhos) or (custo<=self.custo and soma_tam_caminho<self.soma_tam_caminhos):
                    if custo<self.custo:
                        self.demanda_caminho = [] + demanda_caminho
                        self.fluxo_aresta = [] + fluxo_aresta
                        self.custo = custo
                        self.soma_tam_caminhos = soma_tam_caminho
                        continua = 1
                    fluxo_aresta = []+ref_fluxo_aresta
                demanda_idx+=1
    def __lt__(self,other):
        return (self.custo < other.custo and self.soma_tam_caminhos < other.soma_tam_caminhos) or (self.custo <= other.custo and self.soma_tam_caminhos< other.soma_tam_caminhos)

    def eh_aceitavel(self,demanda_caminho):
        fluxo_aresta = [ 0.0 for i in range(len(self.fluxo_aresta))]
        for cmh in range(len(demanda_caminho)):
            for e in demanda_caminho[cmh]:
                fluxo_aresta[e] += G.demandas[cmh].routing_value
        for e in range(len(fluxo_aresta)):
            if fluxo_aresta[e] > G.array_max_cap[e]:
                return None
        return fluxo_aresta

    def __add__(self, other):
        while True:
            filho1 = []
            filho2 = []
            ord = []
            for i in range(len(self.demanda_caminho)):
                ord.append(random.randint(0,1))
            for c in range(len(self.demanda_caminho)):
                if ord[c] == 1:
                    filho1.append(self.demanda_caminho[c])
                    filho2.append(other.demanda_caminho[c])
                else:
                    filho2.append(self.demanda_caminho[c])
                    filho1.append(other.demanda_caminho[c])
            prole = []
            f1 = self.eh_aceitavel(filho1)
            f2 = self.eh_aceitavel(filho2)
            if f1 != None:
                prole.append(cromossomo(tipo='receber',demanda_caminho=filho1,fluxo_aresta=f1))
            if f2 != None:
                prole.append(cromossomo(tipo='receber',demanda_caminho=filho2,fluxo_aresta=f2))
            return prole

    def mutacao(self):
        demanda_caminho = []+self.demanda_caminho
        fluxo_aresta = []+self.fluxo_aresta
        for c in range(len(demanda_caminho)):
            p = float(random.randint(1,100))/100.0
            if p > 0.5:
                continue
            for e in demanda_caminho[c]:
                fluxo_aresta[e] -= G.demandas[c].routing_value
            ref_fluxo_aresta = [] + fluxo_aresta
            while True:
                tam = len(G.caminhos[c])-1
                caminho = G.caminhos[c][random.randint(0,tam)]
                aux = []
                for e in range(len(caminho)):
                    if caminho[e] == 1:
                        aux.append(e)
                for e in aux:
                    fluxo_aresta[e] += G.demandas[c].routing_value
                deu = True
                for i in range(len(fluxo_aresta)):
                    if fluxo_aresta[i] > G.array_max_cap[i]:
                        deu = False
                        break
                if deu == True:
                    demanda_caminho[c] = aux
                    break
                else:
                    fluxo_aresta = []+ref_fluxo_aresta
        return cromossomo(tipo='receber',demanda_caminho=demanda_caminho,fluxo_aresta=fluxo_aresta)

    def __init__(self,tipo='gerar',demanda_caminho=None,fluxo_aresta=None):
        if tipo == 'gerar':
            self.__gera_cromossomo()
        if tipo == 'receber':
            self.demanda_caminho = demanda_caminho
            self.fluxo_aresta = fluxo_aresta
        self.__calcula_custo()
        self.__calcula_soma_tamanho_caminhos()
        # self.__imprime_cromossomo()
        #self.__busca_local()
        #print('custo:',self.custo,'tam caminhos:',self.soma_tam_caminhos)


class GA:
    taxa_cruzamento = 0.5
    taxa_mutacao = 0.5
    tamanho_populacao = 50
    populacao = None
    ranks = None
    def __gera_populacao(self):
        self.populacao = []
        a = cromossomo()
        for i in range(self.tamanho_populacao):
            self.populacao.append(cromossomo())
        print('Populacao gerada')
        pass
    def __insertion_sort(self):
        pass
    def non_dominated_pareto_sort(self):
        ranks = [ -1 for i in range(self.tamanho_populacao)]
        x_dominates = [[] for i in range(self.tamanho_populacao)]
        qt=[0 for i in range(self.tamanho_populacao)]
        for s1 in range(len(self.populacao)):
            for s2 in range(len(self.populacao)):
                if self.populacao[s1] < self.populacao[s2]:
                    x_dominates[s1].append(s2)
                    qt[s2]+=1
        fila = asy.queues.Queue
        for i in range(self.tamanho_populacao):
            if qt[i] == 0:
                fila.put((i,0))
                ranks[i]=0
        while not fila.empty():
            aux = fila.get()
            davez = aux[0]
            r = aux[1]
            for i in x_dominates[davez]:
                qt[i]-=1
            for i in range(self.tamanho_populacao):
                if qt[i] == 0:
                    fila.put((i,r+1))
                    ranks[i] = r+1


    def __decide_parametros(self):
        pass

    def __torneio(self,adv=-1):
        lim = len(self.populacao)
        ret = random.randint(0,lim-1)
        rounds = 3
        for rounds in range(0,3):
            other = random.randint(0,lim-1)
            while other == adv or other == ret:
                other = random.randint(0,lim-1)
            if self.populacao[other] < self.populacao[ret]:
                ret = other
        return ret

    def __operador_cruzamento(self):
        p = float(random.randint(1,100))/100.0
        if p > self.taxa_cruzamento:
            return False
        while True:
            parent1 = self.__torneio()
            parent2 = self.__torneio(adv = parent1)
            prole = self.populacao[parent1]+self.populacao[parent2]
            if len(prole) > 0:
                self.populacao = self.populacao + prole
                return True

    def __operador_mutacao(self):
        for e in range(len(self.populacao)):
            p = float(random.randint(1, 100))/100.0
            if p > self.taxa_mutacao:
                continue
            self.populacao[e] = self.populacao[e].mutacao()

    def __elitismo(self):
        pass
    def __init__(self):
        self.__gera_populacao()
        while True:
            self.__operador_cruzamento()
            print('cruzamento finalizado')
            self.__operador_mutacao()
            print('fim iteracao')


teste = GA()