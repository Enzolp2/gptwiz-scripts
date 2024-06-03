Readme for TDM Setup from TDM2018 HF05  
In the past, many TDM customers were faced with the problem of finding an opportune time to apply 
an update.  
Previously, it was necessary to stop TDM and find a time when no TDM user was logged on to the 
system. Otherwise, access conflicts to the files in the TDM system folder (SYS directory) could occur 
during the installation, which ultimately led to the termin ation of the setup.  
As of version 2018 HF5, a version -specific subdirectory is created in the SYS directory for each setup. 
This avoids access conflicts between setup and logged in users. This change, however, makes it 
necessary to change the paths to the exe and ini files in order to point to the new subdirectory.  
After the first update with the changed setup, it is strongly recommended to run the TDM Client 
Installer once , on all client machines , to ensure that all clients access the current directory.  
 
TDM2018  
For TDM2018, both the SYS and the version -specific subdirectory are updated while the update is 
executed . So, if all clients are logged out during the update, all clients will work with the update  in 
the original SYS directory, even  if the  client in staller was not executed.  
With  TDM2018 , if a client was logged in during the execution of the setup, the clients will continue to 
work with the old hotfix (without the update) until the client installer has been run on the client 
computer . In this case the  following message appears during the execution of the setup:  
 
 
TDM2019  
As of TDM2019, the SYS directory is empty. Therefore, if an update from TDM2018 to TDM2019 is 
executed and the client installer was not executed, TDM cannot be started until the client installer 
has been executed.  
Version  Type of  
Installation  Client 
logged in  Client Installer 
required  Contents of the SYS directories  
 
TDM2018 
ab HF 05  New 
Installation  - 
 YES SYS directory is empty  
Updated subdirectory  
TDM2018 
ab HF 05  Update  YES YES SYS directory not updated  
Updated subdirectory  
TDM2018 
ab HF 05  Update  NO NO Updated SYS directory  
Updated subdirectory  
TDM2019  New 
Installation  - 
 YES SYS directory is empty  
Updated subdirectory  
TDM2019  Update  YES / NO YES SYS directory empty  
Subdirectory is current  
TNC client  
Customers with TNC clients do not need to run a client installer. The setup automatically inserts the 2 
new parameters "Start app" and "Start parameters" into the tmsStart.ini (see parameter in 
tmsStart.ini  below ). If there are any problems starting TDM after the setup, please check if they have 
the right content.  
 
Running the Client Setup  
All clients that have had the client setup run once, and thus have the correct start link, can continue 
to work while the setup is running, and will automatically work with the updated directory after 
rebooting TDM. For information, they  will receive the f ollowing message as soon as the setup is 
finished :  
 
“TMS -1151: Installation finished - please restart TDM ”. 
 
Structure of the Startlink  
The old start link was structured as follows:  
Path to the TDM start -exe - path to the  TDM server  filesystem - path to t he ini -file 
Ex .: 
C:\TDM2018 \SYS\tmsU.exe C: \TDM2018 C: \TDM2018 \SYS\tms.ini  
The new start link, on the other hand, contains the path to tmsStartU.exe (Unicode) or tmsStart.exe 
(non -Unicode), which was also already used for TNC clients. It is given as the p arameter the path to 
tmsStart.ini .:  
Ex .: 
C:\TDM2018 \SYS\tmsStartU.exe "TMS_INIFILE = C: \TDM2018 \Sys\tmsStart.ini"  
   
Parameters in the tmsStart.ini  
The tmsStart.ini contains the following parameters, which are processed by the tmsStartU.exe. These 
parameters contain the information that was previously stored directly in the start link.  
  
1. Path to the TDM Start -exe (previously in the start link)  
a. <SysLastVersion> : is replaced by tmsStartU.exe with the name of the SYS 
subdirectory . 
Structure of the subdirectory name using an example:  
Sys201801 0060093  
Präfix  TDM -Version Hotfix  Intern al Build Num ber 
At the end of the setup, the old subdirectory is renamed, and so the start path points 
to the updated subdirectory.  
 
b. X64 : By default, tmsStart.ini points to the 32 -bit directory of TDM.  
The x64 folder is not in the path:  
Start app:   TMS_STARTAPP=C: \TDM2018_Bamboo \Sys\<SysLastVersion> \ tmsU.exe  
 
If TDM is to be started in 64 -bit mode, the x64 folder must be inserted in tmsStart.ini 
(see above). If both a 32-bit and a 64 -bit version are required, a second tmsStart.ini 
(for example, tmsStart64.ini) can be created, which is then inserted in the start link 
of the client:  
C:\TDM2018 \SYS\tmsStartU.exe "TMS_INIFILE=C: \TDM2018 \Sys\tmsStart64.ini"  
 
c. tmsU.exe  or tms. exe: Start exe for TDM. Is automatically insert ed correctly into the 
path based on license information.  
All Unicode installations are started with the tmsU.exe. It is stored both in the 
current SYS (for 32 -bit) and in the SYS \ x64 folder (for 64 -bit). 
Non -Unicode installations are started either with the tms.exe in the current SYS 
directory (32 bit) or with the tmsU.exe in the SYS \ x64 folder (64 bit)  
 
2. Path to the TDM server filesystem folder  = TMS_HOME  
 
3. Path to the ini-file 
 
