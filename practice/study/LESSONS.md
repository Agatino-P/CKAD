# Lessons

Condensed lessons, one section per topic in `practice/study/STUDY_PLAN.md`.

## Running commands with args in Docker and K8s

### ENTRYPOINT and CMD in an image

The process is the `ENTRYPOINT` words followed by the `CMD` words.\
Words typed after the image name in `docker run` take the place of the `CMD` words, and the `ENTRYPOINT` words stay.

Image `demo-ep` is `FROM busybox` with `ENTRYPOINT ["echo"]` and `CMD ["hello"]`.\
Image `demo-cmd` is `FROM busybox` with only `CMD ["echo", "hello"]`.

| Command | Outcome | Notes |
| --- | --- | --- |
| `docker run demo-ep` | prints `hello` | runs `echo hello` |
| `docker run demo-ep bye` | prints `bye` | `bye` replaces the `CMD` words |
| `docker run --entrypoint date demo-ep` | prints the date | `--entrypoint` replaces `ENTRYPOINT` and drops `CMD` |
| `docker run demo-cmd` | prints `hello` | no `ENTRYPOINT`, so `CMD` is the whole process |
| `docker run demo-cmd echo bye` | prints `bye` | the typed words are the whole process |
| `docker run demo-cmd bye` | fails: executable file `bye` not found | the typed words must start with a program |

- Write `ENTRYPOINT` and `CMD` as lists, as in `ENTRYPOINT ["sh"]`.\
  The plain-string form `ENTRYPOINT sh` is wrapped as `/bin/sh -c sh`, and the `CMD` words then never reach the program.

### command and args in a Pod

`command` replaces the image `ENTRYPOINT`, and `args` replaces the image `CMD`.

| Docker | Kubernetes | Example |
| --- | --- | --- |
| `ENTRYPOINT` | `command` | `["sh"]` |
| `CMD` | `args` | `["-c", "echo hello world"]` |

| `command` | `args` | Process |
| --- | --- | --- |
| set | set | `command` + `args` |
| set | unset | `command` only, and the image `CMD` is dropped |
| unset | set | image `ENTRYPOINT` + `args` |
| unset | unset | image `ENTRYPOINT` + image `CMD` |

Image `nginx` has `ENTRYPOINT ["/docker-entrypoint.sh"]` and `CMD ["nginx", "-g", "daemon off;"]`.\
Image `busybox` has no `ENTRYPOINT` and `CMD ["sh"]`.

| Pod spec | Outcome | Notes |
| --- | --- | --- |
| `nginx`, `args: ["echo", "hi"]` | prints `hi` | runs `/docker-entrypoint.sh echo hi` |
| `nginx`, `command: ["/docker-entrypoint.sh"]` | exits at once, no output | the image `CMD` is dropped |
| `busybox`, `args: ["echo", "hi"]` | prints `hi` | no `ENTRYPOINT`, so `args` is the whole process |
| `busybox`, `command: sh` | rejected | `command` and `args` accept only a list of strings |
| `busybox`, `args: [sleep, 3600]` | rejected | a number must be quoted, as in `"3600"` |
| `busybox`, `command: [sh]`, `args: [-c "echo hello world"]` | fails: `sh: illegal option -` | without the comma, `-c "echo hello world"` is one element |

- `podman image inspect nginx` shows the image lists under `Config.Entrypoint` and `Config.Cmd`.

### One list element is one word of the process

Kubernetes never splits an element and never interprets `;`, `&&`, `|` or `$`.\
The first element is the program.

On `busybox`, where `args` is the whole process:

