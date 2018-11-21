import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
from matplotlib.ticker import NullLocator
import numpy as np
import glob
import os
from cobbi.core.data_logging import load_pickle
from cobbi.sandbox.quick_n_dirty_eval import experiment_naming_engine
from cobbi.core.visualization import MidpointNormalize, truncate_colormap,\
    imshow_ic, plot_glacier_contours, add_colorbar, get_axes_coords,\
    plot_surf_difference
from cobbi.core import test_cases
from oggm import cfg


cfg.initialize()

output_dir = '/media/philipp/Daten/Dokumente/Studium/Master/Masterarbeit' \
           '/Thesis/figs/surf_diff'
basedir = '/home/philipp/thesis/'
file_extension = 'pdf'


figsize = (4.5, 3)


for case in [test_cases.Giluwe, test_cases.Borden]:
    filepaths = glob.glob(os.path.join(basedir,
                                       '*/{:s}/*/data_logger.pkl'.format(
                                           case.name)))
    filepaths = sorted(filepaths)
    for path in filepaths:
        idir, temp = os.path.split(path)
        gdir, exp = os.path.split(idir)
        dl = load_pickle(path)
        exp_name = experiment_naming_engine.get_experiment_name(exp)
        if exp_name is not None:
            print(exp_name + ' ' + case.name)
            ice_mask = np.load(os.path.join(gdir, 'ref_ice_mask.npy'))

            diff_optimized_surf = dl.surfs[-1] - dl.ref_surf
            cbar_min = diff_optimized_surf.min()
            cbar_max = diff_optimized_surf.max()

            surf_noise = None
            if os.path.exists(os.path.join(idir, 'dem_noise.npy')):
                surf_noise = np.load(os.path.join(idir, 'dem_noise.npy'))
                cbar_min = min(surf_noise.min(), cbar_min)
                cbar_max = max(surf_noise.max(), cbar_max)

            cbar_min_max = max(abs(cbar_min), abs(cbar_max))
            norm = MidpointNormalize(midpoint=0., vmin=-cbar_min_max,
                                     vmax=cbar_min_max)
            #my_cmap = sns.diverging_palette(240, 15, l=40, s=99, as_cmap=True)
            my_cmap = plt.get_cmap('PuOr_r')
            if surf_noise is not None:
                plotpath = os.path.join(output_dir,
                                        '{:s}_{:s}_surf_noise.{'
                                        ':s}'.format(
                                            case.name, exp_name, file_extension))
                plot_surf_difference(surf_noise, plotpath, case,
                                     ice_mask=ice_mask, cbar_min=cbar_min,
                                     cbar_max=cbar_max, show_cbar=False,
                                     norm=norm, cmap=my_cmap, figsize=figsize)

            plotpath = os.path.join(output_dir,
                                    '{:s}_{:s}_surf_error.{:s}'.format(
                                        case.name, exp_name, file_extension))
            plot_surf_difference(diff_optimized_surf, plotpath, case,
                                 ice_mask=ice_mask, cbar_min=cbar_min,
                                 cbar_max=cbar_max, show_cbar=True,
                                 norm=norm, cmap=my_cmap, figsize=figsize)
                #'Bed errors case {:s}\n ''experiment {:s}'.format(case,exp_name),
            #exit()