Οδηγίες εκτέλεσης assignment2.py & assignment2_2.py
Απαραίτητη προϋπόθεση εκτέλεσης των παραπάνω αποτελεί η τοποθέτηση του αρχείου meddata2022.csv μέσα σε φάκελο με όνομα input εντός του hdfs.
Το path δηλαδή πρέπει να είναι το εξής:
hdfs://master:9000/user/user/input/meddata2022.csv

Αφού βρεθούμε εντός του φακέλου που βρίσκονται τα αρχεία κώδικα:
Για το assignment2.py εκτελούμε ως εξής:
~/spark/bin/spark-submit --master spark://master:7077 assignment2.py
Η αλλιώς:
 ~/spark/bin/spark-submit --master spark://master:7077 assignment2.py > something.txt
Εάν θέλουμε η έξοδος να γραφτεί σε αρχείο.

Για το assignment2_2.py εκτελούμε ως εξής:
~/spark/bin/spark-submit --master spark://master:7077 ~/assignment2_2.py (number of clusters) (init. method)
π.χ για k-means||: ~/spark/bin/spark-submit --master spark://master:7077 assignment2_2.py 6 k-means  (Οι κάθετες προστίθενται εντός κώδικα)
π.χ για random:~/spark/bin/spark-submit --master spark://master:7077 assignment2_2.py 6 random
Εαν θέλουμε έξοδο σε αρχείο π.χ: ~/spark/bin/spark-submit --master spark://master:7077 assignment2_2.py 6 k-means > something.txt

ΓΙΑ ΕΚΤΕΛΕΣΗ ΜΕ 1 SLAVE,ΣΤΟΝ WORKER ΠΟΥ ΘΑ ΣΤΑΜΑΤΗΣΕΙ ΠΡΟΗΓΕΙΤΑΙ ΠΡΙΝ ΤΑ ΠΑΡΑΠΑΝΩ Η ΕΝΤΟΛΗ:
~/spark/sbin/stop-slave.sh