t = input()
a = list(map(int, input().split()))
chan = 0
sumc = 0
le = 0
suml = 0
for i in range(len(a)):
    if a[i] % 2 == 0:
        chan += 1
        sumc += a[i]
    else:
        le += 1
        suml += a[i]
print(chan, le, sumc, suml, sep='\n')
