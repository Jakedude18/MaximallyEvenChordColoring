from collections import deque

pulses = 12 # 12 notes in the chromatic scale
global normalInterval
global mode
global onsets

#Construct chord using DP
def maximizeColoring(baseChord, m, o):

    #queue to support fifo; useful in recursion
    normalVertices = deque()
    global normalInterval
    global mode
    global onsets
    onsets = o
    mode = m
    normalInterval = pulses / onsets

    for i in range(int(pulses / normalInterval)):
        normalVertices.append(i * normalInterval)
    
    base = deque(baseChord)

    coloring = colorChord(normalVertices, base, list())

    print(coloring)
    print(chordEveness(coloring))

    return coloring, chordEveness(coloring)



#find a list of integers (equal to the size of vertices) that is maximally even
#and must contain the integers in base

def colorChord(vertices: deque, base: deque, coloring=None):
    if coloring is None:
        coloring = []

    if not vertices:
        return coloring



    # Make copies for recursion
    base_copy = base.copy()
    vertices_copy = vertices.copy()

    closestIndex = nearestInMode(vertices_copy.popleft())

    # Two note options to assign this vertex to
    # Option 1
    closestColoring = coloring + [closestIndex]

    # Case: no more base notes    
    if not base:
        return colorChord(vertices_copy, base, closestColoring)
    

    # Case: choose base note in the front, base note in the back, or closestIndex
    # Option 2
    baseColoring = coloring + [base_copy.popleft()]


    # Index is 
    if len(base) >= len(vertices):
        return colorChord(vertices_copy, base_copy, baseColoring)
    # Index is pass next base chord
    if base[0] <= closestIndex:
        return colorChord(vertices_copy, base_copy, baseColoring)
    else:
        baseColoring = colorChord(vertices_copy, base_copy, baseColoring)
        base_copy = base.copy()
        backBaseColoring = coloring.copy() + [base_copy.pop()]
        backBaseColoring = colorChord(vertices_copy, base_copy, backBaseColoring)
        closestColoring = colorChord(vertices_copy, base, closestColoring)

        # find the most even out of the three
        candidates = [c for c in [baseColoring, closestColoring, backBaseColoring] if c is not None]

        # Pick the one with smallest evenness
        best = min(candidates, key=lambda c: chordEveness(c))

        return best
    

def nearestInMode (index: float):
    closest = min(mode, key=lambda x: abs(x - index))

    return closest
        



def chordEveness(coloring):
    """
    Compute evenness by measuring each note's distance
    to the closest normal vertex. This is the linear regression eveness metric
    See more in the README.
    """

    global onsets

    coloring_copy = coloring.copy()
    
    if onsets is None:
        onsets = len(coloring)
    normalInterval = pulses / onsets
    normalVertices = [i * normalInterval for i in range(onsets)]
    sum_dist = 0
    for note in coloring:
        closest_vertex = min(normalVertices, key=lambda v: circular12_distance(note, v))
        sum_dist += circular12_distance(closest_vertex, note)
        normalVertices.remove(closest_vertex)


    return sum_dist

def circular12_distance(a, b):
    """
    Returns the shortest distance between a and b on a 12-step circle.
    """
    diff = abs(a - b) % 12
    return min(diff, 12 - diff)




if __name__ == "__main__":
    o = 3
    baseChord = [11]
    m = [0,2,4,5,7,9,11]
    maximizeColoring(baseChord, m, o)
