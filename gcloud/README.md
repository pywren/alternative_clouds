# PyWren on google cloud functions

## Getting started

Set up your (google cloud account)[https://developers.google.com/identity/protocols/application-default-credentials], and make sure that the environment variable `GOOGLE_APPLICATION_CREDENTIALS` points to your auth credentials

Follow the steps on (this page)[https://cloud.google.com/functions/docs/quickstart]. These will help you set up the gcloud SDK and enable the Google Cloud Functions API. The important steps are: 

1. Set up a Google Cloud project and enable billing for storage and Google Cloud Functions. Note the `projectID`.

2. Enable the Google Cloud Functions API

3. Make sure you have the `gsutil` and `gcloud` command line utilities.
    Instructions on setting up the `gcloud` environment on your machine are (here)[https://cloud.google.com/sdk/docs/]

4. run `gcloud components update && gcloud components install beta`

5. run `pip install --upgrade google-cloud-storage`


## Setting up buckets
Set up our storage bucket. On the command line, run

```
gsutil mb -p <projectID> gs://bucket_name
```

## Deployment

### set-up
A google cloud function is deployed as a node module. Set up a directory for eveyrthing to be staged.
** Important: do not start a git repo in the same directory as your function code. The deploy command zips up everything in the current folder, and including `.git` takes up  unnecessary space`

```
mkdir pywren_gcf
mv package.json pywren_gcf
mv index.js pywren_gcf
cd pywren_gcf
```

`package.json` specifies function metadata, including dependencies. These include utilities for interacting with the file system, and google cloud storage. To install, run

```
npm install
```

### `index.js`
The function handler is in `index.js`. In  `index.json`, there is a line that looks like
```
exports.handler = function(req, res) {}
```

`handler` is the name of deployed function. Notice that `function(req, res)` basically has Express.js handles. `req` has the POST request body, and `res` is the HTTP response.

### Deploying
On the command line, run 
```
gcloud beta functions deploy handler --stage-bucket bucket_name --trigger-http --memory 2048 --timeout 540 
```

## Invoking
Invoke with HTTP POST request.

The request looks something like

```
curl -X POST https://<REGION>-<projectID>.cloudfunctions.net/handler -H "Content-Type:application/json" --data '<data payload>'
```
where `<REGION>` is `us-central1`, because that's the only available deployment region.
