import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--echo",action="store",default="hehe")
args = parser.parse_args()
print args.echo
