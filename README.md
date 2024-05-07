# Pulumi python: aws ec2 + docker

Script to create an aws ec2 with docker.

## Requirements

1. Install pulumi: `https://www.pulumi.com/docs/install/`
2. Login: `$ pulumi login` for remote state or `$ pulumi login --local` to local state (no pulumi account)
3. Up: `$ pulumi up`
4. Destroy: `$ pulumi destroy`

## Custom shell script

Update the file `myshellscript.py` and add your custom scripts in it. This file is also in `.gitignore` so it won't be commited to repo.

This file will run in the ec2 bootstrap script: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html

Run `python test.py` to evaluate the results.