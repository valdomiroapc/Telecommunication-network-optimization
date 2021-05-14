from grafo_pronto import grafo
import random
import queue
from copy import deepcopy
from math import sqrt
import time
import matplotlib.pyplot as plt
import numpy as np
import os
G = grafo('pdh.txt')
random.seed(None)
class cromossomo:
    demanda_caminho = None
    fluxo_aresta = None
    custo = None


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
                    print(a[e],G.array_max_cap[e])
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

    def __calcula_custo(self):
        tam = len(G.arestas)
        self.custo = 0.0
        for e in range(len(G.arestas)):
            self.custo+=G.arestas[e].pre_installed_capacity_cost
            if self.fluxo_aresta == 0 or self.fluxo_aresta[e]<=G.arestas[e].pre_installed_capacity:
                continue
            val = 100000000000.0
            for k in range(len(G.arestas[e].module_list)):
                if G.arestas[e].module_list[k].capacidade+G.arestas[e].pre_installed_capacity >= self.fluxo_aresta[e]:
                    val = min(val,G.arestas[e].module_list[k].cost)
            self.custo += val

    def __calcula_custo_dif(self,fluxo_aresta):
        tam = len(G.arestas)
        custo = 0.0
        for e in range(len(G.arestas)):
            custo+=G.arestas[e].pre_installed_capacity_cost
            if fluxo_aresta[e] == 0 or fluxo_aresta[e]<=G.arestas[e].pre_installed_capacity:
                continue
            val = 100000000000.0
            for k in range(len(G.arestas[e].module_list)):
                if G.arestas[e].module_list[k].capacidade +G.arestas[e].pre_installed_capacity >= fluxo_aresta[e]:
                    val = min(val, G.arestas[e].module_list[k].cost)
            custo += val
        return custo

    def __imprime_cromossomo(self):
        print('-------------')
        for d in range(len(self.demanda_caminho)):
            for e in range(len(self.demanda_caminho[d])):
                print(self.demanda_caminho[d][e],end=' ')
            print()
        print('-------------')
    def __busca_local(self):
        continua = 1
        ti = time.process_time()
        while continua:
            tt = len(self.demanda_caminho)
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
                    if custo < self.custo:
                        self.demanda_caminho = [] + demanda_caminho
                        self.fluxo_aresta = [] + fluxo_aresta
                        self.custo = custo
                        self.soma_tam_caminhos = soma_tam_caminho
                        continua = 1
                    fluxo_aresta = []+ref_fluxo_aresta
                demanda_idx+=1
            break

    def eh_aceitavel(self,demanda_caminho):
        fluxo_aresta = [ 0.0 for i in range(len(self.fluxo_aresta))]
        for cmh in range(len(demanda_caminho)):
            for e in demanda_caminho[cmh]:
                fluxo_aresta[e] += G.demandas[cmh].routing_value
        for e in range(len(fluxo_aresta)):
            if fluxo_aresta[e] > G.array_max_cap[e]+G.arestas[e].pre_installed_capacity:
                return None
        return fluxo_aresta

    def __add__(self, other):
        while True:
            filho1 = []
            filho2 = []
            sz = len(self.demanda_caminho)
            p1 = random.randint(1,int(sz/2))
            p2 = random.randint(int(sz/2+1),sz-2)
            ord = []
            for i in range(len(self.demanda_caminho)):
                if i<=p1 or i>p2:
                    ord.append(0)
                elif i<=p2:
                    ord.append(1)

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
        return cromossomo()

    def __init__(self,tipo='gerar',demanda_caminho=None,fluxo_aresta=None,item=None):
        if tipo == 'gerar':
            self.__gera_cromossomo()
        if tipo == 'receber':
            self.demanda_caminho = demanda_caminho
            self.fluxo_aresta = fluxo_aresta
        if tipo == 'atribuir':
            self.demanda_caminho = item.demanda_caminho
            self.fluxo_aresta = item.fluxo_aresta
            self.custo = item.custo
            return
        self.__calcula_custo()
        # self.__imprime_cromossomo()
        #self.__busca_local()
        #print('custo:',self.custo,'tam caminhos:',self.soma_tam_caminhos)

