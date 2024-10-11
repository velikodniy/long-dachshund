# Long Dachshund

A script for creating long dachshund 3D models.

## Usage

The script is self-contained and doesn't require any dependencies.

You can list the arguments by running the script with the `-h` flag.

This command make the dachshund body 2x longer and writes the result to `dachshung-long.obj`.

```sh
python3.10 stretch.py -s 2 -o dachshund-long.obj
```

## Development

Before you start, please install [pre-commit hooks](https://pre-commit.com/) with

```sh
pre-commit install
```

## Limitations

Note that the script expects that the original model is in the `dachshund.obj` file.
You can use another model, but it should be oriented in the same way as the original dachshund.

Currently, the body is not detected automatically.
Since the base model is static, it's more practical to pre-compute the values ans save to `dachshund.json`.

The script doesn't update the texture coordinates, so the texture will be stretched.
Also, the normals are not recalculated, so the lighting may look weird.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

[The original Dachshund model](https://www.thingiverse.com/thing:182122) is created by [Yahoo! JAPAN](https://www.thingiverse.com/yahoojapan/designs) and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
