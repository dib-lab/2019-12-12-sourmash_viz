#! /usr/bin/env python


def do_something(message, output=None):
    if output:
        output.write(message)
    else:
        print(message)


def test_do_something():
    import io

    out = io.StringIO()

    do_something("message", output=out)
    assert out.getvalue() == "message"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=argparse.FileType("wt"), default=None)
    parser.add_argument("message", nargs="+")
    args = parser.parse_args()

    do_something(" ".join(args.message), args.output)
