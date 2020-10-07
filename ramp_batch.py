# main script for analysis of ramp
import patch_clamp.archive as archive
import patch_clamp.database as db
import patch_clamp.utils as utils
import patch_clamp.ramp as ramp

SCHEMA = archive.get_schema("patch_clamp/ramp_schema.sqlite")
con, cur = archive.make_db(db.DATABASE_PATH, SCHEMA)
cur.close()
con.close()


paths = ramp.get_ramps_from_db()


con = db.persistent_connection_to_db(db.DATABASE_PATH)
for i in paths:
    current = utils.abf_golay(utils.read_abf_IO(i, 0, 0))
    current_peak = ramp.find_ramp_peaks(current)
    serialized = ramp.serialize_for_db(current_peak)
    ramp.add_to_db(con, serialized)
