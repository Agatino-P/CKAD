# Lessons

Condensed lessons, one section per topic in `practice/study/STUDY_PLAN.md`.\
Every behaviour stated here was checked on the lab cluster, on Kubernetes v1.37.

## Running commands with args in Docker and K8s

### ENTRYPOINT and CMD in an image

Shape: process = `ENTRYPOINT` words + `CMD` words, and any words after the image name in `docker run` take the place of the `CMD` words.\
Example: image `demo-ep`, built `FROM busybox` with `ENTRYPOINT ["echo"]` and `CMD ["hello"]`, prints `hello` on `docker run demo-ep`, and `bye` on `docker run demo-ep bye`.

Checked with podman on two images built for the test, `demo-ep` and `demo-cmd`, both `FROM busybox`:

| Dockerfile | Run | Process | Output |
| --- | --- | --- | --- |
| `ENTRYPOINT ["echo"]`, `CMD ["hello"]` | no arguments | `echo hello` | `hello` |
| `ENTRYPOINT ["echo"]`, `CMD ["hello"]` | argument `bye` | `echo bye` | `bye` |
| `ENTRYPOINT ["echo"]`, `CMD ["hello"]` | `--entrypoint date` | `date` | the date |
| `CMD ["echo", "hello"]` only | no arguments | `echo hello` | `hello` |
| `CMD ["echo", "hello"]` only | arguments `echo bye` | `echo bye` | `bye` |
| `CMD ["echo", "hello"]` only | argument `bye` | `bye` | fails: executable file `bye` not found |

- The process is the two lists joined: `ENTRYPOINT` words first, then `CMD` words.
- Words typed after the image name take the place of the `CMD` words, and the `ENTRYPOINT` words stay.
- With no `ENTRYPOINT`, `CMD` is the whole process, program included, and run arguments must then start with a program.
- `--entrypoint` replaces `ENTRYPOINT` and drops `CMD` as well.
- `ENTRYPOINT` and `CMD` are lists in the exec form, `ENTRYPOINT ["sh"]`.\
  The shell form `ENTRYPOINT sh` is stored as `["/bin/sh", "-c", "sh"]`, and the `CMD` words then never reach the inner `sh`.\
  Checked: with `CMD ["-c", "echo hello world"]`, the exec form prints `hello world`, and the shell form prints nothing.

The mapping, for the same process `sh -c "echo hello world"`:

| Docker | Kubernetes | Example |
| --- | --- | --- |
| `ENTRYPOINT` | `command` | `["sh"]` |
| `CMD` | `args` | `["-c", "echo hello world"]` |

- `command` and `args` accept only a list of strings.\
  Checked: `command: sh` is rejected with `cannot unmarshal string into ... of type []string`, and `args: [sleep, 3600]` with `cannot unmarshal number into ... of type string`, so a number must be quoted, as in `"3600"`.
- In a YAML flow list the comma is the separator.\
  Checked: `args: [-c "echo hello world"]`, without the comma, is one element, and `sh` fails with `sh: illegal option -`.

### command and args in a Pod

Shape: the process = (`command`, or else the image `ENTRYPOINT`) followed by (`args`, or else the image `CMD`).\
Example: image `nginx` has `ENTRYPOINT ["/docker-entrypoint.sh"]` and `CMD ["nginx", "-g", "daemon off;"]`, so `args: ["echo", "hi"]` runs `/docker-entrypoint.sh echo hi` and prints `hi`.

- `command` replaces the image `ENTRYPOINT`, and `args` replaces the image `CMD`.
- Setting `command` without `args` drops the image `CMD` as well.\
  Checked: `command: ["/docker-entrypoint.sh"]` on `nginx` exits at once with no output, because `nginx -g "daemon off;"` is no longer passed.
- Setting `args` without `command` keeps the image `ENTRYPOINT`.
- Image `busybox` has no `ENTRYPOINT` and `CMD ["sh"]`, so on `busybox` the `args` alone are the whole process.
- `podman image inspect nginx` shows both values for `nginx`, under `Config.Entrypoint` and `Config.Cmd`.

### One list element is one word of the process

Shape: `args: ["<program>", "<word 1>", "<word 2>"]`, and Kubernetes never splits an element and never interprets `;`, `&&`, `|` or `$`.\
Example: on `busybox`, `args: ["echo", "hello", "world"]` prints `hello world`.

