from gurobipy import *
from grafo_pronto import grafo
from visual import visual
G = grafo(r'brain.txt')
modelo = Model('telecom')
x = modelo.addVars(len(G.nos),len(G.nos),len(G.demandas),vtype=GRB.BINARY,name='fluxo')
print('matriz x definida')
y = modelo.addVars(len(G.nos),len(G.nos),G.tam_capacidade,vtype=GRB.BINARY,name='modulo')
print('matriz y definida')
modelo.ModelSense = GRB.MINIMIZE
obj0 = LinExpr()
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for t in range(G.tam_capacidade):
            obj0 += y[i,j,t] * G.matriz_adjacencia_custo[i][j][t]

# modelo.setObjective(obj0,sense=GRB.MINIMIZE)
modelo.setObjectiveN(obj0,0)

obj1 = LinExpr()
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for k in range(len(G.demandas)):
            obj1 += x[i,j,k]
modelo.setObjectiveN(obj1,1)
print('objetivos definidos')
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        fluxo = LinExpr()
        for k in range(len(G.demandas)):
            fluxo += x[i,j,k] * G.matriz_adjacencia_demanda[i][j][k]
        capacidade = LinExpr()
        for t in range(len(G.matriz_adjacencia_capacidade[i][j])):
            capacidade+= y[i,j,t] * G.matriz_adjacencia_capacidade[i][j][t]
        modelo.addLConstr(fluxo <= capacidade)
print('restrição 1 definida')
for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    for i in range(len(G.nos)):
        if i == ok or i == dk:
            continue
        entrando = LinExpr()
        for j in range(len(G.nos)):
            if j == dk or j == i:
                continue
            entrando += x[j,i,k]
        saindo = LinExpr()
        for j in range(len(G.nos)):
            if j == ok or j == i:
                continue
            saindo += x[i,j,k]
        modelo.addLConstr(entrando == saindo)
print('restrição 2 definida')
for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    entrando = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        entrando+= x[j,ok,k]
    saindo = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        saindo += x[ok,j,k]
    modelo.addLConstr(entrando == 0)
    modelo.addLConstr(saindo == 1)
print('restrição 3 definida')
for k in range(len(G.demandas)):
    ok = G.demandas[k].idx_i
    dk = G.demandas[k].idx_j
    entrando = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        entrando+= x[j,dk,k]
    saindo = LinExpr()
    for j in range(len(G.nos)):
        if j == dk or j == ok:
            continue
        saindo += x[dk,j,k]
    modelo.addLConstr(entrando == 1)
    modelo.addLConstr(saindo == 0)
print('restrição 4 definida')
modelo.Params.timeLimit = 3600.0
modelo.optimize()

vx = [[[0 for k in range(len(G.demandas))] for j in range(len(G.nos))] for i in range(len(G.nos))]

for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for k in range(len(G.demandas)):
            vx[i][j][k]=int(x[i,j,k].getAttr(GRB.Attr.X))


vy = [[[0 for k in range(G.tam_capacidade)] for j in range(len(G.nos))] for i in range(len(G.nos))]
for i in range(len(G.nos)):
    for j in range(len(G.nos)):
        for t in range(len(G.matriz_adjacencia_capacidade[i][j])):
            vy[i][j][t] = int(y[i,j,t].getAttr(GRB.Attr.X))

vis = visual(G,vx,vy)
custo = modelo.getObjective(0)
hops = modelo.getObjective(1)
print('custo gurobi::::',custo.getValue())
print('hops gurobi::::',hops.getValue())

