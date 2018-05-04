#!/usr/bin/expect
set timeout 3
set ip [lindex $argv 0]
set un [lindex $argv 1]
set pw [lindex $argv 2]
spawn ssh $un@$ip
expect {
    "Connection refused" exit
    "Name or service not known" exit
    "continue connecting" {send "yes\r";exp_continue}
    "password:" {send "$pw\r"};
    "Last login" {send " ifconfig |grep eth0 -A3\r\n";send "exit\r\n"}
}
expect eof
exit
#interact


