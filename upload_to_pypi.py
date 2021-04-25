import os
import shutil


def main():
    # Remove the dist folder
    try:
        shutil.rmtree(os.path.dirname(__file__) + '/dist')
    except FileNotFoundError:
        pass
    # Run build
    os.system('/usr/local/bin/python3 -m build')
    # Use Twine to upload
    os.system('/usr/local/bin/python3 /usr/local/bin/twine upload --repository testpypi dist/*')


if __name__ == "__main__":
    main()
