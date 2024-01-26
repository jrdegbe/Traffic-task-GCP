
## Adding a New Cron Job

1. Open Crontab for Editing:

- In the terminal, type crontab -e and press Enter. 
This command will open your user's crontab file in the default text editor for editing.

- Add the Cron Job:

In the crontab editor, add a new line at the bottom of the file for the cron job.

The format of the cron job should be:

0 6 * * * /Users/jrdegbe/Desktop/Derek_Interview_Qs/myenv/bin/python3 /Users/jrdegbe/Desktop/Derek_Interview_Qs/scripts/automate_pipeline.py


- After adding the line, save the crontab file and exit the editor. The method to save and exit depends on the text editor you are using. 

In many cases, it is done by pressing Ctrl + X, then Y (to confirm saving), and Enter.

- Verify the Cron Job:

To check that the new cron job is scheduled, type crontab -l in the terminal. 

You should now see the job you just added listed.


Ensure that the script is executable and has appropriate permissions. 

You might need to run chmod +x /Users/jrdegbe/Desktop/Derek_Interview_Qs/scripts/automate_pipeline.py to make it executable.

