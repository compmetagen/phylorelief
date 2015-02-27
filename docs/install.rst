Installation
============

Requirements
------------

 * Linux or OSX systems
 * Python >= 2.7
 * NumPy and SciPy (http://scipy.org)
 * Pandas (http://pandas.pydata.org
 * DendroPy (http://pythonhosted.org/DendroPy/)
 * Statsmodels (http://statsmodels.sourceforge.net/)

On Linux
    Required Python modules can easily installed by running the package
    manager or using ``easy_install``:

    .. code-block:: sh

        $ sudo easy_install numpy scipy pandas dendropy statsmodels

On OSX
    1. Install the gfortran compiler from
       http://cran.r-project.org/bin/macosx/tools/ (required by SciPy)

    2. Install the Python modules by running ``easy_install``:
   
       .. code-block:: sh
       
           $ sudo easy_install numpy scipy pandas dendropy


Installing PhyloRelief
----------------------

1. Untar ``phylorelief-X.Y.Z.tar.gz``, creating ``phylorelief-X.Y.Z`` folder (where
   ``X.Y.Z`` is the current version of phylorelief)

2. Go into ``phylorelief-X.Y.Z`` folder and from a terminal run:

   .. code-block:: sh

      $ sudo python setup.py install

3. If you don't have root access, installing phylorelief in a directory by
   specifying the ``--prefix`` argument. Then you need to set tht 
   ``PYTHONPATH`` environment variable:

   .. code-block:: sh

      $ python setup.py install --prefix=/path/to/modules
      $ export PYTHONPATH=$PYTHONPATH:/path/to/modules/lib/python{version}/site-packages

 
4. Test the installation:

   .. command-output:: phylorelief
       :ellipsis: 10
