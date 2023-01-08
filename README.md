# ESEF-FixUp

This toolkit lets you fix common issues for ESEF iXBRL filings with the click on a Button!

## Table of Contents

1. [Implemented ESEF Fixes and Upcomming Stuff](#implemented-esef-fixes-and-upcomming-stuff)
2. [Use via CLI](#use-via-cli)
    1. [CLI Deployment](#cli-deployment)
    2. [CLI Usage](#cli-usage)
3. [Use via REST API via Docker](#use-via-rest-api)
    1. [Docker Deployment](#docker-deployment)
    2. [REST API Usage](#docker-usage)

## Implemented ESEF Fixes and Upcomming Stuff:

1. Inline CSS

Inline CSS can be a hazard for ESEF Block tagging, since the styles are taken into the tagged data when the `escape` atrribute was set to `true` for a tag. This can result in misleading representation of the data, since CSS styles can be interpreted differently in different engines and with a lack of specification of which engine to use by the regulator. This fixup removes the inline-css and adds them back in in a optmized set of classes, resulting in "clean" tag contents when rerenderd by any engine, only based on the "sematic" html structure of the data.

2. (Upcomming) External link removal
3. (Upcomming) Optimize Data-URL Placements for ESEF Block Tags

## Use via CLI

### CLI Deployment

Make sure you have python 3 installed.

Install the dependencies:

```bash
pip3 install -r packages/worker/requirements.txt
```

### CLI Usage

All you need to do is to use the `cli.sh` script and pass two arguments:

```bash
./cli.sh "<input zip path>" "<output zip path>"
```

## Use via REST API

### Docker Deployment

To deploy the service you will need docker and docker-compose installed on your system.

Start by cloning the repository:

```bash
git clone git@github.com:antonheitz/esef-fixup.git
cd esef-fixup
```

Build the containers:

```bash
./service.sh build
```

Start the containers:

```bash
./service.sh start
```

Stop the containers:

```bash
./service.sh stop
```

Delete the containers:

```bash
./service.sh cleanup
```

## Docker Usage

There are a few simple routes to use to interact:

Add a job (and upload a file). This will return the id of the job:

```bash
curl -X POST -F file=@</path/to/esef/file> localhost:3001/api/jobs/add
```

Check all Jobs and status:

```bash
curl localhost:3001/api/jobs/data
```

Start the Job you want to run:

```bash
curl -X POST localhost:3001/api/jobs/start/<job-id>
```

After the status is "DONE", you can download the output zip:

```bash
curl localhost:3001/api/files/final/<job-id>/<file-name> --output </path/to/ouput/filename>
```
