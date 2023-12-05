
from music21 import configure, stream, meter, key, note, clef


MAX_HORIZONTAL_DISTANCE = 256

TREBLE_SYMBOL = "treble"
BASS_SYMBOL = "bass"

FLAT_SYMBOL = "flat"
SHARP_SYMBOL = "sharp"
NATURAL_SYMBOL = "natual"

TIME_CUT_SYMBOL = "22"
TIME_C_CYMBOL = "44c"
TIME_24_SYMBOL = "24"
TIME_34_SYMBOL = "34"
TIME_38_SYMBOL = "38"
TIME_44_SYMBOL = "44"
TIME_68_SYMBOL = "68"

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

            if isAccidental(bar[i]):
                accidental = SYMBOL_DICTIONARY[bar[i][1]]
            else:
                tmp = None
                symbol = str(bar[i][1])
                if symbol.count("note") > 0:
                    if symbol.count("whole") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="whole")
                    elif symbol.count("half") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="half")
                    elif symbol.count("quarter") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="quarter")
                    elif symbol.count("eighth") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="eighth")
                    elif symbol.count("sixteen") > 0:
                        tmp = note.Note(getNotePitch(bar[i][0], accidental), type="sixteen")
                elif symbol.count("rest") > 0:
                    if symbol.count("whole") > 0:
                        tmp = note.Rest("whole")
                    elif symbol.count("half") > 0:
                        tmp = note.Rest("half")
                    elif symbol.count("quarter") > 0:
                        tmp = note.Rest("quarter")
                    elif symbol.count("eighth") > 0:
                        tmp = note.Rest("eighth")
                    elif symbol.count("sixteen") > 0:
                        tmp = note.Rest("sixteen")
                    
                measure.append(tmp)
        
        return measure


    def getNotePitch(pos, accidental=""):
        return "C" + accidental + "4" # TODO replace

    
    def checkStart(bar):
        newClef = None
        newKey = 0
        newTime = None

        for i in range(0, len(bar)):
            if isClef(bar[i][1]):
                newClef = SYMBOL_DICTIONARY[bar[i][1]]
            elif isAccidental(bar[i][1]):
                if bar[i][1] == FLAT_SYMBOL and newKey <= 0 and bar[0][0][0] - bar[i][0][0] < MAX_HORIZONTAL_DISTANCE:
                    newKey -= 1
                elif bar[i][1] == SHARP_SYMBOL and newKey >= 0 and bar[0][0][0] - bar[i][0][0] < MAX_HORIZONTAL_DISTANCE:
                    newKey += 1
                else:
                    newKey = key.KeySignature(newKey)

                    return newClef, newKey, newTime, i
            elif isTime(bar[i][1]):
                newTime = SYMBOL_DICTIONARY[bar[i][1]]

                newKey = key.KeySignature(newKey)

                return newClef, newKey, newTime, i + 1
            else:
                newKey = key.KeySignature(newKey)

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
        if TIME_SYMBOLS.__contains__(symbolName):
            return True
        return False
    

    part = stream.Part()
    lastClef = None
    lastKey = None
    lastTime = None

    lastClef, lastKey, lastTime, index = checkStart(bars[0])
    part.append(lastClef)
    part.append(lastKey)
    part.append(lastTime)

    for bar in bars:
        newClef, newKey, newTime, index = checkStart(bar)
        measure = getMeasure(bar, index)

        if newClef != None and newClef != lastClef:
            measure.append(newClef)
            lastClef = newClef

        if newKey != None and newKey != lastKey:
            measure.append(newKey)
            lastKey = newKey

        if newTime != None and newTime != lastTime:
            measure.append(newTime)
            lastTime = newTime

        part.append(measure)

    score = stream.Score()
    score.append(part)
    score.write(fmt=outputFormat, fp=outputName)


def main():
    pass


if __name__ == '__main__':
    main()
