# gaen-pairwise-1m

Data from pairwise handset tests of the GAEN API.

The early-mid June runs (before Google's June 13 recalibration) 
are in [early-mid-june](early-mid-june/). The later runs are
in [late-june](late-june/).

These data were generated as part of the [TACT project](https://down.dsg.cs.tcd.ie/tact/).

## Instructions for replication

Some other SFI researchers are going to try replicate some
of these tests as a way of familiarising themselves with the
test setup (and to see if things have changed).

The typical test setup here is:

- Find a space to use: the specific place you do tests
can affect results, so make sure to find a place you 
can re-use for all related tests. Somewhere quiet is
good as it's annoying for a 40 minute run to have to
be repeated if someone walked between handsets.
- Get two non-metallic stands for handsets that you
can re-use for many tests.
- Pick two handsets, tx and rx.
- Ensure developer-settings/logger buffer sizes is 16MB 
  (or more if you there's a bigger Max)
- For rx:
    - Ensure the modified Google Examplar app is installed and up to
      date (re-installing from a known build via adb
      is a good way to ensure this if you've not used
      this handset in a while)
    - Ensure the EN service is running. Viewing the 
      QR codes for the keys and ensuring there is one
      for today is a good idea.
    - Ensure GAENAdvertiser is not running.
- For tx:
    - Ensure the GAENAdvertiser is installed and up to
      date (re-installing from a known build via adb
      is a good way to ensure this if you've not used
      this handset in a while)
    - Turn off the EN service.
    - Ensure no EN service app is running.
    - Ensure the GAENAdvertiser is running
- Place the handsets on the stands 1m apart, measuring the 1m from top
  to top, oriented face-up, with the tops of the
  handsets facing one another (obviously: always try make
  the physical setup as close to the same as possible)
- I always put tx on the same stand.
- On tx, hitting buttons with phone on stand without moving phone:
    - Generate a new TEK
    - Start generating RPIs
- Create a directory for this test, let's say called ``tx_to_rx``
  (for the relevant names of tx and rx)
- Create a notes file with the time the test started and the 
  details of tx,rx, including esp. the 
  EN service version and GPS version - usually called ``run.md``
  in this repo.
- Allow test to run for 40 minutes or more
  (more is fine, 40 is to ensure >30)
- Stop sending RPIs on tx
- Note test run end time
- Connect tx to computer via USB
    - Extract logcat data using the [grab-trace-data.sh](./grab-trace-data.sh)
      script
- Connect rx to computer via USB
    - Extract logcat data using the [grab-trace-data.sh](./grab-trace-data.sh)
      script
- For a device named foo that'll produce:
    - foo.log - the raw logcat data
    - foo.csv - a CSV file with received beacons (should be empty for tx)
    - foo-blead.csv - a CSV file with TEKs and beacons tx'd (should be missing/empty for rx) 
      (I usually renamed those to foo.blead, you don't need to:-)
- Edit correct TEK and epoch into python script
    - See [here](./late-june/sf_runtest1.py), the changes should be clear
    - The TEK and epoch value are in the blead file, you pick a test-string to
      include that distinguishes your test.
- To check the API outputs, now run the python script (with rx attached
  via USB). 
    - To get nicer output (with test-string  ``tx_to_rx``) I use sed, e.g.:

            $ ../sf_runtest1.py | sed -e 's/tx_to_rx/\ntx_to_rx/g' >tx_to_rx
