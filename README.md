# two-faces

This project is inspired by the coding problem in MD5 Collision Attack Lab of SEEDLab.
This program generates two versions of a program with the same MD5 hash but one can execute malicious code.

## Requirements

This project is based heavily on MD5 collision generate tools called `md5collgen` made by [HashClash](https://github.com/cr-marcstevens/hashclash).
You can read more about `md5collgen` and HashClash [here](https://www.win.tue.nl/hashclash/).

## Usages

This tool can only run on executable files compiled from a C program. An example C program is in `/examples`. You
will have to compile the program first before using this tool.

```
python3 two-faces -f <filename> -t <tag> -n <length of tag array>
```

It will generate two executable files `a1.out` and `a2.out`, one is benign and one can execute malicious code in the
program.

## Future development

I will look into how to build tool for MD5 Collision Attack in Python based on
a research paper by Marc Stevens (he is also the creator of `md5collgen`).
