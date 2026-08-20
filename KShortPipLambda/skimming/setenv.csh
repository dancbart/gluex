# --- Hao halld_sim env (per-session) ---
setenv HALLD_SIM_HOME /work/halld/home/dbarton/gluex/KShortPipLambda/software/halld_sim

# Candidate build dirs (globbing)
set candidates = ( $HALLD_SIM_HOME/src/.Linux_* )
# If the glob didn't expand, there is no build
if ( "$candidates[1]" == "$HALLD_SIM_HOME/src/.Linux_*" ) then
    echo "No build found under $HALLD_SIM_HOME/src/.Linux_* — did you run scons?"
    goto done
endif

# Pick newest build dir; use \ls to bypass any 'ls' alias that adds -l
set builddir = `\ls -1dt $candidates | head -1`

# Create staging bin and symlink all executables from programs/*
set stagebin = "$builddir/bin"
if ( ! -d "$stagebin" ) mkdir -p "$stagebin"

# Symlink every executable (exclude .o files)
foreach f ( `find "$builddir/programs" -maxdepth 2 -type f -perm -u+x ! -name "*.o"` )
    ln -sf "$f" "$stagebin/`basename "$f"`"
end

# Add the staging bin to PATH once (use braces to avoid :-modifier parsing)
if ( $?PATH ) then
    echo ":$PATH:" | grep -Fq ":$stagebin:"
    if ( $status ) setenv PATH "${stagebin}:${PATH}"
else
    setenv PATH "${stagebin}"
endif

done:

