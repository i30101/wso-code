c = 1
y = 1
l = 0
i = 0
n = 1
d = 9
e = 1
r = 1
g = 0
z = 0

def condition(ct, yt, lt, it, nt, dt, et, rt, gt, zt) -> bool:
    return (
        ct*10000000 + yt*1000000 + lt*100000 + it*10000 + nt*1000 + dt*100 + et*10 + rt +
        et*10000000 + nt*1000000 + et*100000 + rt*10000 + gt*1000 + it*100 + zt*10 + et
        ==
        dt*10000000 + rt*1000000 + it*100000 + lt*10000 + lt*1000 + it*100 + nt*10 + gt
        and len([ct, yt, lt, it, nt, dt, et, rt, gt, zt]) != len(set([ct, yt, lt, it, nt, dt, et, rt, gt, zt]))
    )


def find_answer():
    for ct in range(c, 10):
        for yt in range(y, 10):
            for lt in range(l, 10):
                for it in range(i, 10):
                    for nt in range(n, 10):
                        for et in range(e, 10):
                            for rt in range(r, 10):
                                for gt in range(g, 10):
                                    for zt in range(z, 10):
                                        if condition(ct, yt, lt, it, nt, d, et, rt, gt, zt):
                                            print(ct, yt, lt, it, nt, d, et, rt, gt, zt)
                                            return
                                        
find_answer()