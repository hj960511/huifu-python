# 实现打印 支持单个 或多个 对象数据的 d 函数
def d(obj, *args):
    print(obj.__dict__)
    for arg in args:
        print(arg.__dict__)