class GA:
    taxa_cruzamento = 0.8
    taxa_mutacao = 0.05
    tamanho_populacao = 10
    populacao = None
    melhor_individuo = None
    custo_medio =0.0
    k = [1.0,0.3,1.0,0.3]
    custo_minimo=0

    def __probabilidade_crossover(self,idx1,idx2):
        idx = idx1
        if self.populacao[idx2].custo < self.populacao[idx].custo:
            idx = idx2
        if self.populacao[idx].custo > self.custo_medio and self.custo_minimo < self.custo_medio:
            return self.k[0]*((self.custo_medio - self.custo_minimo)/(self.populacao[idx].custo - self.custo_minimo))
        return self.k[2]

    def __probabilidade_mutacao(self,idx):
        if self.populacao[idx].custo <= self.custo_medio and self.custo_minimo < self.custo_medio:
            return self.k[1]*((self.populacao[idx].custo - self.custo_minimo)/(self.custo_medio - self.custo_minimo))
        return self.k[3]

    def __gera_populacao(self):
        print('gerando populacao')
        self.populacao = []
        for i in range(self.tamanho_populacao):
            self.populacao.append(cromossomo())
            print('gerados',i,'cromossomos')
        print('Populacao gerada')

    def __calcula_dados(self):
        self.custo_medio = 0.0
        self.custo_minimo = 10000000000000.0
        for i in range(len(self.populacao)):
            self.custo_medio += float(self.populacao[i].custo)
            self.custo_minimo = min(self.custo_minimo,self.populacao[i].custo)
        self.custo_medio/=float(len(self.populacao))
        pass

    def __torneio(self,adv=-1):
        lim = len(self.populacao)
        ret = random.randint(0,lim-1)
        for rounds in range(0,3):
            other = random.randint(0,lim-1)
            while other == adv or other == ret:
                other = random.randint(0,lim-1)
            if self.populacao[other].custo < self.populacao[ret].custo:
                ret = other
        return ret

    def __operador_cruzamento(self):
        p = float(random.randint(1,100))/100.0
        qtd = int(len(self.populacao)*0.3)
        prole = []
        while qtd>0:
            parent1 = self.__torneio()
            parent2 = self.__torneio(adv = parent1)
            if p <= self.__probabilidade_crossover(parent1,parent2):
                prole += self.populacao[parent1]+self.populacao[parent2]
            qtd-=1
        for i in range(len(prole)):
            if prole[i].custo < self.melhor_individuo.custo:
                self.melhor_individuo = cromossomo(tipo='atribuir',item=prole[i])
        self.populacao += prole

    def __operador_mutacao(self):
        for e in range(len(self.populacao)):
            p = float(random.randint(1, 100))/100.0
            if p  <= self.__probabilidade_mutacao(e):
                self.populacao[e] = self.populacao[e].mutacao()
        print('Mutação realizada')

    def __torneio_selection(self,vet_idx):
        if len(vet_idx) == 1:
            return 0
        tam = len(vet_idx)
        pos = random.randint(0,tam-1)
        pos1 = random.randint(0,tam-1)
        if self.populacao[pos1].custo < self.populacao[pos].custo:
            pos = pos1
        return pos

    def __selection(self):
        populacao = []
        vet_idx = [i for i in range(len(self.populacao))]
        while len(populacao) < self.tamanho_populacao:
            pos = self.__torneio_selection(vet_idx)
            populacao.append(self.populacao[vet_idx[pos]])
            vet_idx.pop(pos)
        self.populacao = []+populacao
        print('Seleção realizada')

    '''
        def __plot_frente_de_pareto(self,geracao):
        custo_frente = np.array([self.frente[i].custo for i in range(len(self.frente))])
        soma_tam_caminhos_frente = np.array([self.frente[i].soma_tam_caminhos for i in range(len(self.frente))])
        custo = np.array([self.populacao[i].custo for i in range(len(self.populacao))])
        soma_tam_caminhos = np.array([self.populacao[i].soma_tam_caminhos for i in range(len(self.populacao))])
        plt.scatter(soma_tam_caminhos,custo,c=np.array(['blue' for i in range(len(self.populacao))]),label='Outras soluções')
        plt.scatter(soma_tam_caminhos_frente, custo_frente, c=np.array(['red' for i in range(len(self.frente))]),label='Frente de pareto')
        plt.xlabel('Soma dos tamanhos dos caminhos')
        plt.ylabel('Custo')
        plt.title('ANSGA II - Geração '+geracao)
        plt.legend()
        caminho = 'NSGA 2 Figuras/' + 'Geração('+str(geracao)+').png'
        plt.savefig(caminho)
        plt.close()
        #plt.show()
    '''

    def apaga_conteudo(self):
        pass

    def __init__(self):
        tempo_inicial = time.process_time()
        self.__gera_populacao()
        self.frente = []
        geracao = 0
        self.melhor_individuo = cromossomo(tipo='atribuir', item=self.populacao[0])
        for i in range(len(self.populacao)):
            if self.populacao[i].custo<self.melhor_individuo.custo:
                self.melhor_individuo = cromossomo(tipo='atribuir',item=self.populacao[i])
        self.__calcula_dados()
        while time.process_time() - tempo_inicial< 1000:
            print('----', geracao, '----',time.process_time() - tempo_inicial,'s')
            self.__operador_cruzamento()
            self.__calcula_dados()
            self.__operador_mutacao()
            for i in range(len(self.populacao)):
                if self.populacao[i].custo < self.melhor_individuo.custo:
                    self.melhor_individuo = cromossomo(tipo='atribuir', item=self.populacao[i])
            self.__selection()
            print('melhor custo geral', self.melhor_individuo.custo)
            print('custo médio',self.custo_medio)
            print('melhor custo',self.custo_minimo)
            print('-----------------')
            self.__calcula_dados()
            geracao+=1
teste = GA()