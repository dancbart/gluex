#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 4
#SBATCH -t 0-02:10:00
#SBATCH --requeue
#SBATCH --account=halld          # https://scicomp.jlab.org/scicomp/slurmJob/slurmAccount
#SBATCH --partition=production        # https://scicomp.jlab.org/scicomp/slurmJob/slurmInfo
#SBATCH --mem=2000
#SBATCH -o LOGOUT
#SBATCH -e LOGERR

######################################################## CHECK DIRECTORIES ######################################################

Setup_Script()
{       
        # PWD, STATUS OF MOUNTED DISKS
        cd /scratch/slurm/${SLURM_JOB_ID}
	echo "pwd =" $PWD
        if [[ $PWD != /scratch/slurm/${SLURM_JOB_ID} ]] ; then
            echo "LOCAL DIRECTORY " $PWD " NOT SUPPORTED"
            exit 1
        fi
        echo "df -h:"
        df -h


}

####################################################### SAVE OUTPUT FILES #######################################################

Save_OutputFiles()
{
        # SEE WHAT FILES ARE PRESENT
        echo "FILES PRESENT PRIOR TO SAVE:"
        ls -l

        # REMOVE INPUT FILE: so that it's easier to determine which remaining files are skims
        # BUILD TAPEDIR, IF $OUTDIR_LARGE STARTS WITH "/cache/"
        # AND CACHE_PIN_DAYS WAS GIVEN AND GREATER THAN 0
        # If so, output files are pinned & jcache put.  If not, then they aren't. 
        local TAPEDIR=""
        local OUTDIR_LARGE_BASE=`echo OUTDIRECT | awk '{print substr($0,1,7)}'`
        # first strip /cache/, then insert /mss/
        if [ "$OUTDIR_LARGE_BASE" == "/cache/" ] && [ 1 -gt 0 ] ; then
                local OUTPATH=`echo OUTDIRECT | awk '{print substr($0,8)}'`
                TAPEDIR=/mss/${OUTPATH}/
        fi

        # CALL SAVE FUNCTIONS
        Save_Histograms
        Save_Histograms
        Save_ROOTFiles
        Save_ROOTFiles

        # SEE WHAT FILES ARE LEFT
        echo "FILES REMAINING AFTER SAVING:"
        ls -l
}

Save_Histograms()
{
        # SAVE ROOT HISTOGRAMS
        if [ -e hd_root.root ]; then
                echo "Saving histogram file"

                # setup output dirs
                local OUTDIR_THIS=OUTDIRECT/hists/RUNNUMBER/
                mkdir -p -m 755 ${OUTDIR_THIS}

                # save it
                local OUTPUT_FILE=${OUTDIR_THIS}/hd_root_RUNNUMBER_FILENUMBER.root
                mv -v hd_root.root $OUTPUT_FILE
                chmod 644 $OUTPUT_FILE

                # check if the target file is empty, if yes try again
                if [ ! -s $OUTPUT_FILE ] ; then
                    mv -v hd_root.root $OUTPUT_FILE
                    chmod 644 $OUTPUT_FILE
                fi

                # if the target file is still empty, fail job
                if [ ! -s $OUTPUT_FILE ] ; then
                    exit 13
                fi

                # force save to tape & pin
                if [ "$TAPEDIR" != "" ]; then
                        echo jcache pin $OUTPUT_FILE -D $CACHE_PIN_DAYS
                        jcache pin $OUTPUT_FILE -D $CACHE_PIN_DAYS
                        echo jcache put $OUTPUT_FILE
                        jcache put $OUTPUT_FILE
                fi
        fi
}


Save_REST()
{       
        # SAVE REST FILE
        if [ -e dana_rest.hddm ]; then
                echo "Saving REST file"
                
                # setup output dirs
                local OUTDIR_THIS=OUTDIRECT/REST/RUNNUMBER
                mkdir -p -m 755 $OUTDIR_THIS
                
                # save it
                local OUTPUT_FILE=${OUTDIR_THIS}/dana_rest_RUNNUMBER_FILENUMBER.hddm
                mv -v dana_rest.hddm $OUTPUT_FILE
                chmod 644 $OUTPUT_FILE
                
                # check if the target file is empty, if yes try again
                if [ ! -s $OUTPUT_FILE ] ; then 
                    mv -v dana_rest $OUTPUT_FILE
                    chmod 644 $OUTPUT_FILE
                fi
                
                # if the target file is still empty, fail job
                if [ ! -s $OUTPUT_FILE ] ; then
                    exit 13
                fi
                
                # force save to tape & pin
                if [ "$TAPEDIR" != "" ]; then
                        echo jcache pin $OUTPUT_FILE -D $CACHE_PIN_DAYS
                        jcache pin $OUTPUT_FILE -D $CACHE_PIN_DAYS
                        echo jcache put $OUTPUT_FILE
                        jcache put $OUTPUT_FILE
                fi
        fi
}


Save_ROOTFiles()
{       
        # SAVE OTHER ROOT FILES
        local NUM_FILES=`ls *.root 2>/dev/null | wc -l`
        if [ $NUM_FILES -eq 0 ] ; then
                echo "No additional ROOT files produced"
                return
        fi
        
        echo "Saving other ROOT files"
        for ROOT_FILE in `ls *.root`; do
                
                # setup output dir
                local OUTDIR_THIS=OUTDIRECT/Tree/RUNNUMBER
                mkdir -p -m 755 $OUTDIR_THIS
                
                # save it
                local OUTPUT_FILE=${OUTDIR_THIS}/DSelector_RUNNUMBER_FILENUMBER.root
                mv -v $ROOT_FILE $OUTPUT_FILE
                chmod 644 $OUTPUT_FILE
                
                # check if the target file is empty, if yes try again
                if [ ! -s $OUTPUT_FILE ] ; then 
                    mv -v $ROOT_FILE $OUTPUT_FILE
                    chmod 644 $OUTPUT_FILE
                fi
                
                # if the target file is still empty, fail job
                if [ ! -s $OUTPUT_FILE ] ; then
                    exit 13
                fi
                
                # force save to tape & pin
                if [ "$TAPEDIR" != "" ]; then
                        jcache pin $OUTPUT_FILE -D $CACHE_PIN_DAYS
                        jcache put $OUTPUT_FILE
                fi
        done
}


########################################################## MAIN FUNCTION ########################################################

Run_Script()
{
	Setup_Script

	source /w/halld-scshelf2101/home/ksaldan/fcal_timing/setupGlueX_environment.sh

        # RUN JANA
	root -b -q $ROOT_ANALYSIS_HOME/scripts/Load_DSelector.C ROOTSCRIPT'("INPUTFILE", "TREENAME", "SELECTORFILE.C+", 4)'

        # RETURN CODE
        RETURN_CODE=$?
        echo "Return Code = " $RETURN_CODE
        if [ $RETURN_CODE -ne 0 ]; then
                exit $RETURN_CODE
        fi

        Save_OutputFiles
}

######################################################### EXECUTE SCRIPT ########################################################

Run_Script


