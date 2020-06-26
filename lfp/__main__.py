# main for extracellular LFP analysis
from args import parser
import parsing

def io_fn(datadir):
    print("io function passed")
    csv_path = parsing.get_csv(datadir)
    csv_data = parsing.IO_parse_csv_main(csv_path, "io")
    json_data = parsing.IO_parse_json_main(datadir, "_io_region.json")
    merged = parsing.merge_csv_json(csv_data, json_data)
    return merged


def main():
    cmd_line = parser.parse_args()
    print("running")
    # first, validate command line opts
    if cmd_line.analysis_type == "io":
        merged_meta = io_fn(cmd_line.data_directory)
        print(f"merged metadata is \n {merged_meta}")
    else:
        print(f"ERROR! did not understand options in {cmd_line.analysis_type}")

if __name__ == "__main__":
    main()
