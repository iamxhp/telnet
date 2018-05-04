#!/bin/bash   
arr=("xhp" "xhp" "admin" "admin") #format：username password
num=${#arr[@]}
#echo $num
index=0
while read myline
do
	#echo "IP:"$myline
	while((index<$num))
	do
		#echo $index
		un=${arr[index]}
		pw=${arr[index+1]}
		let "index = index+2"
		echo "IP:"$myline" un:"$un" pw:"$pw
		./ssh.sh $myline $un $pw
		
	done
	let "index=0"
done < xhp.txt
