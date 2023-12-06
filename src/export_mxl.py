
from music21 import stream, metadata, meter, key, note, clef


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

BASS_CONVERSION = {
    "G5": "B4",
    "F5": "A4",
    "E5": "G3",
    "D5": "F3",
    "C5": "E3",
    "B5": "D3",
    "A5": "C3",
    "G4": "B3",
    "F4": "A3",
    "E4": "G2",
    "D4": "F2"
}

ORDER_OF_SHARPS = ["F", "C", "G", "D", "A", "E", "B"]

def export(bars, outputFormat, outputPath, outputTitle):
    def getMeasure(bar, index, barClef, barKey, barTime, changeClef, changeKey, changeTime):
        measure = stream.Measure()

        if changeClef:
            measure.clef = barClef

        if changeKey:
            measure.keySignature = barKey

        if changeTime:
            measure.timeSignature = barTime

        numSharps = barKey._getSharps()
        barKey = ORDER_OF_SHARPS[0:numSharps]
        barAccidentals = {}

        if numSharps >= 0:
            symbolType = "#"
        else:
            symbolType = "b"

        for accidental in barKey:
            barAccidentals.update({accidental: accidental + symbolType})

        accidental = None

        for i in range(index, len(bar)):
            symbol = str(bar[i][1])

            if isAccidental(symbol):
                accidental = SYMBOL_DICTIONARY[symbol]
            else:
                newNote = None

                if symbol.count("note") > 0:
                    pitch = str(bar[i][3])

                    if barClef == clef.BassClef():
                        pitch = BASS_CONVERSION[pitch]

                    if accidental != None:
                        if accidental == "":
                            barAccidentals.pop(pitch[0], False)
                        else:
                            barAccidentals.update({pitch[0]: pitch[0] + accidental})
                    
                    if barAccidentals.keys().__contains__(pitch[0]):
                        pitch = barAccidentals[pitch[0]] + pitch[1] 

                    if symbol.count("whole") > 0:
                        newNote = note.Note(pitch, type="whole")
                    elif symbol.count("half") > 0:
                        newNote = note.Note(pitch, type="half")
                    elif symbol.count("quarter") > 0:
                        newNote = note.Note(pitch, type="quarter")
                    elif symbol.count("eighth") > 0:
                        newNote = note.Note(pitch, type="eighth")
                    elif symbol.count("sixteen") > 0:
                        newNote = note.Note(pitch, type="16th")

                    measure.append(newNote)
                elif symbol.count("rest") > 0:
                    if symbol.count("whole") > 0:
                        newNote = note.Rest(quarterLength=(barTime.beatDuration.quarterLength * barTime.beatCount))
                    elif symbol.count("half") > 0:
                        newNote = note.Rest(quarterLength=(barTime.beatDuration.quarterLength * barTime.beatCount / 2))
                    elif symbol.count("quarter") > 0:
                        newNote = note.Rest(quarterLength=(barTime.beatDuration.quarterLength * barTime.beatCount / 4))
                    elif symbol.count("eighth") > 0:
                        newNote = note.Rest(quarterLength=(barTime.beatDuration.quarterLength * barTime.beatCount / 8))
                    elif symbol.count("sixteen") > 0:
                        newNote = note.Rest(quarterLength=(barTime.beatDuration.quarterLength * barTime.beatCount / 16))

                    measure.append(newNote)

                accidental = None
        
        return measure

    
    def checkStart(bar):
        def isKey(accidental, next):
            if isAccidental(next[1]) or isTime(next[1]):
                return True
            
            if next[0][0] - accidental[0][0] < MAX_HORIZONTAL_DISTANCE:
                return False
            
            return True


        newClef = None
        newKey = 0
        keyChange = False
        newTime = None

        for i in range(0, len(bar)):
            if isClef(bar[i][1]):
                newClef = SYMBOL_DICTIONARY[bar[i][1]]
            elif isAccidental(bar[i][1]):
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
                newTime = SYMBOL_DICTIONARY[bar[i][1]]

                if keyChange:
                    newKey = key.KeySignature(newKey)
                else:
                    newKey = None

                return newClef, newKey, newTime, i + 1
            else:
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
    changeClef = False

    lastKey = None
    newKey = None
    changeKey = False

    lastTime = None
    newTime = None
    changeTime = False

    for bar in bars:
        changeClef = False
        changeKey = False
        changeTime = False

        newClef, newKey, newTime, index = checkStart(bar)

        if newClef != None and newClef != lastClef:
            changeClef = True
            lastClef = newClef

        if newKey != None and newKey != lastKey:
            changeKey = True
            lastKey = newKey

        if newTime != None and newTime != lastTime:
            changeTime = True
            lastTime = newTime

        measure = getMeasure(bar, index, lastClef, lastKey, lastTime, changeClef, changeKey, changeTime)

        part.append(measure)

    score = stream.Score()
    score.metadata = metadata.Metadata(title=outputTitle, composer="")
    score.append(part)
    score.write(fmt=outputFormat, fp=outputPath)

