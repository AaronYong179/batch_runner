# batch_run.py
This serves as a guide for using a very dirty script `batch_run.py` to run simple bash commands over multiple files.

---
## Setting up
1. Make sure Python v3.7 (and above) is installed
2. Make sure all files of interest are placed [within their own folders](#Directory-structure). This helps in auto-naming output files and is currently compulsory.
3. Make sure the `batch_run.py` script is placed within the [parent directory](#Directory-structure) containing all the files of interest.
4. Make sure the tool to be used (e.g., GATK, samtools) is already installed on the system.


## Quick Start
As an example, if you would want to run `samtools` depth command over all mapped alignment `.bam` files in the current directory, you would execute the following: 
```
python3 batch_run.py --command 'samtools depth "%(INPUT)" > "%(OUTPUT)"' --input-format="_mapped.bam" --output_format=".depth"
```

Another example: if you would want to run `samtools` index command over all alignment `.bam` files
```
python3 batch_run.py --command `samtools index "%(INPUT)"` --input_format=".bam"
```

## Things to take note of
### Directory structure

In order to run this script, the directory structure needs to mirror one shown below:
```
\Documents
    \ProjectAlpha
        \RUN001
            001.fastq
        \RUN002
            002.fastq
        \RUN003
            003.fastq
        batch_run.py
```
Three things to take note of:
* The `batch_run.py` script is placed in the minimum level directory that contains all files-of-interest. In this case, the files of interest would be `fastq` files and the minimum level would be the folder `ProjectAlpha`
* Each file-of-interest is **contained within a distinguishing subfolder** `RUNXXX`. This is to aid output auto-naming. In other words, output names will be automatically pulled from the distinct folder names (such as `RUN003.sam`).
* All directories and subdirectories are **consistent** in structure. All `fastq` files are placed one level within their own folders.

Here is another example of a "correct" directory structure:
```
\Documents
    \ProjectAlpha
        \RUN001
            \raw_fastq
                001.fastq
        \RUN002
            \raw_fastq
                002.fastq
        \RUN003
            \raw_fastq
                003.fastq
        batch_run.py
```

The same three criteria:
* `batch_run.py` is placed in the correct location
* Distinguishing folder names are found for each file of interest (`RUNXXX`)
* Directories and subdirectories are consistent. It does not matter how many levels deep the files of interest are, as long as the **consistency** criterion is fulfilled.


### --command
The basic idea is that all files with the format given under `--input_format` or `--output_format` will be filled into the provided command template.

For example, if the command template given is:
```
'samtools index "%(INPUT)"'
```
Then, all input files will be run using this command template:
```
$ samtools index align1.bam
$ samtools index align2.bam
$ samtools index align3.bam
.
.
.
```
> Basically, the weird "%(INPUT)" term tells the script the position to replace. 

If you're not too sure what to do, just use this sample command and mutate it appropriately:
```
'samtools depth "%(INPUT)" > "%(OUTPUT)"'
```

* Note that the `"%(INPUT)"` and `"%(OUTPUT)"` terms are character sensitive, so just copy-paste them around if you are not too sure what to do.
* Also note the enclosing single quotes (`''`)
* `"%(INPUT)"` is compulsory but `"%(OUTPUT)"` is optional

### --input_format
The file format of files to be used as inputs to the template command (e.g., `.sam`, `.fastq`, `.txt`).

Alternatively, one could specify the tail-end of filenames to provide an additional layer of filtering. For example, if you have two `.bam` files in your directory:
```
\Documents
    \ProjectAlpha
        \RUN001
            \alignments
                \001.bam
                \001_mapped.bam
```

Specifying `--input_format="_mapped.bam"` means that you only wish to run the command on files that end with `_mapped.bam`. File `001.bam` will then be ignored.

### --output_format
The file format of the output file. The main filename itself will be pulled from the [distinguishing folders](#Directory-structure), but you are free to append words to the output filename.

For example, running an alignment command on `--input_format=".fastq"` with `--output_format=".sam"` on the following would result in `RUN001.sam`.
```
\Documents
    \ProjectAlpha
        \RUN001
            \raw_fastq
                001.fastq
```

Running the same alignment command on `--input_format=".fastq"` with `--output_format="_aligned.sam"` on the following would result in `RUN001_aligned.sam`.


## Issues
Oh there will definitely be issues, I wrote this in one hour.
Complain to me irl or threaten to bleach my culture.