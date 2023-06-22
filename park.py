from itertools import permutations
from typing import List
class Interval():
    def __init__(this, start, end, mark):
        this.start = start
        this.end = end
        this.mark = mark
    def __contains__(this, item):
        return this.start <= item and item <= this.end
    def park(this, item):
        out = this.start - 1
        if item < this.mark:
            this.start -= 1
        else:
            this.end += 1
            out = this.end
        this.mark = item
        return out
    def toString(this, showEnds=False):
        out = ""
        if showEnds:
            out += str(this.start)
        out += "▢" * (this.mark - this.start) + "m" + "▢" * (this.end - this.mark)
        if showEnds:
            out += str(this.end)
        if len(out) >= 2:
            out = out[1:-1]
        return out
class ParkingLot():
    def __init__(this, cars = None):
        this.intervals : List[Interval] = []
        this.word = []
        this.isParkingWord = True
        this.park(cars)
    def copy(this):
        return ParkingLot(this.word)
    def parkSingleCar(this, car):
        if car == None:
            return
        this.word.append(car)
        prevInterval = None
        nextInterval = None
        interval = None
        i = 0
        for i in range(len(this.intervals)):
            interval = this.intervals[i]
            prevInterval = None if i == 0 else this.intervals[i-1]
            nextInterval = None if i == len(this.intervals) - 1 else this.intervals[i+1]
            if interval.start > car:
                nextInterval = interval
                break
            if car in interval:
                loc = interval.park(car)
                if nextInterval != None and interval.end + 1 == nextInterval.start:
                    interval.end = nextInterval.end
                    this.intervals.pop(i+1)
                if prevInterval != None and interval.start == prevInterval.end + 1:
                    interval.start = prevInterval.start
                    this.intervals.pop(i-1)
                return loc
            if i == len(this.intervals) - 1:
                prevInterval = this.intervals[-1]
                i += 1
        interval = Interval(car, car, car)
        this.intervals.insert(i, interval)
        if nextInterval != None and interval.end + 1 == nextInterval.start:
                    interval.end = nextInterval.end
                    this.intervals.pop(i+1)
        if prevInterval != None and interval.start == prevInterval.end + 1:
            interval.start = prevInterval.start
            this.intervals.pop(i-1)
        return car
    def park(this, cars):
        if cars == None:
            return
        if type(cars) == int:
            this.parkSingleCar(cars)
        else:
            for car in cars:
                this.parkSingleCar(car)
    def isOmega(this):
        return len(this.intervals) == 1 and this.intervals[0].start == 1
    def toString(this, expandIntervals=False, pad=-1):
        if len(this.intervals) == 0:
            return "Empty Lot"
        out = ""
        for i in range(len(this.intervals)):
            if expandIntervals and i < len(this.intervals) - 1:
                out += this.intervals[i].toString(showEnds=False)
                out += "." * (this.intervals[i + 1].start - this.intervals[i].end - 1)
            elif expandIntervals:
                out += this.intervals[i].toString(showEnds=False)
            else:
                out += this.intervals[i].toString(showEnds=True)
        if len(this.intervals) > 0 and pad > this.intervals[-1].end:
            out += "." * (pad - this.intervals[-1].end)
        return out[:-1]
def swap(w: List[int], i: int, j: int) -> List[int]:
    i -= 1
    j -= 1
    temp = w[i]
    w[i] = w[j]
    w[j] = temp
    return w
def get_descents(w: List[int]) -> List[int]:
    out = []
    for i in range(len(w) - 1):
        if w[i] > w[i+1]:
            out.append(i + 1)
    return out
def get_reduced_words(w: List[int]) -> List[int]:
    w = w.copy()
    des = get_descents(w)
    if len(des) == 0:
        return [[]]
    out = []
    for i in range(len(des)):
        swap(w, des[i], des[i] + 1)
        out += [[des[i]] + rw for rw in get_reduced_words(w)]
        swap(w, des[i], des[i] + 1)
    return out
def findParkingReducedWords(w: List[int], lot: ParkingLot = None, permLength = -1):
    if permLength == -1:
        permLength = l(w)
    if lot == None:
        lot = ParkingLot()
    out = []
    for des in get_descents(w):
        newLot: ParkingLot = lot.copy()
        newLot.park(des)
        if newLot.intervals[0].start < 1 or newLot.intervals[-1].end > permLength:
            continue
        wSwitch = swap(w.copy(), des, des + 1)
        if len(get_descents(wSwitch)) == 0:
            out.append([des])
        else:
            out += [[des] + prw for prw in findParkingReducedWords(wSwitch, newLot, permLength)]
    return out
