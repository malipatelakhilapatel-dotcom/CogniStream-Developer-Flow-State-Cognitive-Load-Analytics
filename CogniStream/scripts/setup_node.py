import os
import sys
import urllib.request
import zipfile
import shutil

NODE_VERSION = "v20.18.0"
ZIP_NAME = f"node-{NODE_VERSION}-win-x64.zip"
URL = f"https://nodejs.org/dist/{NODE_VERSION}/{ZIP_NAME}"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
ZIP_PATH = os.path.join(TOOLS_DIR, ZIP_NAME)
NODE_EXTRACTED = os.path.join(TOOLS_DIR, f"node-{NODE_VERSION}-win-x64")
NODE_FINAL = os.path.join(TOOLS_DIR, "node")

def download_and_extract():
    os.makedirs(TOOLS_DIR, exist_ok=True)
    if os.path.exists(os.path.join(NODE_FINAL, "node.exe")):
        print(f"Node.js already installed in {NODE_FINAL}")
        return

    print(f"Downloading Node.js {NODE_VERSION} from {URL}...")
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = f"\rDownloading: {percent:5.1f}% ({readsofar / (1024*1024):.1f} MB / {totalsize / (1024*1024):.1f} MB)"
            sys.stdout.write(s)
            sys.stdout.flush()

    urllib.request.urlretrieve(URL, ZIP_PATH, reporthook)
    print("\nDownload complete. Extracting...")

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(TOOLS_DIR)

    if os.path.exists(NODE_EXTRACTED):
        if os.path.exists(NODE_FINAL):
            shutil.rmtree(NODE_FINAL)
        os.rename(NODE_EXTRACTED, NODE_FINAL)

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    print(f"Successfully extracted Node.js to {NODE_FINAL}")

if __name__ == "__main__":
    download_and_extract()
