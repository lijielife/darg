
import os
import shutil

import cssmin
import jsmin

print("Minify Static Files (Javascripts & Stylesheets)")


DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(DIR, '..', "site", "static")
SOURCE_DIR = os.path.join(STATIC_DIR, "compiled")
OUTPUT_DIR = os.path.join(STATIC_DIR, "minified")

def clear_dir(dirname, ignore_errors=True):
    shutil.rmtree(dirname, ignore_errors=ignore_errors)


def create_dir(dirname, remove_existing=True):
    if remove_existing and os.path.exists(dirname):
        clear_dir(dirname)

    os.mkdir(dirname)


def copy_dir(source_dir, output_dir):

    if not os.path.exists(source_dir):
        return

    if os.path.exists(output_dir):
        clear_dir(output_dir)

    shutil.copytree(source_dir, output_dir)


if __name__ == "__main__":

    # create/clear output dir
    create_dir(OUTPUT_DIR)

    # copy fonts
    print("Copying fonts...")
    copy_dir(
        os.path.join(SOURCE_DIR, "fonts"),
        os.path.join(OUTPUT_DIR, "fonts")
    )

    # copy images
    print("Copying images...")
    copy_dir(
        os.path.join(SOURCE_DIR, "images"),
        os.path.join(OUTPUT_DIR, "images")
    )

    # copy contrib javascripts
    print("Copying contrib javascripts...")
    copy_dir(
        os.path.join(SOURCE_DIR, "javascript", "contrib"),
        os.path.join(OUTPUT_DIR, "javascript", "contrib")
    )

    # copy contrib stylesheets
    print("Copying contrib stylesheets...")
    copy_dir(
        os.path.join(SOURCE_DIR, "stylesheets", "contrib"),
        os.path.join(OUTPUT_DIR, "stylesheets", "contrib")
    )

    # TODO: minify javascripts
    js_source_dir = os.path.join(SOURCE_DIR, "javascript")
    for pathname in os.listdir(js_source_dir):
        path = os.path.join(js_source_dir, pathname)
        if os.path.isfile(path):
            # open source file
            with open(path, 'r') as f:
                content = f.read()
            # minify
            minified = jsmin.jsmin(content)
            # write minified output file
            output_filepath = os.path.join(OUTPUT_DIR, "javascript", pathname)
            with open(output_filepath, 'w') as f:
                f.write(minified)

    # minify stylesheets
    css_source_dir = os.path.join(SOURCE_DIR, "stylesheets")
    for pathname in os.listdir(css_source_dir):
        path = os.path.join(css_source_dir, pathname)
        if os.path.isfile(path):
            # open source file
            with open(path, 'r') as f:
                content = f.read()
            # minify
            minified = cssmin.cssmin(content)
            # write minified output file
            output_filepath = os.path.join(OUTPUT_DIR, "stylesheets", pathname)
            with open(output_filepath, 'w') as f:
                f.write(minified)
