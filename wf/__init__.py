"""
Analyze Chromatin ImmunopreciPitation sequencing (ChIP-seq) data.
"""

import imp
import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
import os


@small_task
def fastqc_task(input_dir: LatchDir, out_dir: LatchDir) -> LatchDir:

    # passing the files
    file_extensions = ['.fasta', '.fa', '.fastq',
                       '.fq', '.FASTA', '.FA', '.FASTQ', '.FQ', '.gz']
    input_files = [f for f in Path(
        input_dir).iterdir()if f.suffix in file_extensions]
    files = [f.as_posix() for f in input_files]

    # create the output directory
    os.mkdir(Path("fastqc_out"))

    # Writing the command
    _fastqc_rpt = [
        "fastqc",
        *files,
        "--outdir",
        str("fastqc_out"),

    ]

    subprocess.run(_fastqc_rpt, check=True)

    return LatchDir(str("fastqc"), out_dir.remote_path)


"""metadata = LatchMetadata(
    display_name="latch+chipseq"
    documentation="https://github.com/GeOdette/latch_chipseq.git/README.md",
    author=LatchAuthor(
        name="GeOdette",
        email="steveodettegeorge@gmail.com",
        github="https://github.com/GeOdette",
    ),
    repository="https://github.com/GeOdette/latch_chipseq.git",
    license="MIT",
)
"""


@workflow
def latch_chipseq(input_dir: LatchDir, out_dir: LatchDir) -> LatchDir:
    """The latch_chipseq is a pipeline for Chromatin ImmunopreciPitation sequencing (ChIP-seq) data. 

    _latch_chipseq_
    ----

    __metadata__:
        display_name: Analyze Chromatin ImmunopreciPitation sequencing (ChIP-seq) data. 

        author:
            name: Geodette

            email: steveodettegeorge@gmail.com

            github:
        repository: https://github.com/GeOdette/latch_chipseq.git

        license:
            id: MIT

    Args:

        input_dir:
          Input directory containing FASTQ files

          __metadata__:
            display_name: Input directory containing FASTQ files

        out_dir:
          Output directory containing analyzed files

          __metadata__:
            display_name: Output directory 
    """

    return fastqc_task(input_dir=input_dir, out_dir=out_dir)
