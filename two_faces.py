import argparse
import gen

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Target executable file directory.", required=True)
parser.add_argument("-t", "--tag", help="Value of element contains in tag arrays.", required=True)
parser.add_argument("-n", "--numtags", help="Size of the tag array.", required=True)

if __name__ == "__main__":

    try:
        args = parser.parse_args()

        filename = args.filename
        tag = args.tag
        num_tags = args.numtags

        assert len(tag) == 1, "Tag length has to be 1."
        assert int(num_tags) >= 100, "Number of tags in an array has to be at least 100."

        generator = gen.GenFiles(filename, tag, int(num_tags))
        generator.gen()
        generator.clean()

    except Exception as e:
        print(e)
