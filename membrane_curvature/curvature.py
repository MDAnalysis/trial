r"""

--------------------
Curvature
--------------------

In MembraneCurvature, we calculate Gaussian and mean curvature from a cloud of points.

Gaussian curvature is defined by

.. math:: K = \frac{\partial_{xx}\partial_{yy}-\partial_{xy}^2}
   {(1+\partial_x^2+\partial_y^2)^2}.

Mean curvature is defined by

.. math:: H =
    \frac{(1+\partial_x^2)\partial_{yy}+(1+\partial_y^2)\partial_{xx}-2\partial_x\partial_y\partial_{xy}}
    {2(1+\partial_x^2+\partial_y^2)^{3/2}}.


Notes
---------

Since the mean curvature calculates the arithmetic mean of two
principal curvatures, the default units of :math:`H` are Å\ :sup:`-1`.
On the other hand, Gaussian curvature calculates the geometric mean of the
two principal curvatures. Therefore, the default units of :math:`K` are Å\ :sup:`-2`.
In general, units of mean curvature are [length] :sup:`-1`,
and units of Gaussian curvature are [length] :sup:`-2`.

.. warning::

    Numpy cannot calculate the gradient for arrays with inner array of
    `length==1` unless `axis=0` is specified. Therefore in the functions here included
    for mean and Gaussian curvature, shape of arrays must be at least (2,2).
    In general, to calculate a numerical gradients shape of arrays must be >=(`edge_order` +
    1).


Functions
---------

"""

import numpy as np


def gaussian_curvature(Z, *varargs):
    """
    Calculate Gaussian curvature from Z cloud points.


    Parameters
    ----------
    Z: np.ndarray.
        Multidimensional array of shape (n,n).
    varargs : list of scalar or array, optional
        Spacing between f values. Default unitary spacing for all dimensions.
        See np.gradient docs for more information.

    Returns
    -------
    K : np.ndarray.
        The result of Gaussian curvature of Z. Returns multidimensional
        array object with values of Gaussian curvature of shape `(n, n)`.

    """

    Zx, Zy = np.gradient(Z, *varargs)
    Zxx, Zxy = np.gradient(Zx, *varargs)
    _, Zyy = np.gradient(Zy, *varargs)

    K = (Zxx * Zyy - (Zxy**2)) / (1 + (Zx**2) + (Zy**2)) ** 2

    return K


def mean_curvature(Z, *varargs):
    """
    Calculates mean curvature from Z cloud points.


    Parameters
    ----------
    Z: np.ndarray.
        Multidimensional array of shape (n,n).
    varargs : list of scalar or array, optional
        Spacing between f values. Default unitary spacing for all dimensions.
        See np.gradient docs for more information.

    Returns
    -------
    H : np.ndarray.
        The result of mean curvature of Z. Returns multidimensional
        array object with values of mean curvature of shape `(n, n)`.

    """

    Zx, Zy, = np.gradient(Z, *varargs)
    Zxx, Zxy = np.gradient(Zx, *varargs)
    _, Zyy = np.gradient(Zy, *varargs)

    H = (1 + Zx**2) * Zyy + (1 + Zy**2) * Zxx - 2 * Zx * Zy * Zxy
    H = H / (2 * (1 + Zx**2 + Zy**2) ** (1.5))

    return H
