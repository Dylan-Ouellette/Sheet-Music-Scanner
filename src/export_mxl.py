
from music21 import configure, stream, meter, key, note, clef


MAX_HORIZONTAL_DISTANCE = 64

TREBLE_SYMBOL = "treble"
BASS_SYMBOL = "bass"

FLAT_SYMBOL = "flat"
SHARP_SYMBOL = "sharp"
NATURAL_SYMBOL = "natual"

TIME_CUT_SYMBOL = "2/2c time"
TIME_C_CYMBOL = "4/4c time"
TIME_24_SYMBOL = "2/4 time"
TIME_34_SYMBOL = "3/4 time"
TIME_38_SYMBOL = "3/8 time"
TIME_44_SYMBOL = "4/4 time"
TIME_68_SYMBOL = "6/8 time"

TIME_SYMBOLS = [
    TIME_CUT_SYMBOL,
    TIME_C_CYMBOL,
    TIME_24_SYMBOL,
    TIME_34_SYMBOL,
    TIME_38_SYMBOL,
    TIME_44_SYMBOL,
    TIME_68_SYMBOL
]

SYMBOL_DICTIONARY = {
    TREBLE_SYMBOL: clef.TrebleClef(),
    BASS_SYMBOL: clef.BassClef(),
    FLAT_SYMBOL: "b",
    SHARP_SYMBOL: "#",
    NATURAL_SYMBOL: "",
    TIME_CUT_SYMBOL: meter.TimeSignature("2/2"),
    TIME_C_CYMBOL: meter.TimeSignature("4/4"),
    TIME_24_SYMBOL: meter.TimeSignature("2/4"),
    TIME_34_SYMBOL: meter.TimeSignature("3/4"),
    TIME_38_SYMBOL: meter.TimeSignature("3/8"),
    TIME_44_SYMBOL: meter.TimeSignature("4/4"),
    TIME_68_SYMBOL: meter.TimeSignature("6/8")
}


def export(bars, outputFormat, outputName):
    def getMeasure(bar, index):
        measure = stream.Measure()

        for i in range(index, len(bar)):
            accidental = ""

            symbol = str(bar[i][1])
            if isAccidental(symbol):
                accidental = SYMBOL_DICTIONARY[symbol]
            else:
                tmp = None

                if symbol.count("note") > 0:
                    print("note")
                    if symbol.count("whole") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="whole")
                    elif symbol.count("half") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="half")
                    elif symbol.count("quarter") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="quarter")
                    elif symbol.count("eighth") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="eighth")
                    elif symbol.count("sixteen") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="16th")

                    measure.append(tmp)
                elif symbol.count("rest") > 0:
                    print("rest")
                    if symbol.count("whole") > 0:
                        tmp = note.Rest("whole")
                    elif symbol.count("half") > 0:
                        tmp = note.Rest("half")
                    elif symbol.count("quarter") > 0:
                        tmp = note.Rest("quarter")
                    elif symbol.count("eighth") > 0:
                        tmp = note.Rest("eighth")
                    elif symbol.count("sixteen") > 0:
                        tmp = note.Rest("16th")

                    measure.append(tmp)
        
        return measure


    def getNotePitch(pos, accidental=""):
        return "C" + accidental + "4" # TODO replace

    
    def checkStart(bar):
        def isKey(accidental, next):
            if isAccidental(next[1]) or isTime(next[1]):
                return True
            
            print(str(next[0][0] - accidental[0][0]))
            if next[0][0] - accidental[0][0] < MAX_HORIZONTAL_DISTANCE:
                return False
            
            return True


        newClef = None
        newKey = 0
        keyChange = False
        newTime = None

        for i in range(0, len(bar)):
            if isClef(bar[i][1]):
                print("clef")
                newClef = SYMBOL_DICTIONARY[bar[i][1]]
            elif isAccidental(bar[i][1]):
                print("accidental")
                if isKey(bar[i], bar[i + 1]):
                    keyChange = True

                    if bar[i][1] == FLAT_SYMBOL:
                        newKey -= 1
                    elif bar[i][1] == SHARP_SYMBOL:
                        newKey += 1
                else:
                    if keyChange:
                        newKey = key.KeySignature(newKey)
                    else:
                        newKey = None

                    return newClef, newKey, newTime, i
            elif isTime(bar[i][1]):
                print("time")
                newTime = SYMBOL_DICTIONARY[bar[i][1]]

                if keyChange:
                    newKey = key.KeySignature(newKey)
                else:
                    newKey = None

                return newClef, newKey, newTime, i + 1
            else:
                print("done start")
                if keyChange:
                    newKey = key.KeySignature(newKey)
                else:
                    newKey = None

                return newClef, newKey, newTime, i
            
        return newClef, newKey, newTime, 0


    def isClef(symbolName):
        if symbolName == TREBLE_SYMBOL or symbolName == BASS_SYMBOL:
            return True
        return False
    

    def isAccidental(symbolName): 
        if symbolName == FLAT_SYMBOL or symbolName == SHARP_SYMBOL or symbolName == NATURAL_SYMBOL:
            return True
        return False


    def isTime(symbolName):
        if TIME_SYMBOLS.count(symbolName) > 0:
            return True
        return False
    

    part = stream.Part()

    lastClef = None
    newClef = None

    lastKey = None
    newKey = None

    lastTime = None
    newTime = None

    for bar in bars:
        newClef, newKey, newTime, index = checkStart(bar)
        measure = getMeasure(bar, index)

        if newClef != None and newClef != lastClef:
            measure.clef = newClef
            lastClef = newClef

        if newKey != None and newKey != lastKey:
            measure.keySignature = newKey
            lastKey = newKey

        if newTime != None and newTime != lastTime:
            measure.timeSignature = newTime
            lastTime = newTime

        part.append(measure)        

    score = stream.Score()
    score.append(part)
    score.write(fmt=outputFormat, fp=outputName)


def main():
    pass


if __name__ == '__main__':
    main()
