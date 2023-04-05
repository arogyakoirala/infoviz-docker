import argparse

parser = argparse.ArgumentParser()
parser.add_argument("uid")
parser.add_argument("clcode")
parser.add_argument("cltype")
parser.add_argument("stcode")
args = parser.parse_args()

str = f"uid={args.uid}\nclcode={args.clcode}\ncltype={args.cltype}\nstcode={args.stcode}\n"

text_file = open("sample.txt", "w")
n = text_file.write(str)
text_file.close()