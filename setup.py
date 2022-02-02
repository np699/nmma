#!/usr/bin/env python

from setuptools import setup
import subprocess
import sys
import os

# check that python version is 3.5 or above
python_version = sys.version_info
if python_version < (3, 5):
    sys.exit("Python < 3.5 is not supported, aborting setup")
print("Confirmed Python version {}.{}.{} >= 3.5.0".format(*python_version[:3]))


def write_version_file(version):
    """ Writes a file with version information to be used at run time

    Parameters
    ----------
    version: str
        A string containing the current version information

    Returns
    -------
    version_file: str
        A path to the version file

    """
    try:
        git_log = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%h %ai']).decode('utf-8')
        git_diff = (subprocess.check_output(['git', 'diff', '.']) +
                    subprocess.check_output(
                        ['git', 'diff', '--cached', '.'])).decode('utf-8')
        if git_diff == '':
            git_status = '(CLEAN) ' + git_log
        else:
            git_status = '(UNCLEAN) ' + git_log
    except Exception as e:
        print("Unable to obtain git version information, exception: {}"
              .format(e))
        git_status = ''

    version_file = '.version'
    if os.path.isfile(version_file) is False:
        with open('nmma/' + version_file, 'w+') as f:
            f.write('{}: {}'.format(version, git_status))

    return version_file


def get_long_description():
    """ Finds the README and reads in the description """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst')) as f:
        long_description = f.read()
    return long_description


def get_requirements():
    with open("requirements.txt", "r") as ff:
        requirements = ff.readlines()
    return requirements


# get version info from __init__.py
def readfile(filename):
    with open(filename) as fp:
        filecontents = fp.read()
    return filecontents


VERSION = '0.0.1'
version_file = write_version_file(VERSION)
long_description = get_long_description()

setup(name='nmma',
      description='A nuclear physics multi-messenger Bayesian inference library',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      url='https://git.ligo.org/tsun-ho.pang/nmma',
      author='Peter Tsun Ho Pang, Michael Coughlin, Tim Dietrich, Ingo Tews',
      author_email='thopang@nikhef.nl',
      license="MIT",
      version=VERSION,
      packages=['nmma', 'nmma.em', 'nmma.em.data', 'nmma.joint', 'nmma.eos', 'nmma.pbilby'],
      package_dir={'nmma': 'nmma'},
      package_data={'nmma': [version_file], 'nmma.em.data': ['*.pkl','*.joblib']},
      python_requires='>=3.5',
      install_requires=get_requirements(),
      entry_points={
          "console_scripts": ["nmma_analysis=nmma.pbilby.analysis:main",
                              "nmma_generation=nmma.pbilby.generation:main",
                              "parallel_em_analysis=nmma.pbilby.em_analysis:main",
                              "parallel_em_generation=nmma.pbilby.em_generation:main",
                              "light_curve_analysis=nmma.em.analysis:main",
                              "light_curve_injection_summary=nmma.em.injection_summary:main",
                              "light_curve_injection_slurm_setup=nmma.em.create_injection_slurm:main",
                              "light_curve_injection_condor_setup=nmma.em.create_injection_condor:main",
                              "lightcurve_marginalization=nmma.em.lightcurve_marginalization:main",
                              "create_light_curve_slurm=nmma.em.create_lightcurves_slurm:main",
                              "create_light_curve_condor=nmma.em.create_lightcurves_condor:main",
                              "light_curve_generation=nmma.em.create_lightcurves:main",
                              "light_curve_detection=nmma.em.detect_lightcurves:main",
                              "nmma_create_injection=nmma.eos.create_injection:main",
                              "gwem_resampling=nmma.em.gwem_resampling:main",
                              "gwem_resampling_condor=nmma.em.gwem_resampling_condor:main",
                              "gwem_Hubble_estimate=nmma.em.gwem_Hubble_estimate:main"]
      },
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"])