| `args` | Outcome | Notes |
| --- | --- | --- |
| `["echo", "hello", "world"]` | prints `hello world` | `echo` with two arguments |
| `["echo", "hello world"]` | prints `hello world` | `echo` with one argument |
| `["echo hello world"]` | fails: `executable file not found` | the program name holds spaces |
| `["sh", "-c", "echo hello world"]` | prints `hello world` | the script is one element |
| `["sh", "-c", "echo", "hello world"]` | prints an empty line | the script is only `echo` |
| `["sh", "-c", "echo hello; echo world"]` | prints `hello`, then `world` | the shell reads the `;` |
| `["echo", "hello;", "echo", "world"]` | prints `hello; echo world` | no shell, so `;` is a plain character |

### sh -c reads exactly one element as its script

The script is only the element right after `-c`.

```
element 1   element 2   element 3
sh          -c          echo hello world
                        └── the script
```

```
element 1   element 2   element 3   element 4   element 5
sh          -c          echo        hello       world
                        └── the script
                                    └── extra elements, not part of the script
```

| Command | Outcome | Notes |
| --- | --- | --- |
| `sh -c 'echo hello world'` | prints `hello world` | the quotes keep the script as one element |
| `sh -c echo hello world` | prints an empty line | the script is only `echo` |

### kubectl run and the words after `--`

`kubectl run` flags come before `--`.\
Every word after `--` becomes one element of `args`, or of `command` with `--command`.\
The line fills either `args` or `command`, never both.

| Command | Outcome | Notes |
| --- | --- | --- |
| `kubectl run t --image=busybox --restart=Never -- echo hello world` | `args: ["echo", "hello", "world"]`, prints `hello world` | no `ENTRYPOINT` on `busybox` |
| `kubectl run t --image=busybox --restart=Never --command -- echo hello world` | `command: ["echo", "hello", "world"]`, prints `hello world` | same process on `busybox` |
| `kubectl run t --image=nginx --restart=Never -- sleep 30` | `args: ["sleep", "30"]`, runs `sleep 30` | goes through `/docker-entrypoint.sh` |
| `kubectl run t --image=nginx --restart=Never --command -- sleep 30` | `command: ["sleep", "30"]`, runs `sleep 30` | `/docker-entrypoint.sh` never runs |
| `kubectl run t --image=busybox --restart=Never -- hello world` | fails: `exec: "hello": executable file not found` | the first word must be a program |

### Which one to use

- To run a specific program, use `--command`, or set `command` in YAML.\
  The process is exactly the typed words, on any image.
- To run the image's own program with different arguments, such as a flag for an application, use plain `--`, or set `args` in YAML.
- `/docker-entrypoint.sh` in `nginx` runs its setup only when its first argument is `nginx`, then runs its arguments with `exec "$@"`.

### Quoting on the command line

Your shell splits the line at spaces, except inside quotes, and each word becomes one list element.\
Quote the script after `sh -c` as one piece, and leave `sh` and `-c` unquoted.

| After `--command --` | Outcome | Notes |
| --- | --- | --- |
| `sh -c 'echo hello world'` | `["sh", "-c", "echo hello world"]`, prints `hello world` | |
| `sh -c "echo hello; echo world"` | `["sh", "-c", "echo hello; echo world"]`, prints `hello`, then `world` | |
| `sh -c echo hello world` | `["sh", "-c", "echo", "hello", "world"]`, prints an empty line | the script is only `echo` |
| `"sh -c 'echo hello world'"` | `["sh -c 'echo hello world'"]`, fails: `executable file not found` | one element, taken as the program name |
| `sh -c echo one; echo two` | `["sh", "-c", "echo", "one"]`, prints an empty line, and `two` appears in your terminal | the unquoted `;` ends the kubectl command, and `echo two` runs on your machine |
| `sh -c 'echo a' && echo b` | `["sh", "-c", "echo a"]`, prints `a`, and `b` appears in your terminal | the unquoted `&&` runs `echo b` on your machine |

### Brackets belong to YAML, not to the command line

In YAML, write the list with brackets or `- ` lines.\
On the `kubectl run` line, write space-separated words, and quote a word that holds spaces.

