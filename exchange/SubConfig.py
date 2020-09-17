from common.Common import Common


class SubConfig:
    trade_kind = Common.futures   # 交易类型（币币、交割、永续）
    symbol = None  # 币种
    contract_type = None  # 合约类型
    frequency = None  # 频率
    instrument_id = None  # 币种编号

    def __init__(self, symbol, contract_type, frequency):
        self.symbol = symbol
        self.contract_type = contract_type
        self.frequency = frequency

    def __eq__(self, other):
        # print(self.props())
        # print(other.props())
        return self.__class__ == other.__class__ and self.props() == other.props()

    def props(self):
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                pr[name] = value
        return pr


if __name__ == '__main__':
    l = []
    subA = SubConfig(1, 1, 1)
    l.append(subA)
    subB = SubConfig(1, 1, 1)
    print(id(subA))
    print(id(subB))
    print(subA == subB)
    print(subB in l)
    if subB in l:
        l.remove(subB)
    print(l)
