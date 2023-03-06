# Weekly Pay_Alert slack_bot using Python and AWS Services


## A pay notification bot for Slack using Lambda and AWS Services

This project uses a python script that has been integrated into AWS lambda. The script reads an excel spread sheet with punch in and punch out times-
recording days and hours worked. Using pandas this script is read into the script and prints the recent pay week. It does this by finding the current week. 
If it finds the current week it will print the current weeks hours worked, what week it is and the total pay for the hours worked. Additionally there is a try catch that will- determine if the current week has been worked or if it has not and will know to skip that week when searching for current week. Lastly there is a slack block where the information from the current week found is displayed in a slack block. There is a second event bridge set up that will continue alerting that this weeks pay is due until the user turns off the button labled payment complete turning off the second alarm

* Uses pandas to read an excel spreadsheet and take the current information from it
* Will skip weeks where not information is recorded
* Takes current dates information and displays it in a slack_block
* Using Lambdas to integrate the script into AWS services
* AWS Event Bridge was set up to run the script at specific time every week to notify payment needs to be made
* CD is set up using GitHub runners


