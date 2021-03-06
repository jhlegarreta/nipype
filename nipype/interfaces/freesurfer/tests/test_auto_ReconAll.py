# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import ReconAll


def test_ReconAll_inputs():
    input_map = dict(T1_files=dict(argstr='-i %s...',
    ),
    T2_file=dict(argstr='-T2 %s',
    min_ver='5.3.0',
    ),
    args=dict(argstr='%s',
    ),
    directive=dict(argstr='-%s',
    position=0,
    usedefault=True,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    flags=dict(argstr='%s',
    ),
    hemi=dict(argstr='-hemi %s',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    openmp=dict(argstr='-openmp %d',
    ),
    parallel=dict(argstr='-parallel',
    ),
    subject_id=dict(argstr='-subjid %s',
    usedefault=True,
    ),
    subjects_dir=dict(argstr='-sd %s',
    genfile=True,
    hash_files=False,
    ),
    terminal_output=dict(nohash=True,
    ),
    use_T2=dict(argstr='-T2pial',
    min_ver='5.3.0',
    ),
    )
    inputs = ReconAll.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_ReconAll_outputs():
    output_map = dict(BA_stats=dict(altkey='BA',
    loc='stats',
    ),
    T1=dict(loc='mri',
    ),
    annot=dict(altkey='*annot',
    loc='label',
    ),
    aparc_a2009s_stats=dict(altkey='aparc.a2009s',
    loc='stats',
    ),
    aparc_aseg=dict(altkey='aparc*aseg',
    loc='mri',
    ),
    aparc_stats=dict(altkey='aparc',
    loc='stats',
    ),
    aseg=dict(loc='mri',
    ),
    aseg_stats=dict(altkey='aseg',
    loc='stats',
    ),
    brain=dict(loc='mri',
    ),
    brainmask=dict(loc='mri',
    ),
    curv=dict(loc='surf',
    ),
    curv_stats=dict(altkey='curv',
    loc='stats',
    ),
    entorhinal_exvivo_stats=dict(altkey='entorhinal_exvivo',
    loc='stats',
    ),
    filled=dict(loc='mri',
    ),
    inflated=dict(loc='surf',
    ),
    label=dict(altkey='*label',
    loc='label',
    ),
    norm=dict(loc='mri',
    ),
    nu=dict(loc='mri',
    ),
    orig=dict(loc='mri',
    ),
    pial=dict(loc='surf',
    ),
    rawavg=dict(loc='mri',
    ),
    ribbon=dict(altkey='*ribbon',
    loc='mri',
    ),
    smoothwm=dict(loc='surf',
    ),
    sphere=dict(loc='surf',
    ),
    sphere_reg=dict(altkey='sphere.reg',
    loc='surf',
    ),
    subject_id=dict(),
    subjects_dir=dict(),
    sulc=dict(loc='surf',
    ),
    thickness=dict(loc='surf',
    ),
    volume=dict(loc='surf',
    ),
    white=dict(loc='surf',
    ),
    wm=dict(loc='mri',
    ),
    wmparc=dict(loc='mri',
    ),
    wmparc_stats=dict(altkey='wmparc',
    loc='stats',
    ),
    )
    outputs = ReconAll.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
