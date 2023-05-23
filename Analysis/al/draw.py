""" @File   : test

    @Author : BabyMuu
    @Time   : 2023/2/4 13:05
"""
from Analysis.al.Apriori import Apriori

from utils.driver import conn

cur = conn.cursor()
cur.execute("select score from scores_rule")
rule_order = cur.fetchall()
dataset = []
for i in rule_order:
    dataset.append(i[0].split(','))

a = Apriori(dataset)
L, support_ = a.apriori(0.5)
e = 0
# for fre in L:
#     print(f'{e + 1}-项集: {fre}')
#     e += 1
rules = a.gen_rate_rules(L, support_)

def process(rule):
    rule = list(rule)
    rule[:2] = list(map(list, rule[:2]))
    rule[0] = "-".join(rule[0])
    rule[1] = "-".join(rule[1])
    rule[2] = round(rule[2], 2)
    return rule

rules = list(map(process, rules))
print(rules)

def draw():

    import matplotlib.pyplot as plt  # 导入 Matplotlib 工具包

    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['figure.figsize'] = (16, 9)
    import networkx as nx  # 导入 NetworkX 工具包

    # 问题 2：无向图的最短路问题（司守奎，数学建模算法与应用，P43，例4.3）
    G2 = nx.DiGraph()  # 创建：空的 有向图

    for i in rules:
        G2.add_edge(i[0], i[1], weight=i[2])

    pos = nx.spring_layout(G2)  # 用 FR算法排列节点
    nx.draw(G2, pos, with_labels=True, alpha=0.5)
    labels = nx.get_edge_attributes(G2, 'weight')
    nx.draw_networkx_edge_labels(G2, pos, edge_labels=labels)
    plt.show()
