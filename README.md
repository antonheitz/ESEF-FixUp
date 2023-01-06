# ESEF-FixUp

This toolkit lets you fix common issues for ESEF iXBRL filings with the click on a Button!

## Table of Contents

1. Deployment
2. Usage

## Deployment

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

## Usage

DESCRIBE API