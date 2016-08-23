#!/usr/bin/env sh


LD_LIBRARY_PATH="/auto/cmb-08/fa/local/software/imp2.5/lib:/home/cmb-08/fa/local/software/imp2.5/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

PYTHONPATH="$PYTHONPATH:/home/cmb-08/fa/local/software/imp2.5/lib:/home/cmb-08/fa/local/software/imp2.5/lib"
export PYTHONPATH

# Where to find data for the various modules
IMP_DATA="/auto/cmb-08/fa/local/software/imp2.5/data"
export IMP_DATA

# Extra places to look for imp modules
IMP_EXAMPLE_DATA="/auto/cmb-08/fa/local/software/imp2.5/doc/examples"
export IMP_EXAMPLE_DATA

# Location of binaries (for wine builds, which don't get PATH)
IMP_BIN_DIR="/auto/cmb-08/fa/local/software/imp2.5/bin"
export IMP_BIN_DIR

PATH="/auto/cmb-08/fa/local/software/imp2.5/bin:/auto/cmb-08/fa/local/software/imp2.5/module_bin/EMageFit:/auto/cmb-08/fa/local/software/imp2.5/module_bin/algebra:/auto/cmb-08/fa/local/software/imp2.5/module_bin/atom:/auto/cmb-08/fa/local/software/imp2.5/module_bin/benchmark:/auto/cmb-08/fa/local/software/imp2.5/module_bin/cgal:/auto/cmb-08/fa/local/software/imp2.5/module_bin/cnmultifit:/auto/cmb-08/fa/local/software/imp2.5/module_bin/container:/auto/cmb-08/fa/local/software/imp2.5/module_bin/core:/auto/cmb-08/fa/local/software/imp2.5/module_bin/display:/auto/cmb-08/fa/local/software/imp2.5/module_bin/domino:/auto/cmb-08/fa/local/software/imp2.5/module_bin/em:/auto/cmb-08/fa/local/software/imp2.5/module_bin/em2d:/auto/cmb-08/fa/local/software/imp2.5/module_bin/example:/auto/cmb-08/fa/local/software/imp2.5/module_bin/foxs:/auto/cmb-08/fa/local/software/imp2.5/module_bin/gsl:/auto/cmb-08/fa/local/software/imp2.5/module_bin/integrative_docking:/auto/cmb-08/fa/local/software/imp2.5/module_bin/isd:/auto/cmb-08/fa/local/software/imp2.5/module_bin/kernel:/auto/cmb-08/fa/local/software/imp2.5/module_bin/kinematics:/auto/cmb-08/fa/local/software/imp2.5/module_bin/kmeans:/auto/cmb-08/fa/local/software/imp2.5/module_bin/misc:/auto/cmb-08/fa/local/software/imp2.5/module_bin/modeller:/auto/cmb-08/fa/local/software/imp2.5/module_bin/mpi:/auto/cmb-08/fa/local/software/imp2.5/module_bin/multi_state:/auto/cmb-08/fa/local/software/imp2.5/module_bin/multifit:/auto/cmb-08/fa/local/software/imp2.5/module_bin/parallel:/auto/cmb-08/fa/local/software/imp2.5/module_bin/pepdock:/auto/cmb-08/fa/local/software/imp2.5/module_bin/pmi:/auto/cmb-08/fa/local/software/imp2.5/module_bin/rmf:/auto/cmb-08/fa/local/software/imp2.5/module_bin/rotamer:/auto/cmb-08/fa/local/software/imp2.5/module_bin/saxs:/auto/cmb-08/fa/local/software/imp2.5/module_bin/saxs_merge:/auto/cmb-08/fa/local/software/imp2.5/module_bin/score_functor:/auto/cmb-08/fa/local/software/imp2.5/module_bin/scratch:/auto/cmb-08/fa/local/software/imp2.5/module_bin/statistics:/auto/cmb-08/fa/local/software/imp2.5/module_bin/symmetry:/auto/cmb-08/fa/local/software/imp2.5/module_bin/test:/auto/cmb-08/fa/local/software/imp2.5/bin:/home/cmb-08/fa/local/software/imp2.5/bin:$PATH"
export PATH


IMP_TMP_DIR="/auto/cmb-08/fa/local/software/imp2.5/tmp"
export IMP_TMP_DIR


mkdir -p ${IMP_TMP_DIR}

exec ${precommand} "$@"
