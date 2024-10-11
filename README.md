# Long Dachshund

A script for creating long dachshund 3D models.

![Long dachshund](images/long-dachshund.png)

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

## How it works

The script stretches the dog's body along the axis.
Do do this we need to define an function mapping the corresponding coordinate.

To make stretching smooth we can use a cubic function with the following constraints:

- the points at the bedy boundaries should have the same coordinates as if they're stretched linearly,
- the derivative of the mapping function at the body boundaries should be equal to 1 to make the function smooth.

The cubic function fits perfectly well (even though it's not guaranteed that the average curvature will be minimal).
It has enough degrees of freedom to constrain both the points and angles.

To get the coefficients of the cubic polynomial $a x^3 + b x^2 + c x + d$ we have to solve a system of linear equations:

$$a x_\text{min}^3 + b x_\text{min}^2 + c x_\text{min} + d = x_\text{min},$$
$$a x_\text{max}^3 + b x_\text{max}^2 + c x_\text{max} + d = s (x_\text{max} - x_\text{min}) + x_\text{min},$$
$$3 a x_\text{min}^2 + 2 b x_\text{min} + c = 1,$$
$$3 a x_\text{max}^2 + 2 b x_\text{max} + c = 1.$$

This system can be solved in advanced, and the solution is

$$a = -\frac{2 (s-1)}{(x_\text{max}-x_\text{min})^2},$$
$$b = \frac{3 (s-1) (x_\text{max}+x_\text{min})}{(x_\text{max}-x_\text{min})^2},$$
$$c = \frac{(4 - 6 s) x_\text{max} x_\text{min} + x_\text{max}^2 + x_\text{min}^2}{(x_\text{max}-x_\text{min})^2},$$
$$d = \frac{(s-1) x_\text{min}^2 (3 x_\text{max} - x_\text{min})}{(x_\text{max}-x_\text{min})^2}.$$

The mapping will look like the following.

![Cubic stretch](images/mapping.png)

### Limitations

Note that the script expects that the original model is in the `dachshund.obj` file.
You can use another model, but it should be oriented in the same way as the original dachshund.

Currently, the body is not detected automatically.
Since the base model is static, it's more practical to pre-compute the values ans save to `dachshund.json`.

The script doesn't update the texture coordinates, so the texture will be stretched.
Also, the normals are not recalculated, so the lighting may look weird.

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

## Credits

[The original Dachshund model](https://www.thingiverse.com/thing:182122) is created by [Yahoo! JAPAN](https://www.thingiverse.com/yahoojapan/designs) and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