Checked on `busybox`, where `args` is the whole process:

| `args` | Output |
| --- | --- |
| `["echo", "hello", "world"]` | `hello world` |
| `["echo", "hello world"]` | `hello world` |
| `["echo hello world"]` | fails: `exec: "echo hello world": executable file not found in $PATH` |
| `["sh", "-c", "echo hello world"]` | `hello world` |
| `["sh", "-c", "echo", "hello world"]` | an empty line |
| `["sh", "-c", "echo hello; echo world"]` | `hello`, then `world` |
| `["echo", "hello;", "echo", "world"]` | `hello; echo world` |

- The first element is the program, so a first element holding spaces names a program that does not exist.
- `sh -c` reads exactly one element as its script, as "sh -c reads exactly one element as its script" below explains.
- Without `sh -c`, a `;` is just a character handed to the program.

### kubectl run and the words after `--`

Shape: `kubectl run` flags come before `--`, and every word after `--` becomes one element of `args`, or of `command` when `--command` is given.\
Example: `kubectl run b --image=busybox --restart=Never -- echo hello world` sets `args: ["echo", "hello", "world"]` and prints `hello world`.

Checked with `--dry-run=client`:

| Command line ends with | Result |
| --- | --- |
| `-- echo hello world` | `args: ["echo", "hello", "world"]` |
| `--command -- echo hello world` | `command: ["echo", "hello", "world"]` |

- On `busybox` both lines run the same process, because `busybox` has no `ENTRYPOINT`.
- On `nginx` they differ: without `--command`, the words run after `/docker-entrypoint.sh`, and with `--command`, they replace it.
- The shell on your machine splits the line into words before kubectl runs, so quotes decide where an element ends.
- On the `kubectl run` line, the words fill either `args` or `command`, never both.\
  In YAML both can be set:

| `command` | `args` | Process |
| --- | --- | --- |
| set | set | `command` + `args` |
| set | unset | `command` only, and the image `CMD` is dropped |
| unset | set | image `ENTRYPOINT` + `args` |
| unset | unset | image `ENTRYPOINT` + image `CMD` |

### Which one to use

- To run a specific program, use `--command`, or set `command` in YAML.\
  `command` replaces the image `ENTRYPOINT` whatever it is, and the image `CMD` is ignored, so the process is exactly the typed words on any image.\
  Example: `kubectl run t --image=nginx --restart=Never --command -- sleep 30` runs `sleep 30`.
- To run the image's own program with different arguments, such as a flag for an application, use plain `--`, or set `args` in YAML.\
  Only then does the image `ENTRYPOINT` matter, and it is the image's normal program.
- Plain `--` also runs a program on `busybox`, only because `busybox` has no `ENTRYPOINT`.\
  On `nginx`, `-- sleep 30` runs `/docker-entrypoint.sh sleep 30`: the script skips its setup unless its first argument is `nginx`, then hands over with `exec "$@"`, so the main process is `sleep 30`.

### Quoting on the command line

Shape: your shell splits the line at spaces, except inside quotes, and each resulting word becomes one list element.\
Example: `kubectl run q --image=busybox --restart=Never --command -- sh -c 'echo hello world'` sets `command: ["sh", "-c", "echo hello world"]` and prints `hello world`.

Checked with `--dry-run=client`, all with `--command`:

| After `--` | `command` | Output when run |
| --- | --- | --- |
| `sh -c 'echo hello world'` | `["sh", "-c", "echo hello world"]` | `hello world` |
| `sh -c "echo hello; echo world"` | `["sh", "-c", "echo hello; echo world"]` | `hello`, then `world` |
| `sh -c echo hello world` | `["sh", "-c", "echo", "hello", "world"]` | an empty line |
| `"sh -c 'echo hello world'"` | `["sh -c 'echo hello world'"]` | fails: `exec: "sh -c 'echo hello world'": executable file not found` |

- Quote the script after `sh -c` as one piece, and leave `sh` and `-c` unquoted.
- Quoting the whole `sh -c ...` makes one element, which Kubernetes takes as the program name.

### sh -c reads exactly one element as its script

Shape: `sh -c <script> <extra 1> <extra 2>`, where the script is only the element right after `-c`.\
Example: `sh -c 'echo hello world'` prints `hello world`, and `sh -c echo hello world` prints an empty line.

The first example: the quotes keep `echo hello world` together as element 3, so all of it is the script.

