#!/usr/bin/env bash

sed "
6d;
40d;
44d;
58d;
77d;
79d;
82d;
87d;
106d;
107d;
121d;
181d;
187d;
188d;
223d;
230d;
232d;
244d;
269d;
270d;
289d;
292d;
336d;
348d;
370d;
411d;
417d;
421d;
430d;
444d;
454d;
468d;
469d;
476d;
489d;
491d;
494d;
522d;
525d;
539d;
548d;
558d;
568d;
588d;
591d;
596d;
600d;
604d;
647d;
664d;
669d;
674d;
693d;
706d;
707d;
736d;
768d;
777d;
784d;
789d;
820d;
827d;
846d;
880d;
885d;
901d;
912d;
933d;
936d;
951d;
973d;
1012d;
1066d;
1068d;
1069d;
1111d;
1148d;
1164d;
1170d;
1195d;
1199d;
1200d;
1230d;
1240d;
1247d;
1257d;
1290d;
1297d;
1324d;
1326d;
1341d;
1371d;
1372d;
1402d;
1408d;
1474d;
1497d;
" sampled_workload.sparql
