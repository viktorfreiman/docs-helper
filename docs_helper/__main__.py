"""
This is a docstring

`Docs how to write docstring
<https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_
"""
import argparse


def main():
    aparse = argparse.ArgumentParser(description="hello")

    aparse.add_argument(
        "-i",
        "--input",
        required=True,
    )
    args = aparse.parse_args()

    print(args.input)

    print("hello world")


if __name__ == "__main__":
    main()
