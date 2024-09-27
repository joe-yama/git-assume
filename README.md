# git-assume: A CLI Tool to Switch Your .netrc Configuration

`git-assume` helps you manage multiple `.netrc` configurations with ease.

## Features

- List available `.netrc` profiles.
- Switch between different `.netrc` profiles.

## Installation

```sh
git clone https://github.com/tmc-coco/git-assume.git
cd git-assume
pip install .
```

## Prerequisites

### Create `.netrc-longterm` File

Create a `.netrc-longterm` file in your home directory. This file should be in [INI file](https://w.wiki/BL3e) format, with each section representing a different `.netrc` profile.

Example `.netrc-longterm`:

```ini
[default]
machine = github.com
login = someone-foo
password = ghp_xxxxxxxxxx

[sub]
machine = github.tmc-stargate.com
login = someone-hoge
password = ghp_yyyyyyyyyy
```

> **CAUTION:** Your Git password is stored in plain text. Ensure that the permissions of your `.netrc-longterm` file are restricted to you.

### Backup Your `.netrc` File (Optional)

Since this tool overwrites your `.netrc` file, it's advisable to back it up before running the CLI.

```sh
cp ~/.netrc ~/.netrc-backup
```

## Basic Usage

`git-assume` provides two subcommands: `list` and `assume`.

### `list`: List Available Profiles

Use the `list` subcommand to display current profiles:

```sh
$ git-assume list
Profiles that exist in .netrc-longterm: /home/someone/.netrc-longterm
- default
- sub
```

| Argument           | Required | Default           | Detail                                                                          |
| ------------------ | -------- | ----------------- | ------------------------------------------------------------------------------- |
| `--netrc-longterm` | No       | ~/.netrc-longterm | Filepath to your `.netrc-longterm`.                                             |
| `--log-level`      | No       | INFO              | Log level. Choices: ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"] |

### `assume`: Switch Your .netrc Profile

Use the `assume` subcommand to switch profiles:

```sh
$ git-assume assume default
Are you sure you want to overwrite /home/someone/.netrc with profile `default`? [Y/n] Y
INFO - Successfully wrote to .netrc: /home/someone/.netrc
```

| Argument           | Required | Default           | Detail                                                                             |
| ------------------ | -------- | ----------------- | ---------------------------------------------------------------------------------- |
| `--netrc-longterm` | No       | ~/.netrc-longterm | Filepath to your `.netrc-longterm`.                                                |
| `--netrc`          | No       | ~/.netrc          | Filepath to your `.netrc`.                                                         |
| `--log-level`      | No       | INFO              | Log level. Choices: ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]    |
| `-y, --yes`        | No       | False             | If True, it overwrites `.netrc` file without any confirmation.                     |

## How It Works

When you run the `assume` subcommand, `git-assume` overwrites your `.netrc` file with the profile specified.

## Example Workflow

```sh
$ git pull origin main
Username for 'https://github.com/xxx/yyy.git':
^C

$ git-assume list
Profiles that exist in .netrc-longterm: /home/someone/.netrc-longterm
- default
- sub

$ git-assume assume sub
Are you sure you want to overwrite /home/someone/.netrc with profile `default`? [Y/n] Y
INFO - Successfully wrote to .netrc: /home/someone/.netrc

$ git pull origin main
Already up to date.
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
