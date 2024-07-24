from functools import cmp_to_key
def sum(a):
    tong = 0
    for i in range(len(a)):
        if i == 0 or i == 1:
            tong += a[i] * 2
        else: tong += a[i]
    return tong / (len(a) + 2)
class Sinh_vien:
    def __init__(self, s, a, i):
        if(i < 10): self.ma = 'HS0' + str(i)
        else: self.ma = 'HS' + str(i)
        self.s = s
        self.a = a
    def Get_a(self):
        return self.a
    def Get_s(self):
        return self.s
    def Get_ma(self):
        return self.ma
Ds = []

def cmp(x, y):
    if (sum(x.Get_a()) != sum(y.Get_b())):
        return sum(x.Get_a()) != sum(y.Get_b())
    else:
        return x.Get_s() < y.Get_s()

for i in range(int(input())):
    s = input()
    a = list(map(float, input().split()))
    S = Sinh_vien(s, a, i + 1)
    Ds.append(S)
Ds.sort(key = lambda x: (-sum(x.Get_a()), x.Get_ma()))
for i in range(len(Ds)):
    print(Ds[i].ma, Ds[i].s, '%.1f' % sum(Ds[i].a), end=' ')
    if sum(Ds[i].a) >= 9: print('XUAT SAC')
    elif sum(Ds[i].a) < 9  and sum(Ds[i].a) >= 8: print('GIOI')
    elif sum(Ds[i].a) < 8 and sum(Ds[i].a) >= 7: print('KHA')
    elif sum(Ds[i].a) < 7 and sum(Ds[i].a) >= 5: print('TB')
    else: print('YEU')



