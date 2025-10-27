# Getting everyone on the instance

### Two paths

There are two paths forward here: one where `gcloud` and associated tools
manage everything in the Google-Cloud-specific-way, and one where we eschew all
the GC tool stuff and just do caveman SSH from the command line (like the way
everyone logs on to `cpsc.umw.edu`.

After the first path proved problematic, we're switching to the second way.

# Instructions for the "plain-ol-ssh" way

### 1. Owner (SD) does this one time:

`$ gcloud compute instances add-metadata frozone --zone=us-east4-c --metadata enable-oslogin=FALSE`

_This tells GCP: don’t rewrite or manage SSH keys; we'll handle them manually._

### 2. Stephen manually adds accounts and .ssh dirs for each other collaborator:

```
$ sudo useradd -m -s /bin/bash USERNAME
$ sudo mkdir -p /home/USERNAME/.ssh
$ sudo chmod 700 /home/USERNAME/.ssh
$ sudo chown -R USERNAME:USERNAME /home/USERNAME/.ssh
```
for all values of "`USERNAME`".


### 3. **Everybody else** does this on their machine:

```
$ ssh-keygen -t ed25519 -C "theirname@frozone"
$ cat ~/.ssh/id_ed25519.pub
```

where "`theirname`" is one of: `bethanie05`, `riderle`, `garrett`, or
`noahyfine`. (If you feel strongly that you'd like a different username on the
frozone server, lmk and I'll make that happen.) Then email me the resulting
`id_ed25519.pub` key file (you can paste its contents in the email if MS
Outlook doesn't let you attach it for some reason.)

### 4. Stephen manually appends their public key info into `authorized_keys`.

```
$ sudo bash -c 'echo "ssh-ed25519 AAAA... user@host" >> /home/USERNAME/.ssh/authorized_keys'
$ sudo chown USERNAME:USERNAME /home/USERNAME/.ssh/authorized_keys
$ sudo chmod 600 /home/USERNAME/.ssh/authorized_keys
```

### 5. Stephen gives sudo since we're all compatriots here:

```
$ sudo usermod -aG sudo USERNAME
```

### 6. Now **everyone else** should be able to ssh to the server with:

```
$ ssh -o IdentitiesOnly=yes -i ~/.ssh/yourPrivateKey USERNAME@34.48.61.114

```
