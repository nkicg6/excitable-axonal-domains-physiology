# main for extracellular LFP analysis
from args import parser
import os
import json
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
            exp_temp_res = lfpio.input_output_experiment(temp)
            forjson = lfpio.gather_io_data_to_json(exp_temp_res)
            lfpio.input_output_experiment_plot(exp_temp_res, uniquekey)
            all_res.append(forjson)
            print(f"appending {uniquekey}")
        # now write the json
        for result in all_res:
            base_name = result[0]["unique_id"] + "_io_results.json"
            path_base, _ = os.path.split(result[0]["file"])
            p = os.path.join(path_base, base_name)
            with open(p, "w") as resultwrite:
                json.dump(result, resultwrite)
                print(f"writing {result[0]['unique_id']} to {p}\n\n")
    else:
        print(f"ERROR! did not understand options in {cmd_line.analysis_type}")


if __name__ == "__main__":
    main()
