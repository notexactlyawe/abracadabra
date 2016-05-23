from ascii_graph import graph_ascii
import wave
import numpy as np

def graph_wav_ascii(filename, term_width):
    spf = wave.open(filename, 'r')

    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    chunk_size = len(signal)/term_width

    temp = 0
    counter = 0
    to_graph = []
    for val in signal:
        if counter == chunk_size:
            to_graph.append(temp / chunk_size)
            temp = 0
            counter = 0
        temp += val
        counter += 1
    else:
        # Check if it's worth including the remainder of results
        if counter > chunk_size / 2:
            to_graph.append(temp / counter)

    graph_ascii(to_graph, resolution=20)

graph_wav_ascii('file3.wav', 100)
