from textnode import *
from inline_markdown import *
from htmlnode import *
import shutil
import os


def main():

    copy_static_to_public()
    pass

def copy_static_to_public():

    public_path = "~/workspace/github.com/Breadumi/stat_site_gen/public"
    static_path = "~/workspace/github.com/Breadumi/stat_site_gen/static"

    shutil.rmtree(public_path)





main()