# ESEF-FixUp

This toolkit lets you fix common issues for ESEF iXBRL filings with the click on a Button!

## Table of Contents

1. [Currently implemented fixes](#currently-implemented-fixes)
2. [Use via CLI](#use-via-cli)
    1. [CLI Deployment](#cli-deployment)
    2. [CLI Usage](#cli-usage)
3. [Use via REST API via Docker](#use-via-rest-api)
    1. [Docker Deployment](#docker-deployment)
    2. [REST API Usage](#docker-usage)

## Currently implemented fixes:

TBD

## Use via CLI

### CLI Deployment

Make sure you have python 3 installed.

Install the dependencies:

```bash
pip3 install -r packages/worker/requirements.txt
```

### CLI Usage

TBD

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