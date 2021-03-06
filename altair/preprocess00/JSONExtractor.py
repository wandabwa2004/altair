import gzip
import json
import os
import time

from altair.util.log import getLogger

logger = getLogger(__name__)

class JSONExtractor:
    def __init__(self, output_dir, output_extension):
        self.output_dir = output_dir
        self.output_extension = output_extension

    def extract(self, path_to_json_gz):
        basename = os.path.basename(path_to_json_gz).split(".")[0] # remove extension
        folder = os.path.join(self.output_dir, basename)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with gzip.open(path_to_json_gz, "rb") as f1:
            for line in f1:
                j = json.loads(line.decode("utf-8"))
                target = os.path.join(folder, "%s.%s" % (j["id"], self.output_extension))
                if not os.path.exists(target):
                    with open(target, "wb") as f2:
                        f2.write(j["content"].encode("utf-8"))

    def extract_dir(self, input_dir):
        for json_gz_file in sorted(os.listdir(input_dir)):
            fullpath = os.path.join(input_dir, json_gz_file)
            logger.info("Processing file: %s" % fullpath)
            start_time = time.time()
            self.extract(fullpath)
            logger.info("Elapsed time: %s" % (time.time()-start_time))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Extract individual files from .json.gz archive.')

    # Required args
    parser.add_argument("input_target",
                        type=str,
                        help="Input target for JSONExtractor")
    parser.add_argument("output_dir",
                        type=str,
                        help="Output directory for JSONExtractor")

    # Optional args
    parser.add_argument("--dir",
                        action="store_true",
                        help="Specify whether [input_target] is a directory (default = false)")
    parser.add_argument("--extension",
                    type=str,
                    default="py",
                    help="Extracted file extension (all must be the same) (default = py)")

    args = parser.parse_args()
    extractor = JSONExtractor(args.output_dir, args.extension)
    if args.dir:
        extractor.extract_dir(args.input_target)
    else:
        extractor.extract(args.input_target)