def makeParkingReducedWordTree(w: List[int], lot: ParkingLot = None, permLength = -1):
    if permLength == -1:
        permLength = l(w)
    if lot == None:
        lot = ParkingLot()
    out = {"perm": str(w), "lot":lot.toString(expandIntervals=True, pad=permLength), "tree":[]}
    for des in get_descents(w):
        newLot: ParkingLot = lot.copy()
        newLot.park(des)
        if newLot.intervals[0].start < 1 or newLot.intervals[-1].end > permLength:
            continue
        wSwitch = swap(w.copy(), des, des + 1)
        wSwitchTree = makeParkingReducedWordTree(wSwitch, newLot, permLength)
        if len(get_descents(wSwitch)) == 0 or len(wSwitchTree["tree"]) > 0:
            out["tree"] += [[des, wSwitchTree]]
    return out
def makeParkingReducedWordTree2(w: List[int], lot: ParkingLot = None, permLength = -1):
    if permLength == -1:
        permLength = l(w)
    if lot == None:
        lot = ParkingLot()
    out = {"perm": str(w), "word":[], "tree":[]}
    for des in get_descents(w):
        newLot: ParkingLot = lot.copy()
        newLot.park(des)
        if newLot.intervals[0].start < 1 or newLot.intervals[-1].end > permLength:
            continue
        wSwitch = swap(w.copy(), des, des + 1)
        wSwitchTree = makeParkingReducedWordTree2(wSwitch, newLot, permLength)
        if len(get_descents(wSwitch)) == 0 or len(wSwitchTree["tree"]) > 0:
            out["tree"] += [[des, wSwitchTree["tree"]]]
    return out
def S(n):
    return [list(perm) for perm in permutations([i for i in range(1,n+1)])]
def l(perm):
    out = 0
    for i in range(len(perm)):
        for j in range(i, len(perm)):
            if (perm[i] > perm[j]):
                out += 1
    return out
def insertAtBeg(w, n):
    return [i for i in range(1,n+1)] + [wi+n for wi in w]
def permFromCode(code: List[int]):
    out = []
    for codeNum in code:
        out.append(codeNum + 1 + len([i for i in out if i <= codeNum + 1]))
    for i in range(1,max(out)):
        if not i in out:
            out.append(i)
    return out
def printAll(N): 
    for perm in S(N):
        if l(perm) < N - 1:
            continue
        print("perm: " + str(perm))
        rws = get_reduced_words(perm)
        nonomegaPerms = [rw for rw in rws if not ParkingLot(rw).isOmega()]
        omegaPerms = [rw for rw in rws if ParkingLot(rw).isOmega()]
        #print("nonomega rws: " + str(nonomegaPerms))
        print("omega rws: " + str(omegaPerms))
        if len(omegaPerms) == 0:
            print("OHNO")
            print(perm)
            break
        for oP in omegaPerms:
            loP = list(oP)
            loP.reverse()
            if not ParkingLot(loP).isOmega():
                print("NOT OMEGA " + str(loP))
def printPermToHTML(w):
    print(str(makeParkingReducedWordTree(w)).replace("\'", "\"").replace("\"[", "[").replace("]\"","]"))
def printPermToHTML2(w):
    print(str(makeParkingReducedWordTree2(w)).replace("\'", "\"").replace("\"[", "[").replace("]\"","]"))
printPermToHTML2([2,1])
#printPermToHTML2([3,2,1])
#printPermToHTML([3,2,1])
#printPermToHTML2(insertAtBeg(permFromCode([8,8]),1))
'''print(findParkingReducedWords([4,3,2,1]))
print(findParkingReducedWords([1,4,5,6,7,8,9,2,3]))
print(findParkingReducedWords([3,4,5,6,7,8,9,1,2]))
rect = [3,4,5,6,7,8,9,1,2]
for i in range(1,10):
    w = permFromCode([i,i])
    for j in range(1,2):
        print("i: " + str(i) + " j: " + str(j))
        #print(findParkingReducedWords(insertAtBeg(rect,j)))
        print(len(findParkingReducedWords(insertAtBeg(w,j))))
        print(findParkingReducedWords(insertAtBeg(w,j)))
print(permFromCode([5,5]))
print(findParkingReducedWords(permFromCode([5,5])))'''