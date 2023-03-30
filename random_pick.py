import os
import random
import argparse

args = argparse.ArgumentParser()
args.add_argument("--filelist", required=True, help="full filelist to be sampled")
args.add_argument("--val_ratio", default=0.015, type=float, help="ratio of validation data")
args = args.parse_args()

with open(args.filelist, "r", encoding="utf-8") as f:
  data = f.readlines()

val_ratio = args.val_ratio
random.shuffle(data)
val_data = data[:int(len(data) * val_ratio)]
train_data = data[int(len(data) * val_ratio):]

val_path = os.path.join(os.path.dirname(args.filelist), "filelist_val.txt")
train_path = os.path.join(os.path.dirname(args.filelist), "filelist_train.txt")

with open(val_path, "w", encoding="utf-8") as f:
    f.writelines(val_data)
    print("val data saved to", val_path)
with open(train_path, "w", encoding="utf-8") as f:
    f.writelines(train_data)
    print("train data saved to", train_path)