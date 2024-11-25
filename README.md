# nucleus-cl-access-tool



## Description
The access-test tool was created to help debug client connections or data upload failures to a Nucleus server. This tool uses the Omniverse Connect Samples SDK along with a Python script `access-tool` . This script is executed at a command line and will do the following:

1. Open a connection to a Nucleus server. Server can be FQDN or raw IP address for targeting. The user name and password are specified on the command line.

2. Once the connection is opened, all the files contained in the `usd-files` directory will be uploaded to the Nucleus server. There are two files currently in this repo directory (one is small and will not use LFT, the other is larger and thus will invoke LFT transport logic). The target location on the Nucleus server is also specified on the command line.

3. Close the connection


## Prereqs

### Clone this repo.
The following documetation is based on creating a directory called ***omniverse*** somewhere on the client **local** filesystem. The name of this directory is up to the user.

```
PS > cd C:\
PS > mkdir omniverse
PS > cd C:\omniverse
PS > git clone repo <...>
```


<details>
  <summary>Linux</summary>

```
$ cd ~
$ mkdir omniverse
$ cd omniverse
$ git clone repo <...>
```
</details>


### Install Omnivese Connect Samples
Download and build the Omniverse Connect Samples. Site to get Connect SDK https://github.com/NVIDIA-Omniverse/connect-samples/releases.
Use this site to get a pointer to the current archive

Place this download zip/tar.gz anywhere on the client **local** filesystem.
> Note: The SDK cannot be installed in a OneDrive location.

***Windows***
```
For this example:
PS > cd C:\omniverse\nucleus-cl-access-tool 
PS > wget https://github.com/NVIDIA-Omniverse/connect-samples/archive/refs/tags/v205.0.0.zip -OutFile connect-sdk.zip
PS > Expand-Archive .\connect-sdk.zip
PS > rm connect-sdk.zip
PS > cd connect-sdk\connect-samples-205.0.0
PS > ./build.bat
```

<details>
  <summary>Linux</summary>

```
$ wget https://github.com/NVIDIA-Omniverse/connect-samples/archive/refs/tags/v205.0.0.tar.gz  -O connect-sdk.tar.gz
$ mkdir -p connect-sdk && tar -xvf connect-sdk.tar.gz -C connect-sdk/
$ rm connect-sdk.tar.gz
$ cd connect-sdk/connect-samples-205.0.0/
$ ./build.sh
```
</details>


## Setup
Once the Omniverse Connect Samples has been downloaded and built, update the `access-test.bat` or `access-test.sh` to define the path to the root of the Omniverse Connect Samples. These scripts have comments to where to make the modifications. Following is snippet from `access-test.bat`

```
::
::  Change this line to point to the downloaded (and built)
::  Client library root dir. 
::
set CLIENT_LIB_SDK_DIR=C:\omniverse\nucleus-cl-access-tool\connect-sdk\connect-samples-205.0.0\
```

## Usage

```
PS > cd C:\omniverse\nucleus-cl-access-tool\access-test
PS > ./access-test.bat -h
Python 3.10.14
usage: access-test.py [-h] [-u USER_ID] [-p PASSWORD] [-v] [-d] nucleus nucleus_path

Python Client to copy data from a local file system to Nucleus Server

positional arguments:
  nucleus               example: ov-elysium.redshiftltd.net
  nucleus_path          Projects/SomeFolder (no leading '/')

options:
  -h, --help            show this help message and exit
  -u USER_ID, --user_id USER_ID
  -p PASSWORD, --password PASSWORD  (not needed if using API Key)
  -v, --verbose
  -d, --pre_delete_path
  -M, --Mode (0,1,2,3)
```
If the `-v` option is used, a verbose log of all steps will be output to the console. This output data can show error/warning information that the Nucleus team can use to help debug

If the `-d` option is used, the target direction on the Nucleus server is deleted prior to any upload operation. If the `-d` option is not set, then subsequent runs of the script will not upload any files if the hashes are the same.

### Example Upload files (-M 0)
Connect to Nucleus and do nothing but discaonnect

### Example Upload files (-M 1) (user/pass)
```
./access-test.bat -u omniverse -p 123456  -M 1 ov-elysium.redshiftltd.net Projects/test
Python 3.10.14
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://ov-elysium.redshiftltd.net
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTED
[access-test]: copy_file     : result: OK                   omniverse://ov-elysium.redshiftltd.net/Projects/test/nat-file-00.usd
[access-test]: copy_file     : result: OK                   omniverse://ov-elysium.redshiftltd.net/Projects/test/nat-file-01.usd
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.SIGNED_OUT
```

In the directory ```usd-files``` one can place any number of additional files (and sub directories with files) to test other upload permutations. Files can be of any size. Files need not be USD or USDC file, can be random data


### Example Upload files (-M 1) (API Key)
First get a valid Nucleus API key for the Nuclues server. Save this key in a file called ***api-token.txt*** in the ***access-test*** directory. Execute commands with the -u argument being '$omni-api-token', this will cause the script to read the ***api-token.txt*** to get the API key to log into the server.

> Note: Make sure you single quote the user argment exactly as shown below. 

This will work even if the Nuclues server is SSO/SSL enabled.

```
PS > .\access-test.bat -u '$omni-api-token'  -M 1 ov-elysium.redshiftltd.net Projects/test
Python 3.10.14
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://ov-elysium.redshiftltd.net
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTED
[access-test]: copy_file     : result: OK                   omniverse://ov-elysium.redshiftltd.net/Projects/test/nat-file-00.usd
[access-test]: copy_file     : result: OK                   omniverse://ov-elysium.redshiftltd.net/Projects/test/nat-file-01.usd
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.SIGNED_OUT
```
### Example Read File (-M 2)

```
PS > .\access-test.bat -u '$omni-api-token' -v -M 2 ov-elysium.redshiftltd.net Projects/somefile.usd
```

### Example List directory (-M 3)
This test will simply list the contents of a directory on Nucleus.

Following lists the root directory
```
PS > .\access-test.bat -u '$omni-api-token' -v -M 3 ov-elysium.redshiftltd.net "/"
Python 3.10.14
[access-test]: Omni Client initialized2.47.1-hotfix.5338+tc.ff2e947b
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTING
[access-test]: Authenticating to omniverse://ov-elysium.redshiftltd.net
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.CONNECTED
[access-test]: list dir : Library
[access-test]: list dir : NVIDIA
[access-test]: list dir : Projects
[access-test]: list dir : Users
[access-test]: Connection status to omniverse://ov-elysium.redshiftltd.net is ConnectionStatus.SIGNED_OUT
```

To list other directories do not include the "/". Example:
```
PS > .\access-test.bat -u '$omni-api-token' -M 3 -v ov-elysium.redshiftltd.net "Projects"
PS > .\access-test.bat -u '$omni-api-token' -M 3 -v ov-elysium.redshiftltd.net "NVIDIA/assets"
```

If the `-v` option is used, a verbose log of all steps will be output to the console. This output data can show error/warning information that the Nucleus team can use to help debug

## Support
TBD.


## Authors and acknowledgment
TBD.

## License
For open source projects, say how it is licensed.

