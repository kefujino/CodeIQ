# coding: utf-8
# Python2


import fileinput 
import Queue 
import copy 

debug = False 
dict = {} 
index = 0 

# 現在の、1 つ前の手順の状態を保持するクラス
class State: 
    def __init__(self,oTable,prev,cnt): 
        self.table = oTable 
        self.prev = prev 
        self.cnt = cnt

# サーバーから与えられる初期値を取得
def initial_input(): 
    for line in fileinput.input(): 
        tokens = map(int, line.strip().split()) 
    dolls = tokens[0] 
    moves = tokens[1] 
    return (dolls,moves)

# 最も大きいマトリョーシカのサイズを取得
def getMat(num): 
    res = 0 
    while(num != 0): 
        num /= 10 
        res += 1 
    return res 

# 初期配置を作成
def newTable(m): 
    tA,tB,tC = 0,0,0 
    for i in range(0,m): 
        tA += pow(10,i) 
    t = [tA,tB,tC] 
    return t 

# 過去に出たパターンを記憶(重複なし)
def memoTable(cTable): 
    global dict 
    global index 
    
    cTable.sort(key = int) 
    for val in dict: 
        if cTable == dict[val]: 
            return True 
    else: 
        dict[index] = cTable 
        index += 1 

# マトリョーシカ移動後のテーブルの状態を更新
def makeT(table, frm ,to): 
    a = getMat(table[frm]) 
    b = getMat(table[to]) 
    if(debug):print "Now makeT : "+str(table) 
    if (a>b): 
        table[to] += pow(10,a-1) 
        table[frm] -= pow(10,a-1) 
    return table 


def main(): 
    global count 
    m,n = initial_input() 
    ans = 0 
    table = newTable(m) 
    
    # 現在の状態はスタックで保持する
    q = Queue.LifoQueue() 
    q.put(State(table,-1,0)) 
    
    # スタックが空になったら移動終了
    while(q.qsize()>0): 
        s = q.get() 
        table = s.table 
        prev = s.prev 
        cnt = s.cnt 
        
        #現在のパターンが過去のパターンに含まれる場合は探索終了
        if memoTable(copy.deepcopy(table)) is True: 
            continue

        #移動回数 n を越えた場合は探索終了
        if(cnt >= n): 
            ans += 1 
            continue 
        
        # どのテーブルにあるマトリョーシカを動かすかを決めるループ
        for frm in range(0,3): 
            if(debug):print "frm, prev = "+str(frm) + ", "+str(prev) 
           
            # 1 前の手順で移動したマトリョーシカの乗ってるテーブルは対象から除外
            if frm == prev: 
                continue

            # マトリョーシカが乗っていないテーブルも対象から除外
            if table[frm] == 0: 
                continue 
            
            for to in range(0,3): 
                if frm == to: 
                    continue

                #現在の状態を引数に、移動後の状態を表す新しいテーブルを作成
                nTable = makeT(copy.deepcopy(table), frm ,to)

                #移動した場合は、今の状態をスタックに格納し、次の手順に進む
                q.put(State(copy.deepcopy(nTable), to , cnt+1))
    print ans
    
if __name__ == '__main__': 
    main()