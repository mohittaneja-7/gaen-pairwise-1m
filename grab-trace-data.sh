#
# Grab limited device and opentrace/EN data from a handset via ``adb logcat``
# and store those in a useful, privacy-friendly manner
#
# set -x

# Copyright (C) 2020 Stephen Farrell
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

function whenisitagain()
{
	date -u +%Y%m%d-%H%M%S
}
NOW=$(whenisitagain)

# TODO: check commands we need are present - since we're asking others to do
# this we should be nice

# any sensitive identifiers will be run through HMAC-SHA256 before being
# stored, each run of this script will generate a new key for that, so
# results can't be correlated so easily 
# TODO: consider making that a daily key instead so that running this
# twice on same machine, same day can accumulate results, if we want 
# that
hmackey=`head -c 32 /dev/urandom | base64`
#echo "Hmac key is $hmackey"

# if the log has opentrace type entries
OTTYPE="OPENTRACE"
# if the log has google EN type entries
ENTYPE="ENAPI"

# default to google/apple API
APPTYPE=$ENTYPE

# if a log file is given on the command line use that
# rather than re-run adb logcat
LOGSUPPLIED=""

# if CLEAN is "yes" then we'll delete matching old log and csv
# files 
CLEAN="no"

function usage()
{
	echo "$0 [-o|-e] [-l <logcat-file>]"
    echo "Extract RSSI info in \"TACT\" format from a logcat log"
    echo "	-e means assume log has Exposure-Notification type log entries (default)"
	echo "	-o means assume log has OpentTrace type log entries"
	echo "	-l means read from file-name supplied rather than use adb logcat"
	echo "	-c means clean out any old logs or CSVs from this directory"
	exit 99
}

# options may be followed by one colon to indicate they have a required argument
if ! options=$(getopt -s bash -o oel:hc -l opentrace,enapi,log:,help,clean -- "$@")
then
	# something went wrong, getopt will put out an error message for us
	exit 1
fi
#echo "|$options|"
eval set -- "$options"
while [ $# -gt 0 ]
do
	case "$1" in
		-h|--help) usage;;
		-e|--enapi) APPTYPE="$ENTYPE";;
		-o|--opentrace) APPTYPE="$OTTYPE";;
		-l|--log) LOGSUPPLIED="$2"; shift;;
		-c|--clean) CLEAN="yes"; shift;;
		(--) shift; break;;
		(-*) echo "$0: error - unrecognized option $1" 1>&2; exit 1;;
		(*)  break;;
	esac
	shift
done

if [[ "$LOGSUPPLIED" == "" ]]
then
    devname=`adb devices -l | grep 'device ' | sed -e 's/  .*//'`
    if [[ "$devname" == "" ]]
    then
        echo "No devices attached - exiting"
        exit 0
    fi
else
    devname=`basename $LOGSUPPLIED .log`
fi

# The case-insensitive names of the devices we know...
PETS="KittyMooney Jersey" 
PLANETS="Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto"
KNOWN_DEVICES="$PETS $PLANETS"

for dev in $devname
do
    lfname=$LOGSUPPLIED
    if [[ "$LOGSUPPLIED" == "" ]]
    then
        # try a couple of options for naming
        dname=`adb -s $dev shell settings get global device_name`
        udname=`adb -s $dev shell settings get global unified_device_name`
        for known in $KNOWN_DEVICES
        do
            if [[ "$dname" == "$known" ]]
            then
                continue
            elif [[ "$udname" == "$known" ]]
            then
                dname=$udname
            fi
        done
        ble_dets=`adb -s $dev shell getprop vendor.bluetooth_fw_ver`
        model=`adb -s $dev shell getprop ro.product.model`
        echo "$dev is known as $dname is a $model with a $ble_dets"
        echo "Grabbing data from $dname"
        if [[ "$CLEAN" == "yes" ]]
        then
            echo "Cleaning old files..."
            rm -f $dev-*.log $dev-*.csv
        fi
        adb -s $dev logcat -d -v year -b all >$dev-$NOW.log
        lfname=$dev-$NOW.log
    fi
    if [[ "$APPTYPE" == "$OTTYPE" ]]
    then
        cat $lfname | grep -A2 rssi | paste - - - - -d, | grep BtGatt | grep "NOT-IDLE Scanned" \
            | awk '{print $1" "$2"," $18 $17 ",'$dev'," $38","$27}' | sed -e 's/txPower=//' | sed -e 's/rssi=//' > $dev-$NOW.csv
    elif [[ "$APPTYPE" == "$ENTYPE" ]]
    then
        # logcat as written by google/apple sample API
        cat $lfname | grep calibrated_rssi \
            | awk '{print $1" "$2"," $12 "1," $13"dev," $9 $11}' \
            | sed -e 's/raw_rssi=//' \
            | sed -e 's/calibrated_rssi=//' \
            | sed -e 's/id=//' \
            | sed -e 's/,$//' \
                     > $dev-$NOW.csv
        # logcat entries from BLEAdvertiser, only keep 'em if we have 'em
        bleadcount=`grep -c TEK,RPI, $lfname`
        if [[ "$bleadcount" != "0" ]]
        then
            cat $lfname | grep "TEK,RPI," \
                | awk '{print $1" "$2","$9}' \
                    >$dev-$NOW-blead.csv
        fi
    else
        usage
    fi
done

