# scratch for current ramp analysis
import scipy.signal as s
import matplotlib.pyplot as plt
import pyabf
import patch_clamp.steps as steps
import patch_clamp.database as db

con = db.persistent_connection_to_db(db.DATABASE_PATH)

paths = con.execute(
    "SELECT fpath FROM metadata WHERE protocol = 'cc_03-rheobase' AND include = 'yes'"
).fetchall()

paths = [i[0] for i in paths]
sweep = 5
path_n = 5
target = steps.abf_golay(steps.read_abf_IO(paths[path_n], sweep, 0))
abf = pyabf.ABF(paths[path_n])
m = target["filtered"].mean()
thresh = (abs(m) * 0.9) + m
peak, _ = s.find_peaks(target["filtered"], threshold=thresh, height=0, distance=11)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.plot(target["x"], target["filtered"])
ax1.plot(target["x"][peak], target["filtered"][peak], "g.")
ax1.hlines(y=thresh, xmin=target["x"][0], xmax=target["x"][-1])
ax2.plot(abf.sweepX, abf.sweepC)

plt.show()
