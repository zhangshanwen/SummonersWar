import os

a = [
    6,
    16,
    39,
    240,
    242,
    256,
    299,
    306,
    324,
    391,
    457,
    696,
    758,
    787,
    788,
    791,
    793,
    804,
    845,
    867,
    872,
    882,
    901,
    911,

]
for i in a:
    print(i)
    os.system(f"cd ~/mp4 &&  /Users/zsw/Desktop/golang_code/gomovie/gomovie download -id={i}")
