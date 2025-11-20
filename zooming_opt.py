import numpy as np

def zooming(n, f_real, L, low, high, N):
    A = list(range(0, n))  # 注意：这里应该是 range(0, n)，不是 n-1
    I = [int((n-1)/4), int(3*(n-1)/4)]  # 修正索引
    intv = [low, low + (high-low)//2, low + (high-low)//2 + 1, high]
    count = 0
    
    while count < N:
        ub = np.zeros(n) - 100
        lb = np.zeros(n) - 100
        ub_max = []
        count += 1
        mu_max = max([f_real[i] for i in I])
        a_max = I[np.argmax([f_real[i] for i in I])]   
        
        for a in A:
            ub[a] = min(f_real[i] + L * abs(a - i) for i in I)
            lb[a] = max(f_real[i] - L * abs(a - i) for i in I)
        
        intv_new = [range(intv[2*i], intv[2*i+1]+1) for i in range(len(intv)//2)]
        for i in range(len(intv_new)):
            if len(intv_new[i]) >= 3:
                ub_max.append(max(ub[j] for j in intv_new[i]))
            else:
                ub_max.append(-10000)

        if not ub_max:
            break
        
        i_new = np.argmax(ub_max)        
        a_new_1 = (intv[2*i_new] + 3*intv[2*i_new+1]) // 4
        a_new_2 = (3*intv[2*i_new] + intv[2*i_new+1]) // 4
        I.extend([a_new_1, a_new_2])
        I.sort()
        
        intv.extend([a_new_1, a_new_2])
        intv.sort()
        
        # 删除区间
        del_intv = []
        for i in range(len(intv)//2 - 1, -1, -1):   
            temp = max([ub[j] for j in range(intv[2*i], intv[2*i+1]+1)])
            if temp <= mu_max:
                del_intv.extend([2*i+1, 2*i])
                
        for i in sorted(del_intv, reverse=True):  # 从后往前删除
            del intv[i] 

    print("mu_max=", mu_max, "a_max=", a_max, '\n')
    return mu_max, a_max  # 建议返回结果