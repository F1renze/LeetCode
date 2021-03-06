
import os
import urllib

from git import Repo


"""
自动生成带超链接 Markdown 
github 查看具体目录时在 repo url 后加 tree
具体文件则加 blob
"""

preface = """ LeetCode
Solved Problems by python, total count: {}
"""


def main():
    repo = Repo("./")
    branch = repo.active_branch.name
    # 移除结尾 .git
    remote_url = repo.remotes[0].url[:-4]
    with open("README.md", "w", encoding="utf-8") as file:
        total, count = list_files(".")
        file.write(preface.format(count) + "\n")

        for _queue in total:
            grand = None
            parent = None
            for e in _queue:
                if isinstance(e, list):
                    if e[1] == 1:
                        grand = e[0]
                    prefix = "#" * (e[1] + 1)
                    file.write("\n" + prefix + " " + e[0] + "\n")
                    parent = e[0]
                else:
                    # e is file name
                    link = (
                        "["
                        + e.split(".")[0]
                        + "]("
                        + remote_url
                        + "/"
                        + "blob"
                        + "/"
                        + branch
                        + "/"
                        + grand
                        + "/"
                        + parent
                        + "/"
                        + urllib.parse.quote(e)
                        + ")"
                    )
                    file.write("- " + link + "\n\n")


def list_files(startpath):
    enable = [".py", ".cpp", ".go", ".java"]

    excludes = ["0Data", ".git", ".idea", "venv"]
    total, counter = list(), set()

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        if any(e in root for e in excludes) or level == 0:
            continue
        root = os.path.basename(root)
        if level == 1:
            total.append(list())
        total[-1].append([root, level])
        print("{}{}/".format(indent, root))
        subindent = " " * 4 * (level + 1)
        for f in files:
            for end in enable:
                if not f.endswith(end):
                    continue
            total[-1].append(f)
            # 根据题号计数
            counter.add(f.split('.')[0])
            print("{}{}".format(subindent, f))
    # 按文件夹字母序排名
    total = sorted(total, key=lambda x: x[0][0])
    return total, len(counter)


if __name__ == "__main__":
    main()
