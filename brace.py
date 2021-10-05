
if __name__ == '__main__':

    F = ""
    with open('c:\\tcc\\pac.ic') as fd:
        F = fd.read()

    # --------------------------------------------------------------
    # --- block --- str, slc, mlc, ppd ---

    F2 = []
    buf = ""
    mode = 0
    for ch in F:
        if mode == 0:
            if ch == "\"":
                if len(buf) > 0:
                    F2.append(buf)
                buf = ""
                mode = 1
                buf += ch
            elif ch == "*" and len(buf)>0 and buf[-1] == '/':
                buf = buf[0:-1]
                if len(buf) > 0:
                    F2.append(buf)
                buf = ""
                mode = 2
                buf += "/*"
            elif ch == '/' and len(buf)>0 and buf[-1] == '/':
                buf = buf[0:-1]
                if len(buf) > 0:
                    F2.append(buf)
                buf = ""
                mode = 3
                buf += '//'
            elif ch == '#':
                if len(buf) > 0:
                    F2.append(buf)
                buf = ""
                mode = 4
                buf += ch
            else:
                buf += ch
        elif mode == 1:
            if ch == "\"" and buf[-1] != "\\":
                buf += ch
                F2.append(buf)
                buf = ""
                mode = 0
            else:
                buf += ch
        elif mode == 2:
            if ch == '/' and len(buf)>0 and buf[-1] == '*':
                buf += ch
                F2.append(buf)
                buf = ""
                mode = 0
            else:
                buf += ch
        elif mode == 3:
            if ch == '\n':
                buf += ch
                F2.append(buf)
                buf = ""
                mode = 0
            else:
                buf += ch
        elif mode == 4:
            if ch == '\n' and len(buf) > 0 and buf[-1] != '\\':
                buf += ch
                F2.append(buf)
                buf = ""
                mode = 0
            else:
                buf += ch

    # --------------------------------------------------------------
                
    if mode != 0:
        raise Exception('Unclosed str/slc/mlc/ppd at and of file')
    else:
        F2.append(buf)

    # --------------------------------------------------------------
    # --- block brackets

    F3 = []
    buf = ""
    br = 0
    for t in F2:
        if t[0] in ['#', '\"'] or t[:2] in ['//', '/*']:
            if br == 0:
                if buf:
                    F3.append(buf)
                buf = ""
                F3.append(t)
            else:
                buf += t
        else:
            for ch in t:
                if ch == '(':
                    if br == 0:
                        if buf:
                            F3.append(buf)
                        buf = ''
                        buf += ch
                    else:
                        buf += ch
                    br += 1
                elif ch == ')':
                    br -= 1
                    buf += ch
                    if br == 0:
                        F3.append(buf)
                        buf = ''
                    elif br < 0:
                        raise Exception('Too much \')\' ')
                else:
                    buf += ch

    for x in F2:
        print( "%s\n-------------" % x)
    exit(0)
    # --------------------------------------------------------------

    if br != 0:
        raise Exception('Non matching count of \'(\' and \')\' at and of file')
    else:
        F3.append(buf)

    # --------------------------------------------------------------
    # --- split code blocks by \n

    F4 = []
    for t in F3:
        if t[0] in ['#', '\"', '('] or t[:2] in ['//', '/*'] or t.strip() == '':
            F4.append(t)
        else:
            for x in t.split('\n'):
                F4.append(x+'\n')
            F4[-1] = F4[-1][:-1]

    # --------------------------------------------------------------
    # --- join block so only one code block followed by \n is new block

    F5 = []
    buf = ''
    start_pos = None
    end_pos = None
    for t in F4:
        if t[0] == '#' or t[:2] in ['//', '/*'] or t.strip() == '':  # comments
            buf += t
        else:
            if start_pos is None:
                start_pos = len(buf)
            buf += t
            end_pos = len(buf)
            if buf[-1] == '\n':
                end_pos -= 1
        if start_pos is not None and t[-1] == '\n':
            F5.append([start_pos, end_pos, buf])
            buf = ''; start_pos = end_pos = None

    # --------------------------------------------------------------
    # --- replace start_pos with tabs and move end_pos to left

    for t in F5:
        tabs = 0
        while t[2][t[0]] == '\t':
            tabs += 1
            t[0] += 1
        t[0] = tabs
        while t[2][t[1]-1] in ['\n', '\t', ' ']:
            t[1] -= 1

    # --------------------------------------------------------------
    # --- print 

    F5.append(F5[0])

    for n in range(1, len(F5)):
        diff = F5[n][0] - F5[n - 1][0]
        if diff == 0:
            sep = ';'
        elif diff > 0:
            sep = ' ' + '{' * diff
        else:
            sep = ';' + ' ' + '}' * (-diff)

        print('%s%s%s' % (F5[n-1][2][:F5[n-1][1]], sep, F5[n-1][2][F5[n-1][1]:]), end='')
