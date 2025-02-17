.. _usage:

Usage
=========================================================

In this page, you can find examples of how to use MembraneCurvature to derive
curvature profiles in three types of systems:

:ref:`membrane-only`.

:ref:`membrane-protein`.

        :ref:`membrane-protein-pr`.

        :ref:`membrane-protein-no-pr`.

.. note::
   Examples included in this page show how to use MembraneCurvature
   using data files from `MDAnalysisTests`_. In order to run the examples
   here provided, `MDAnalysisTests`_ must be installed.


.. _membrane-only:

1. Membrane-only systems
-----------------------------

In this example, we show a basic usage of MembraneCurvature in a system that
comprises a lipid bilayer of DPPC:CHOL using the Martini force field. Since we
have a bilayer, we select atoms of phoshpholipid head groups in the upper
leaflet only using the :attr:`~select` parameter and apply coordinate wrapping.
Once we run :attr:`~MembraneCurvature`, we can extract the values of mean and
Gaussian curvature::

        import MDAnalysis as mda
        from membrane_curvature.base import MembraneCurvature
        from MDAnalysis.tests.datafiles import Martini_membrane_gro

        universe = mda.Universe(Martini_membrane_gro)
        
        curvature_upper_leaflet = MembraneCurvature(universe, 
                                                    select='resid 1-225 and name PO4', 
                                                    n_x_bins=8, 
                                                    n_y_bins=8, 
                                                    wrap=True).run()


        # extract mean curvature
        mean_upper_leaflet = curvature_upper_leaflet.results.average_mean

        # extract Gaussian
        gaussian_upper_leaflet = curvature_upper_leaflet.results.average_gaussian

You can find more complex examples in the tutorial notebooks.


.. _membrane-protein:

2.1 Membrane-protein systems
------------------------------


.. _membrane-protein-pr:

2.1.1 Membrane-protein systems, protein with position restraints
------------------------------------------------------------------

In this example, we have a simulation box comprising a copy of the Yiip
transporter, embedded in a lipid bilayer of POPE:POPG. Similar to the example
for membrane-only, we select the atoms for the upper leaflet and apply
coordinate wrapping. Then, we can calculate membrane curvature as::

        import MDAnalysis as mda
        from membrane_curvature.base import MembraneCurvature
        from MDAnalysis.tests.datafiles import XTC_MEMPROT, GRO_MEMPROT

        universe = mda.Universe(GRO_MEMPROT, XTC_MEMPROT)
        
        curvature_upper_leaflet = MembraneCurvature(universe,
                                               select='resid 297-517 and name P', 
                                               n_x_bins=2, 
                                               n_y_bins=2, 
                                               wrap=True).run

        avg_mean_curvature_upper_leaflet = curvature_upper_leaflet.results.average_mean_curvature

.. note::
        When passing raw trajectories, in systems of :ref:`membrane-only` and 
        :ref:`membrane-protein-pr` set :attr:`~wrap=True` to improve sampling. 

Some points to keep in mind when calculating membrane curvature in :ref:`membrane-only`
and :ref:`membrane-protein-pr` are addressed in this `blog post`_. 

.. _membrane-protein-no-pr:

2.1.2. Membrane-protein systems, protein with no position restraints
---------------------------------------------------------------------

For membrane-protein systems where the simulation setup has no position
restraints on the protein, a trajectory preprocessing by the user is required.
If the goal is to assess membrane curvature induced by the protein, the 
preprocessed trajectory should have the protein centered in the simulation box 
with translational and rotational fit.

In `Gromacs`_, the trajectory would be preprocessed with::

        gmx trjconv -pbc whole -ur compact -c
        gmx trjconv -fit rot+transxy

After you have preprocessed the trajectory, a typical usage of membrane curvature is::

        import MDAnalysis as mda
        from membrane_curvature.base import MembraneCurvature
        from membrane_curvature.tests.datafiles import XTC_MEMBPROT_FIT, GRO_MEMBPROT_FIT

        universe = mda.Universe(GRO_MEMBPROT_FIT, XTC_MEMBPROT_FIT)
        
        curvature_lower_leaflet = MembraneCurvature(universe, 
                                                    select='resid 2583-3042', 
                                                    wrap=False, # wrap=False when passing preprocessed trajs!
                                                    n_x_bins=10,
                                                    n_y_bins=10).run()

        avg_mean_curvature  = curvature_lower_leaflet.results.average_mean

.. note::

        Since you are providing a preprocess trajectory with translation/rotational fit 
        you can ignore the warning message: 
        ``WARNING   `wrap == False` may result in inaccurate calculation of membrane curvature.`` 
        


More information on how to visualize the results of the MDAnalysis Membrane 
Curvature tool can be found in the :ref:`visualization` page.

.. _`blog post`: https://ojeda-e.com/blog/2021/07/22/Considerations-curvature-MD-simulations-PartI.html

.. _`MDAnalysisTests`: https://github.com/MDAnalysis/mdanalysis/wiki/UnitTests

.. _`Gromacs`: https://www.gromacs.org/