# Must be run on Alma9 server (i.e. not CentOS)

#!/bin/tcsh

(root -l -b -q runDSelectorINTERACTIVE.cc > runDSelectorINTERACTIVE_proof_THROWN.txt) >& runDSelectorINTERACTIVE_proof_error_THROWN.txt

# 7/3/2024 there may be a CCDB error causing a crash.  Try sourcing 'gxenv' in a different environment.
# $ gxenv /group/halld/www/halldweb/html/halld_versions/version_5.17.0.xml
# $ then run the script again -->
# $ source runDSelectorINTERACTIVE.csh
# $ If that doesn't work step back one-by-one through versions preceeding *_5.17.0.xml, running the runDSelectorINTERACTIVE.csh script each time until you find an .xml file that works.
