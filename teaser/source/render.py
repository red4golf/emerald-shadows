import sys, time
sys.path.insert(0, ".")
from build import *
d = storyboard()
t = time.time()
encode(d.frames, "emerald_shadows_teaser_silent.mp4", crf=17, preset="medium")
print("rendered", d.t, "s in", round(time.time()-t), "s")
