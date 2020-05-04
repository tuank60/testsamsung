import math

def calculateDistance(txPower,rssi):
    if rssi == 0:
        return -1.0
    ratio = rssi * 1.0 / txPower
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        accuracy = 0.89976 * math.pow(ratio, 7.7095) + 0.111
        return accuracy

def Wn():
    dn_bottom = 12.7
    # dn_bottom = 3.175
    FLUID_HEIGHT = 300
    # FLUID_HEIGHT = 0.0762
    k_h_prod = 0.8105869167082297
    C38 = 1.1341
    C39 = 3.9365
    C40 = 5.9352
    m = C40 - 0.4324 * math.log10(dn_bottom) + 0.5405 * math.log10(FLUID_HEIGHT)
    print(m)
    tu = C39 + 2 * math.log10(dn_bottom) - math.log10(k_h_prod)
    print(tu)
    A = tu/m
    print("A="+str(A))
    print(pow(A,m))
    mu = 2 * math.log10(dn_bottom) + 0.5 * math.log10(FLUID_HEIGHT)- 0.74*pow(A,m)
    print(mu)
    print(C38 * pow(10,mu))
    # print(C38 * pow(10, 2 * math.log10(self.dn_bottom(i)) + 0.5 * math.log10(self.FLUID_HEIGHT) - 0.74 * pow(
        # (C39 + 2 * math.log10(self.dn_bottom(i)) - math.log10(self.k_h_prod())) / m, m)))
    # print(math.log10(10))
    # print(pow(10,-3.1))
if __name__ == '__main__':
    # print(calculateDistance(-85,-95))
    # calculateDistance(-85,-95)
    Wn()


