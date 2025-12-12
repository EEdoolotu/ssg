import os
import shutil
import sys
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

# Project directories
DIR_STATIC = "./static"
DIR_PUBLIC = "./docs"  # you use "docs" instead of "public"
DIR_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"
DEFAULT_BASEPATH = "/"


def start_server():
    """Start a simple HTTP server in DIR_PUBLIC."""
    os.chdir(DIR_PUBLIC)
    server = HTTPServer(("localhost", 8888), SimpleHTTPRequestHandler)
    print("Serving on http://localhost:8888")
    server.serve_forever()


def main():
    # Optional basepath argument
    basepath = DEFAULT_BASEPATH
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # 1️⃣ Delete old public/docs folder
    print("Deleting public directory...")
    if os.path.exists(DIR_PUBLIC):
        shutil.rmtree(DIR_PUBLIC)

    # 2️⃣ Copy static files
    print("Copying static files to public directory...")
    copy_files_recursive(DIR_STATIC, DIR_PUBLIC)

    # 3️⃣ Generate all pages recursively
    print("Generating content...")
    generate_pages_recursive(DIR_CONTENT, TEMPLATE_PATH, DIR_PUBLIC, basepath)

    # 4️⃣ Start HTTP server in a separate thread so Boot.dev can connect immediately
    threading.Thread(target=start_server, daemon=True).start()

    # 5️⃣ Wait a short time to ensure Boot.dev can connect
    time.sleep(0.5)

    # 6️⃣ Keep the script alive (optional if run manually)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
