# Ansible Error Handling
## Scenario

We have to set up automation to pull down a data file, from a notoriously unreliable third-party system, for integration purposes. Create a playbook that attempts to download https://bit.ly/3dtJtR7 and save it as `transaction_list` to `localhost`. The playbook should gracefully handle the site being down by outputting the message "Site appears to be down. Try again later." to stdout. If the task succeeds, the playbook should write "File downloaded." to stdout. No matter if the playbook errors or not, it should always output "Attempt completed." to stdout.

If the report is collected, the playbook should write and edit the file to replace all occurrences of `#BLANKLINE` with a line break '\n'.

Task list: 

* Create a playbook, `/home/ansible/lab-error-handling/report.yml` that runs against `localhost`.
* Configure the playbook to use the `get_url` module to download https://bit.ly/3dtJtR7 to `/home/ansible/lab-error-handling/transaction_list` on `localhost` and output "File downloaded." to `stdout`.
* Configure the playbook to handle connection failure by outputting "Site appears to be down. Try again later." to `stdout`.
* Configure the playbook to output "Attempt Completed" to stdout, whether it was successful or not.
* Configure the playbook to replace all instances of `#BLANKLINE` with the line break character `\n`
* Run the playbook using the default inventory to verify whether things work or not.
* Configure ansible to run with escalated permissions.

After confirming the playbook successfully downloads and updates the `transaction_list` file, pull the latest changes from the repository, and run the `break_stuff.yml` playbook in the `maint` directory to simulate an unreachable host.

```
cd ~/ansible-best-practices && git pull
```

```
cd /home/ansible/lab-error-handlng
```


```sh
ansible-playbook maint/break_stuff.yml --tags service_down
```

Confirm the host is no longer reachable 
```sh
curl -L -o transaction_list https://bit.ly/3dtJtR7
```

Run the playbook again and confirm it gracefully handles the failure.

Restore the service using `break_stuff.yml`, and confirm the `report.yml` playbook reports the service is back online.

## Congrats!

