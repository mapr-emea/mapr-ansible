#!/bin/bash

find_unused_disks() {
   [[ -n "$DBG" ]] && set -x
   disklist=""
   fdisks=$(fdisk -l |& awk '/^Disk .* bytes/{print $2}' |sort)
   for d in $fdisks; do
      [[ -n "$DBG" ]] && echo Fdisk list loop, Checking Device: $dev
      dev=${d%:} # Strip colon off the dev path string
      # If mounted, skip device
      mount | grep -q -w -e $dev -e ${dev}1 -e ${dev}2 && continue
      # If swap partition, skip device
      swapon -s | grep -q -w $dev && continue
      # If physical volume is part of LVM, skip device
      type pvdisplay &> /dev/null && pvdisplay $dev &> /dev/null && continue
      # If device name appears to be LVM swap device, skip device
      [[ $dev == *swap* ]] && continue
      # Looks like might be swap device
      lsblk -nl $(readlink -f $dev) | grep -i swap && continue
      # If device is part of encrypted partition, skip device
      type cryptsetup >& /dev/null && cryptsetup isLuks $dev && continue
      if [[ $dev == /dev/md* ]]; then
         mdisks+="$(mdadm -D $dev |grep -o '/dev/[^0-9 ]*' |grep -v /dev/md) "
         continue
      fi
      if [[ "$testtype" != "readtest" ]]; then
         #Looks like part of MapR disk set already
         grep $dev /opt/mapr/conf/disktab &>/dev/null && continue
         #Looks like something has device open
         lsof $dev && continue
      fi
      ## Survived all filters, add device to the list of unused disks!!
      disklist="$disklist $dev "
   done

   for d in $mdisks; do #Remove devices used by /dev/md*
#      echo Removing MDisk from list: $d
      disklist=${disklist/$d }
   done

   #Remove devices used by LVM or mounted partitions
   [[ -n "$DBG" ]] && echo LVM checks
   awkcmd='$2=="lvm" {print "/dev/"$3; print "/dev/mapper/"$1}; '
   awkcmd+=' $2=="part" {print "/dev/"$3; print "/dev/"$1}'
   lvmdisks=$(lsblk -ln -o NAME,TYPE,PKNAME,MOUNTPOINT |awk "$awkcmd" |sort -u)
   for d in $lvmdisks; do
#      echo Removing LVM disk from list: $d
      disklist=${disklist/$d }
   done

   # Remove /dev/mapper duplicates from $disklist
   for i in $disklist; do
      [[ "$i" != /dev/mapper* ]] && continue
      [[ -n "$DBG" ]] && echo Disk is mapper: $i
      #/dev/mapper underlying device
      dupdev=$(lsblk | grep -B2 $(basename $i) |awk '/disk/{print "/dev/"$1}')
      #strip underlying device used by mapper from disklist
      disklist=${disklist/$dupdev }
      #disklist=${disklist/$i } #strip mapper device
   done

   # Remove /dev/secvm/dev duplicates from $disklist (Vormetric)
   for i in $disklist; do
      [[ "$i" != /dev/secvm/dev/* ]] && continue
      [[ -n "$DBG" ]] && echo Disk is Vormetric: $i
      #/dev/secvm/dev underlying device
      dupdev=$(lsblk | grep -B2 $(basename $i) |awk '/disk/{print "/dev/"$1}')
      #strip underlying device used by secvm(Vormetric) from disklist
      disklist=${disklist/$dupdev }
      #disklist=${disklist/$i } #strip secvm(Vormetric) device
   done
   [[ -n "$DBG" ]] && { set +x; echo DiskList: $disklist; }
   [[ -n "$DBG" ]] && read -p "Press enter to continue or ctrl-c to abort"
   echo $disklist | tr " " "\n" > /tmp/disks.txt
}

find_unused_disks
