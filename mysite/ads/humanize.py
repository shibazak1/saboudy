
def neutralize(count):

    fcount = float(count)
    k = 1024 # defin the size of kilo byte
    m = k*k  # defin //     //   miga byte
    g = m*k  # giga byte


    if fcount < k:
        return str(count)+'B'
    elif fcount >= k and fcount < m:
        return str(fcount/k)+'KB'
    elif fcount >=m and fcount <g:
        return str(fcount/m)+'MB'
    return str(fcount/g)+'GB'

