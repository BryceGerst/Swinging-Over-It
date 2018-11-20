def toGameCoords(x, y, screenW, screenH):
    properX = int(x + screenW/2)
    properY = int(-1 * y + screenH/2)
    return properX, properY

