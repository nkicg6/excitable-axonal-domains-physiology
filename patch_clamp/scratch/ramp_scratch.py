# scratch for current ramp analysis
import patch_clamp.utils as utils
import patch_clamp.ramp as ramp
import patch_clamp.database as db

con = db.persistent_connection_to_db(db.DATABASE_PATH)
paths = ramp.get_ramps_from_db()
sweep = 2

path_n = 20  # path 20 sweep 0 is empty
target = utils.abf_golay(utils.read_abf_IO(paths[path_n], sweep, 0))
target = ramp.find_ramp_peaks(target)
serialized = ramp.serialize_for_db(target)

ramp.add_to_db(con, serialized)

r = con.execute("SELECT * FROM ramp").fetchall()
print(r)
