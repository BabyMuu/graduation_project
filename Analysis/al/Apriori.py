""" @File   : al
    
    @Author : BabyMuu
    @Time   : 2023/2/4 12:56
"""


class Apriori:
    def __init__(self, dataset):
        self.dataset = dataset

    def create_c1(self):
        """构建数据集"""
        C1 = []
        for transaction in self.dataset:
            # 获取每一个事物
            for item in transaction:
                # 获取每一个项
                if not [item] in C1:
                    C1.append([item])
        C1.sort()
        return list(map(frozenset, C1))

    def scan_dataset(self, C_k, min_support):
        """
        数据集扫描, 获取每一个项集出现的次数, 并计算相应的支持度
        :param C_k: k-项集 collection of k
        :param min_support: 最小支持度
        :returns 满足设定支持度条件的项集, 每个项集对应的支持度
        """
        ss_cnt = {}  # 键：项集  值：项集出现的次数
        # 看项集中的每一个项在数据集中出现的次数
        for transaction in self.dataset:
            for item in C_k:
                if item.issubset(transaction):
                    if not item in ss_cnt:
                        ss_cnt[item] = 1
                    else:
                        ss_cnt[item] += 1
        sat_list = []
        num_items = len(list(self.dataset))  # 总的事务数量
        support_set = {}  # 键:项集 值: 支持度
        for key in ss_cnt:
            support = ss_cnt[key] / num_items  # 计算支持度
            if support >= min_support:
                sat_list.append(key)  # 如果符合条件, 到时候返回给下一步
            support_set[key] = support  # 保存当前结果的支持度
        return sat_list, support_set

    @staticmethod
    def apriori_gen(L_k, k):
        """ 项集拼接, 生成新的 C_k
        当传入项集为1-项集时
            所有项集都可过 L_1 == L_2 的条件:
                原理: 1-项集[:k-2] 均为空 空==空恒成立
                即 所有 1-项集都会与其他项集相互拼接
        当传入项集为k-项集时: (k > 1)
            当且仅当除最后一项不同外其余均相同时:
                才将两个项集进行拼接
        当存在项集可以拼接时, 返回有效数据
            否则返回空, ===> 结束算法
        """
        stitching_item_sets = []
        len_lk = len(L_k)
        for i in range(len_lk):
            for j in range(i + 1, len_lk):
                L_1 = list(L_k[i])[:k - 2]
                L_2 = list(L_k[j])[:k - 2]
                if L_1 == L_2:  # 如果两个项集前缀相同
                    stitching_item_sets.append(L_k[i] | L_k[j])
        return stitching_item_sets

    def apriori(self, min_support=0.5):
        """算法入口"""
        c1 = self.create_c1()  # 生成1-项集数据
        # 获取1-项集 项集列表 及对应支持度集合
        L1, support_set = self.scan_dataset(c1, min_support)
        L = [L1]  # l1 一项集  l2 二项集 。。。
        k = 2
        while len(L[k - 2]) > 0:
            C_k = self.apriori_gen(L[k - 2], k)  # 生成 k-项集数据
            # 获取 k-项集 项集列表, 及对应支持度集合
            LK, support_k = self.scan_dataset(C_k, min_support)
            # 更新支持度集合
            support_set.update(support_k)
            # 总项集列表扩充
            L.append(LK)
            # 项集数 + 1
            k += 1
        # 返回数据所能展现的项集次数的项集列表, 及每一个项集对应的支持度集合
        return L, support_set

    def gen_rate_rules(self, L, support_set, min_conf=0.5):
        """置信度"""
        rule_list = []
        for i in range(1, len(L)):  # 遍历每一个k-项集:
            for fre_set in L[i]:  # 遍历K-项集中的项集
                H_1 = [frozenset([item]) for item in fre_set]  # 获取 1-项集
                self.rules_from_conseq(fre_set, H_1, support_set, rule_list, min_conf)
        return rule_list

    def rules_from_conseq(self, fre_set, H_k, support_set, rule_list, min_conf):
        k = len(H_k[0])  # k-项集 ==> k
        while len(fre_set) > k:
            H_k = self.cal_conf(fre_set, H_k, support_set, rule_list, min_conf)
            if len(H_k) > 1:  # 如果k+1-项集中有两个及以上个项集
                self.apriori_gen(H_k, k + 1)  # 构建k+1-项集
                k += 1
            else:
                break

    @staticmethod
    def cal_conf(fre_set, H, support_set, rule_list, min_conf, printable=False):
        """计算当前k-项集中满足置信度条件的项集"""

        def _print(*args, **kwargs):
            if printable:
                print(*args, **kwargs)

        _print(f'{fre_set}'.center(50, "-"))
        sta_list = []  # 满足条件的k+1-项集列表
        for item in H:
            # 计算置信度
            conf = support_set[fre_set] / support_set[fre_set - item]  # p(xy) / p(y)  == p(x | y)
            if conf >= min_conf:  # 如果满足条件
                # 打印结果
                _print(fre_set - item, '-->', item, 'conf:', conf)
                # 置信度集合扩充, 所有项集对应置信度
                rule_list.append((fre_set - item, item, conf))
                # k+1-项集满足规则的集合扩充
                sta_list.append(item)
        _print()
        return sta_list


if __name__ == '__main__':
    dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    a = Apriori(dataset)
    L, support_ = a.apriori()
    e = 0
    for fre in L:
        print(f'{e + 1}-项集: {fre}')
        e += 1
    rules = a.gen_rate_rules(L, support_)
    print(rules)
