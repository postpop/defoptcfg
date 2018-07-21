# defoptcfg - the love child (or ugly chimera) of defopt and configargparser
Extends [defopt](https://github.com/evanunderscore/defopt) to read defaults from a [yaml](https://pyyaml.org) file.

running `test.py`:
```python
import defoptcfg
def main(greeting: str, *, name: str = 'Paul'):
    print(f"{greeting} {name}!")
defoptcfg.run(main)
```

[defopt](https://github.com/evanunderscore/defopt) will generate a command line interface from the function signature. Type information must be provided by annotating the function definition or in the doc string (see the defopt [docs](http://defopt.readthedocs.io/en/latest/) for details):
```shell
python test.py -h
usage: test.py [-h] [--cfg CFG] [-n NAME] [greeting]

positional arguments:
  greeting

optional arguments:
  -h, --help            show this help message and exit
  --cfg CFG             config file for setting defaults
  -n NAME, --name NAME
 ```
Configuration can be provided via yaml files. These override function defaults and are overridden by command line arguments.
```yaml
greeting: Salut
name: Ringo
```

```shell
python test.py Hello --cfg config.yml
Salut Ringo!
```
```shell
python test.py Hello --cfg config.yml -n John
Salut John!
```

Generally, the order of precedence for arguments is:
- command line arguments > config file >  function defaults
- if multiple config files are provided then
    - later files in default list override earlier ones and
    - the config file provided via command line arguments overrides the default config files.

## Future plans
- Needs much more testing. Does probably not work with defopt's advanced fatures (entrypoints, custom parsers etc)
- support interpolation (via jinja2?):  [here](http://dontfragment.com/using-python-yaml-and-jinja2-to-generate-config-files/), [here](https://stackoverflow.com/questions/42083616/yaml-and-jinja2-reader),
