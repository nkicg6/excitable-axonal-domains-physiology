# main for extracellular LFP analysis
from args import parser
import parsing
import lfpio


def input_output(datadir):
    print("io function passed")
    csv_data = parsing.IO_parse_csv_main(datadir, "io")
    json_data = parsing.IO_parse_json_main(datadir, "_io_region.json")
    merged = parsing.merge_csv_json(csv_data, json_data)
    io_analysis_datastructure = parsing.make_io_analysis_datastructure(merged)
    return merged, io_analysis_datastructure


def main():
    cmd_line = parser.parse_args()
    print("running")
    # first, validate command line opts
    if cmd_line.analysis_type == "io":
        merged_meta, io_analysis_datastructure = input_output(cmd_line.data_directory)
        all_res = []
        for uniquekey in io_analysis_datastructure.keys():
            temp = io_analysis_datastructure[uniquekey]["io"]
            all_res.append(lfpio.input_output_experiment(temp))
        print(f"all res {all_res}")
    else:
        print(f"ERROR! did not understand options in {cmd_line.analysis_type}")


if __name__ == "__main__":
    main()
