import json
import os
import argparse

def is_substring_in_list(substring, string_list):
    return any(substring in string for string in string_list)


parser = argparse.ArgumentParser()

parser.add_argument('--scene_path', required=True)

args = parser.parse_args()

PATH = args.scene_path
JSON_FILENAME = r"instant_ngp_all.json"

TEST_FILEPATH = os.path.join(PATH, "sparse/0/test.txt")

with open(TEST_FILEPATH, 'r') as file:
    test_filenames = [line.strip() for line in file]

with open(os.path.join(PATH, JSON_FILENAME), 'r') as file:
    data = json.load(file)

data_test = data.copy()
data_train = data.copy()

print(data["frames"][0]["file_path"])
print(test_filenames[0])
data_train["frames"] = [f for f in data["frames"] if not is_substring_in_list(f["file_path"], test_filenames)]
data_test["frames"] = [f for f in data["frames"] if is_substring_in_list(f["file_path"], test_filenames)]

print("Train images: ", len(data_train["frames"]), "Test image: ", len(data_test["frames"]))

with open(os.path.join(PATH, JSON_FILENAME.split(".")[0] + "_train.json"), 'w') as file:
    json.dump(data_train, file, indent=4)
with open(os.path.join(PATH, JSON_FILENAME.split(".")[0] + "_test.json"), 'w') as file:
    json.dump(data_test, file, indent=4)