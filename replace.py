import re
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file that will be processed")
parser.add_argument("-j", "--json", help="targets json file", default="targets.json")
parser.add_argument("-o", "--output", help="output file that contains all replacements")

args = parser.parse_args()

lines = []
with open(args.input) as infile:
    lines = infile.readlines()

with open(args.json) as injson:
    jsonLines = injson.readlines()
    jsonData = json.loads("".join(jsonLines))
    replaceTargets = jsonData["replaceTargets"]

# for each line in the original input file
for i, _ in enumerate(lines):
    # for each replace target from the json
    for jsonTarget in replaceTargets:
        originalLine = lines[i]
        isRegex = "regex" in jsonTarget.keys()

        if (isRegex):
            jsonTarget["target"] = jsonTarget["target"].replace(r"\\", "\\")
            # print(jsonTarget)
            lines[i] = re.sub(jsonTarget["target"], jsonTarget["with"], lines[i])

        else:
            lines[i] = originalLine.replace(jsonTarget["target"], jsonTarget["with"])

        if (lines[i] != originalLine):
            print(f"replaced line[{i+1}] regex={isRegex} target={jsonTarget['target']} value={jsonTarget['with']}")

with open(args.output, "w") as outfile:
    outfile.writelines(lines)