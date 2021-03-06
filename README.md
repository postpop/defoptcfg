# defoptcfg - defopt with config files
Extends [defopt][1] to read defaults from [yaml][2] files. Inspired by (but much worse than) [configargparse][3].

## Simple example
```python
import defoptcfg
def main(greeting: str, *, name: str = 'Paul'):
    """Greet someone.

    Args:
        greeting: How do you want to greet someone?
        name: Who do you want to greet?
    """
    print(f"{greeting} {name}!")
defoptcfg.run(main)
```
[defopt][1] is used to generate a command line interface from the function signature. Type information must be provided by annotating the function definition or via doc strings (see defopt's [docs][4] for details):
```text
python test.py -h
usage: test.py [-h] [-n NAME] [--cfg CFG] [greeting]

Greet someone.

positional arguments:
  greeting              How do you want to greet someone?

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Who do you want to greet?
                        (default: Paul)
  --cfg CFG             config file for setting defaults
```
Configuration can also be provided via yaml files. Arguments from config files override function defaults and are overridden by command line arguments. Keys in the config file must match the full argument name:
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
## Installation
In a terminal window run
```shell
pip install git+http://github.com/postpop/defoptcfg.git
```
## More complex use case
Say you have written a function in `train_network.py` that runs a complex machine learning task and has many, many parameters for flexibility:
```python
import defoptcfg

def train_network(data_path: str, *,
                  base_output_path: str = "models",
                  run_name: str = None,
                  data_name: str = None,
                  x_dset: str = "images",
                  y_dset: str = "masks",
                  val_size: float = 0.15,
                  filters: int = 32,
                  rotate_angle: float = 15,
                  epochs: int = 50,
                  batch_size: int = 32,
                  save_every_epoch: int = False,
                  ):
    pass # do something magical here

if __name__ == '__main__':
    defoptcfg.run(train_network)
```
Thanks to [defopt][1], you automagically have a command line interface (provided you have properly [type annotated][5] or [docstring][6]'ed it, defopt's [docs][4] have all the details on how to do that) and can call the function like so:
```shell
python train_network.py /Volumes/share/data/exp1/data_20151021 --base-output-path /Volumes/share/networks/results --run-name test_more_filters --data-name fly-courtship --filters 64 --epochs 20 --batch_size 1
```
This is long. defoptcfg extends [defopt][1] to allow you to provide arguments that rarely change via a config file, e.g. `config.yml`:
```yaml
data_path: /Volumes/share/data/exp1/data_20151021_1629
base_output_path: /Volumes/share/networks/results
data-name: fly-courtship
epochs: 20
batch_size: 1
```
resulting in a much shorter command line:
```shell
python train_network.py --cfg config.yml --run-name test_more_filters --filters 64
```

## String interpolation in config files
In addition, string interpolation facilitates the structuring of config files:
```yaml
root: /Volumes/share
data_path: $root$/data
```
Values of any key in the config file can be turned into variables by surrounding with `$...$` (e.g. `$root$`). Their occurrences in any of the values will be
replaced by that key's value. In the above example, `$root$` in `$root$/data` will be replaced by `/Volumes/share` to become `/Volumes/share/data`.

__Warning__: Take care when using this feature since the current implementation does only incompletely guard against recursion catastrophes. For instance, a config file with `root1: $root2$; root2: $root1$` will result in an endless cycle of interpolations. Current safeguard is to limit the number of cycles to 20 with the `n_iter` parameter.

## Default config files
Default config files can be provided via
```python
defoptcfg.run(main, default_config_files=['a.yml', 'b.yml'])
```
Precedence is according to order in list of files. Values in `a.yml` are overridden by those in `b.yml`, which in turn are overridden by those in the config file provided via the command line.

## Future plans
- Needs much more testing. Does probably not work with defopt's advanced features (entry points, custom parsers etc)
- Better support and more robust support for string interpolation (via jinja2?):  [here](http://dontfragment.com/using-python-yaml-and-jinja2-to-generate-config-files/), [here](https://stackoverflow.com/questions/42083616/yaml-and-jinja2-reader),

[1]: https://github.com/evanunderscore/defopt
[2]: https://pyyaml.org
[3]: https://github.com/bw2/ConfigArgParse
[4]: http://defopt.readthedocs.io/en/latest/
[5]: linktopythonannotations
[6]: linktodocstringformats
