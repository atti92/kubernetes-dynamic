# Contributing guide

## pre-commit

### Only once per system

#### Install pre-commit

```shell
pip install pre-commit
```

#### Init pre-commit template

Windows

```console
set "PCDIR=%USERPROFILE%\.git-template"
git config --global init.templateDir "%PCDIR%"
pre-commit init-templatedir -t pre-commit "%PCDIR%"
pre-commit init-templatedir -t commit-msg "%PCDIR%"
```

PowerShell

```powershell
$Env:PCDIR="${Env:USERPROFILE}\.git-template"
git config --global init.templateDir "${Env:PCDIR}"
pre-commit init-templatedir -t pre-commit "${Env:PCDIR}"
pre-commit init-templatedir -t commit-msg "${Env:PCDIR}"
```

Linux

```shell
PCDIR=~/.git-template
git config --global init.templateDir "${PCDIR}"
pre-commit init-templatedir -t pre-commit "${PCDIR}"
pre-commit init-templatedir -t commit-msg "${PCDIR}"
```

### Once per repo

Only needed if repo created before the template init.

```shell
pre-commit install
pre-commit install --hook-type commit-msg
```
