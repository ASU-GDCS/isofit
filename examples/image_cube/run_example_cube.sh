
# Download relevant datasets - unlike other examples, these datasets are too large to place in
if [ ! -e test_data.zip ] ; then
    curl -O https://avng.jpl.nasa.gov/pub/PBrodrick/isofit/test_data.zip
    unzip test_data.zip
fi

n_cores=4

isofit_base_path=$(python -c "import isofit; import os; print(os.path.dirname(isofit.__file__))")
file_base=ang20170323t202244

if [ ! -e configs/basic_surface.mat ]; then
    python -c "from isofit.utils import surface_model; surface_model('configs/basic_surface.json')"
fi

# Small test (10x10 pixels, no empirical line) - this should take   2-3 minutes with n_cores = 4.
python ${isofit_base_path}/utils/apply_oe.py small_chunk/${file_base}_rdn_7000-7010 small_chunk/${file_base}_loc_7000-7010 small_chunk/${file_base}_obs_7000-7010 small_chunk_test_emulator ang --presolve=1 --empirical_line=0 --emulator_base=${EMULATOR_PATH} --n_cores ${n_cores} --surface_path configs/basic_surface.mat --copy_input_files 0

# Medium test (1000x598 pixels, empirical line) - this should take ~45 minutes with n_cores = 4
python ${isofit_base_path}/utils/apply_oe.py medium_chunk/${file_base}_rdn_7k-8k medium_chunk/${file_base}_loc_7k-8k medium_chunk/${file_base}_obs_7k-8k medium_chunk_test_emulator ang --presolve=1 --empirical_line=1 --emulator_base=${EMULATOR_PATH} --n_cores ${n_cores} --surface_path configs/basic_surface.mat --segmentation_size 400
