Figures Demo
============

This page demonstrates the ``.. plot::`` directive from
``matplotlib.sphinxext.plot_directive`` for generating figures
directly from Python code in Sphinx documentation.

Referencing an external script
------------------------------

.. plot:: examples/plot_rpolygon.py

.. plot:: examples/plot_rectangles.py

The plot inline directive
-------------------------

You can also embed the plotting code directly in the RST file.
Here is a simple rectangle:

.. plot::

   import matplotlib.pyplot as plt
   import matplotlib.patches as mpatches
   from physdes.interval import Interval
   from physdes.recti import Rectangle

   r = Rectangle(Interval(2, 7), Interval(1, 5))
   fig, ax = plt.subplots(figsize=(5, 4))
   rect = mpatches.Rectangle((r.xcoord.lb, r.ycoord.lb),
                              r.xcoord.ub - r.xcoord.lb,
                              r.ycoord.ub - r.ycoord.lb,
                              facecolor="lightgreen", edgecolor="black", lw=2)
   ax.add_patch(rect)
   ax.text((r.xcoord.lb + r.xcoord.ub) / 2, (r.ycoord.lb + r.ycoord.ub) / 2,
           "Rectangle", ha="center", va="center", fontsize=12)
   ax.set_xlim(0, 10)
   ax.set_ylim(0, 8)
   ax.set_aspect("equal")
   ax.grid(True, alpha=0.3)
   ax.set_title("A single Rectangle")

Clock Tree Synthesis
--------------------

.. plot:: examples/plot_cts.py

Global Router
-------------

.. plot:: examples/plot_global_router.py

Controlling options
-------------------

Use ``:width:``, ``:alt:``, and ``:align:`` as with any figure:

.. plot:: examples/plot_rpolygon.py
   :width: 60%
   :align: center
   :alt: Rectilinear polygon at 60% width