```
element 1   element 2   element 3
sh          -c          echo hello world
                        └── the script
```

The second example: the shell on your machine splits the words, so only `echo` is the script, and `echo` with no arguments prints an empty line.

```
element 1   element 2   element 3   element 4   element 5
sh          -c          echo        hello       world
                        └── the script
                                    └── extra elements, not part of the script
```

### An unquoted `;` ends the kubectl command on your machine

Shape: your shell treats an unquoted `;`, `&&`, `|` or `>` as its own syntax, before kubectl runs.\
Example: `kubectl run t --image=busybox --restart=Never --command -- sh -c echo one; echo two` creates the Pod with `command: ["sh", "-c", "echo", "one"]`, which prints an empty line, and then runs `echo two` on your machine, which prints `two` in your terminal.

### When a shell is needed

Shape: use `sh -c '<script>'` only when the command uses shell syntax: `;`, `&&`, `||`, `|`, `>`, `<`, `$VAR`, `*`, or a loop.\
Example: `["echo", "$HOME"]` prints `$HOME`, and `["sh", "-c", "echo $HOME"]` prints `/root`.

Checked on `busybox`:

| Without a shell | Prints | With `sh -c` | Prints |
| --- | --- | --- | --- |
| `["echo", "$HOME"]` | `$HOME` | `["sh", "-c", "echo $HOME"]` | `/root` |
| `["echo", "hi", ">", "/tmp/x"]` | `hi > /tmp/x` | `["sh", "-c", "echo hi > /tmp/x; cat /tmp/x"]` | `hi` |
| `["ls", "/etc/*.conf"]` | `ls: /etc/*.conf: No such file or directory` | `["sh", "-c", "ls /etc/*.conf"]` | `/etc/nsswitch.conf`, `/etc/resolv.conf` |

- Without a shell, these characters reach the program as plain text.
- A plain program with plain arguments, such as `["sleep", "3600"]`, needs no shell.

### Writing the list in YAML

Shape: the same list can be written inline as `["a", "b"]`, or as lines starting with `- `, where every `- ` starts one element, and a `- |` element holds a multi-line script as one string.\
Example: `command: ["sh", "-c", "echo one; echo two"]` and the block below run the same kind of process.

```yaml
command:
- sh
- -c
- |
  echo one
  for i in 1 2; do echo "loop $i"; done
  echo done
```

Checked: the block above becomes `["sh", "-c", "echo one\nfor i in 1 2; do echo \"loop $i\"; done\necho done\n"]` and prints `one`, `loop 1`, `loop 2`, `done`.

- `- |` keeps the lines and their line breaks as one element, so the whole script stays the single element after `-c`.
- Each line of the script is one shell command, so no `;` is needed between lines.

### `$(VAR)` expanded by Kubernetes, `$VAR` expanded by a shell

Shape: in `command` and `args`, Kubernetes replaces `$(VAR)` with the value of the container's `env` variable `VAR` before the container starts, and only a shell replaces `$VAR`.\
Example: with `env` `DELAY` set to `"3"`, `["echo", "$(DELAY)"]` prints `3`, and `["echo", "$DELAY"]` prints `$DELAY`.

Checked on `busybox`, with `env` `DELAY` set to `"3"`:

| `command` | Prints |
| --- | --- |
| `["echo", "$(DELAY)"]` | `3` |
| `["echo", "$DELAY"]` | `$DELAY` |
| `["sh", "-c", "echo $DELAY"]` | `3` |
| `["echo", "$(NOPE)"]`, with no `NOPE` in `env` | `$(NOPE)` |

- `$(VAR)` needs no shell, so `["sleep", "$(DELAY)"]` works on any image.
- A variable missing from `env` is left as written, with no error.

### `--rm` on `kubectl run`

Shape: `kubectl run <name> --image=<image> --restart=Never --rm -i -- <command>` shows the output in your terminal, then deletes the Pod when the command ends.\
Example: `kubectl run rmtest --image=busybox --restart=Never --rm -i -- echo hi` prints `hi`, then `pod "rmtest" deleted`, and `kubectl get pod rmtest` then finds nothing.

- `--rm` works only while your terminal is attached to the Pod, so it needs `-i`, or `-it` for an interactive shell.\
  Checked: without `-i`, kubectl refuses with `--rm should only be used for attached containers`.
- `--restart=Never` makes the Pod run the command once.
