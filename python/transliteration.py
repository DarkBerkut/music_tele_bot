from collections import defaultdict

moveMap = defaultdict(list)

for line in open("data/ru-en.translit.txt"):
    parts = line.split("\t")
    p = float(parts[1])
    fromTo = parts[0].split("|")
    fr = fromTo[0]
    to = fromTo[1]
    moveMap[fr].append((to, p))

maxLen = max([len(x) for x in moveMap])

def check(s1, s2, i1=0, i2=0):
    if i1 == len(s1) and i2 == len(s2):
        return 0
    results = []
    for l in range(1, maxLen + 1):
        prefix = s1[i1:i1 + l]
        for (to, weight) in moveMap[prefix]:
            if s2[i2:].startswith(to):
                res = check(s1, s2, i1 + l, i2 + len(to))
                if res is not None:
                    results.append(res + weight)
    if results:
        return min(results)
    else:
        return None