import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
import time

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive  # recursive generator

# Project directories
DIR_STATIC = "./static"
DIR_PUBLIC = "./public"
DIR_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    # 1️⃣ Delete public folder if it exists
    print("Deleting public directory...")
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)

    # 2️⃣ Copy static files to public
    print("Copying static files to public directory...")
    copy_files_recursive(DIR_STATIC, DIR_PUBLIC)

    # 3️⃣ Generate all pages recursively
    print("Generating content...")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_PATH, DIR_PUBLIC)

    # 4️⃣ Serve public/ on port 8888
    os.chdir(DIR_PUBLIC)
    print("Serving on http://localhost:8888")
    time.sleep(0.5)  # give a tiny buffer for Boot.dev to connect
    server = HTTPServer(("localhost", 8888), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