| Command | Outcome | Notes |
| --- | --- | --- |
| `kubectl run t --image=busybox --restart=Never --command -- echo 'hello world'` | `command: ["echo", "hello world"]` | |
| `kubectl run t --image=busybox --restart=Never --command -- [echo, hi]` | `command: ["[echo,", "hi]"]` in bash | brackets are plain characters |
| `kubectl run t --image=busybox --restart=Never --command -- '["echo", "hi"]'` | one element holding the bracket text | taken as the program name |

### When a shell is needed

Use `sh -c` only when the command uses shell syntax: `;`, `&&`, `||`, `|`, `>`, `<`, `$VAR`, `*`, or a loop.\
Without a shell, these characters reach the program as plain text.

On `busybox`:

| `command` | Outcome | Notes |
| --- | --- | --- |
| `["echo", "$HOME"]` | prints `$HOME` | no shell |
| `["sh", "-c", "echo $HOME"]` | prints `/root` | |
| `["echo", "hi", ">", "/tmp/x"]` | prints `hi > /tmp/x` | no shell |
| `["sh", "-c", "echo hi > /tmp/x; cat /tmp/x"]` | prints `hi` | |
| `["ls", "/etc/*.conf"]` | fails: `/etc/*.conf: No such file or directory` | no shell |
| `["sh", "-c", "ls /etc/*.conf"]` | lists `/etc/nsswitch.conf` and `/etc/resolv.conf` | |
| `["date", ">", "/tmp/d"]` | prints the usage of `date` | no shell |
| `["sh", "-c", "date > /tmp/d"]` | writes the date to `/tmp/d` | |
| `["sleep", "3600"]` | sleeps | plain program, no shell needed |

### Writing the list in YAML

Every `- ` starts one element.\
A `- |` element holds a multi-line script as one string, so the whole script stays the single element after `-c`.\
Each line of the script is one shell command, so no `;` is needed between lines.

```yaml
command:
- sh
- -c
- |
  echo one
  for i in 1 2; do echo "loop $i"; done
  echo done
```

| YAML | Outcome | Notes |
| --- | --- | --- |
| the block above | prints `one`, `loop 1`, `loop 2`, `done` | 3 elements |
| `command: ["sh", "-c", "echo one; echo two"]` | prints `one`, then `two` | the same list written inline |
| `- sh`, `- -c`, `- echo one`, `- echo two` | prints `one` | `echo two` is an extra element |

### `$(VAR)` expanded by Kubernetes, `$VAR` expanded by a shell

In `command` and `args`, Kubernetes replaces `$(VAR)` with the container's `env` variable `VAR` before the container starts.\
Only a shell replaces `$VAR`.\
A variable missing from `env` is left as written, with no error.

On `busybox`, with `env` `DELAY` set to `"3"`:

| `command` | Outcome | Notes |
| --- | --- | --- |
| `["echo", "$(DELAY)"]` | prints `3` | no shell needed |
| `["echo", "$DELAY"]` | prints `$DELAY` | no shell |
| `["sh", "-c", "echo $DELAY"]` | prints `3` | the shell expands it |
| `["sleep", "$(DELAY)"]` | sleeps 3 seconds | works on any image |
| `["echo", "$(NOPE)"]` | prints `$(NOPE)` | `NOPE` is not in `env` |

### `--rm` on `kubectl run`

`--rm` deletes the Pod when the command ends, and works only while your terminal is attached, so it needs `-i`, or `-it` for an interactive shell.\
`--restart=Never` makes the command run once.

| Command | Outcome | Notes |
| --- | --- | --- |
| `kubectl run t --image=busybox --restart=Never --rm -i -- echo hi` | prints `hi`, then `pod "t" deleted` | no Pod left |
| `kubectl run t --image=busybox --restart=Never --rm -- echo hi` | refused: `--rm should only be used for attached containers` | no `-i` |
| `kubectl run t -rm --image=busybox --restart=Never -i -- echo hi` | refused: `unknown shorthand flag: 'r' in -rm` | `--rm` needs two dashes |
