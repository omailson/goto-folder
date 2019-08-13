# goto-folder

goto-folder is a tool that you can use to save named bookmarks for your local directories. Instead of typing the entire path of a folder you commonly use, you can bookmark that folder and just `goto` them.

## Usage

First we need to add a bookmark. We can do that by setting the `$GOTOFOLDERS` environment var

```bash
export GOTOFOLDERS=small:/home/user/long/path,$GOTOFOLDERS
```

Now you can go to your bookmarked folder from anywhere

```bash
$ goto small
```

Please note the path in `$GOTOFOLDERS` must be an absolute path

## The .goto file

You can also add your bookmarks to a file called `.goto`. This file can be localed anywhere on you file path. `goto` will look for those files in your current directory and all directories above, up until your user's home folder.

Inside `.goto` the paths can be either absolute or relative paths. If the path is relative, it will be resolved relative to where the `.goto` file containing the bookmark is located.

## Instalation

After cloning this repository, add the following line to your bash startup script (usually `~/.bashrc` or `~/.bash_profile`)

```bash
source /path/to/goto-folder/goto.bash
```

To add code completion (which I highly recommend), add the following line too:

```bash
source /path/to/goto-folder/goto-completion.bash
```

## History

goto-folder used to be a bash script I maintened in my machine for many years. The script was very useful but it wasn't very portable and contained some bugs. Instead of dealing with a code mess I decided to rewrite the entire thing in Python.

We still rely on bash scripting in order to properly change folders (the python program only resolves the bookmark name to an absolute path), but now I can have my tool working without bugs and I'm finally able to expand it to add more features
