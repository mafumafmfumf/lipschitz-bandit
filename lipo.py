import numpy as np

def LIPO(n, f_real, L, low, high, N):
    A=list(range(0,n-1))
    I = [int((n-1)/4), int(3*(n-1)/4)]
    R=[i for i in A if i not in I]
    count=0
    while count<N:
        ub=np.zeros(n)-np.inf
        lb=np.zeros(n)-np.inf
        count+=1
        mu_max = max([f_real[i] for i in I])
        a_max = I[np.argmax([f_real[i] for i in I])]
        for a in R:
            ub[a]=min(f_real[i]+L*abs(a-i) for i in I)
            lb[a]=max(f_real[i]-L*abs(a-i) for i in I)
        if max(ub)<=mu_max:
            break
        
        R = []
        
        for i in range(n):
            if ub[i]<=mu_max:
                ub[i]=-np.inf
                lb[i]=-np.inf
            else: 
                R.append(i)

        a=random.choice(R)
        I.append(a)           
        R.remove(a)
        print("mu_max=",mu_max,"a_max=",a_max, '\n')