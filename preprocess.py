import argparse
import text
from tqdm import tqdm
from utils import load_filepaths_and_text

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--text_index", default=1, type=int, help="index of text column in filelist")
  parser.add_argument("--filelists", nargs="+", required=True, help="filelists to be saved")
  parser.add_argument("--text_cleaners", nargs="+", default=["korean_cleaners"], help="text cleaners")

  args = parser.parse_args()

  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    for i in tqdm(range(len(filepaths_and_text))):
      original_text = filepaths_and_text[i][args.text_index]
      cleaned_text = text._clean_text(original_text, args.text_cleaners)
      filepaths_and_text[i][args.text_index] = cleaned_text

    new_filelist = "".join(filelist.split(".")[:-1]) + "_cleaned." + filelist.split(".")[-1]
    with open(new_filelist, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])
