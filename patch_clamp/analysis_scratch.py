# analysis stuff
import patch_clamp.database as database
import pyabf
import matplotlib.pyplot as plt


con = database.persistent_connection_to_db(database.DATABASE_PATH)
target = "20101003"
query = f"SELECT fpath FROM metadata WHERE fname == {target}"

p = con.execute(query).fetchall()[0]

abf = pyabf.ABF(p[0])
abf.setSweep(10)

plt.plot(abf.sweepX, abf.sweepY)
plt.show()

for sweep in abf.sweepList:
    abf.setSweep(sweep)
    print(f"sweep {sweep} max is {max(abf.sweepC)}, min is {min(abf.sweepC)}")
