# PyWren on Azure 

** NOTE: Python on Azure has been deprecated and removed. As of October 2017, none of the code here works becuase any Python function automatically crashes and errors. **


## Deployment
Azure gives you two options to deploy a function: web portal or via HTTP Put
* Deploying with web portal isn't a great fit because we need to upload `jobrunner.py`, so the better option is to deploy with HTTP.
* HTTP PUT also makes it easier for us to set up file IO, which is very wonky in Azure.

The following files need to be zipped and PUT to the endpoint `https:{function_name}.scm.azurewebsites.net/api/zip/site/wwwroot`

* `function.json` this is the config file. 
* `jobrunner.py` This runs in a subprocess to unpickle the function, and puts the output in storage.
* `run.py` same as wrenhandler
* `pywren.version.py` Version.

## Invoking
In order to have asynchronous invocation, we use Queue Triggers. This works similar to PyWren on AWS. We pack all of our arguments into a dict, serialize it into a JSON string, and drop an arg string into the queue for each task we want to run. Under the hood, Azure will parse the json and do any processing or preparation necessary before your function starts. 
For example, if you want to use a file from storage `foo/*.pickle` in your function, and where `*` is some job id, then in the queue string, you could have something like

```
{
  'job_Id": 00000000.pickle
}
```
and in your `function.json` file, you could specify that you want the file at 

```
    {
      ...
      "path": "azure-webjobs-hosts/foo/{job_Id}", //Specify the path of the file in the cloud storage bucket.
      ...
    },
```
This is confusing as hell and not documented.


## Storage IO
This is where things get a bit hairy. Instead of Google Cloud or AWS, where the conanical way to access cloud storage is via a typical SDK (`boto3`, `@google-cloud/storage`), Azure expects you to declare the files you want to read and write when deploying. 

Here's how storage accesses work in Azure: 
* In `function.json`, specify any input and output `bindings` that you want to be able to access from the function. This is how I added the binding to write the output pickle. 

```
    {
      "type": "blob",                      //Read from blob storage
      "name": "outputfile",                //The filename will be availble at os.environ['outputfile']
      "path": "azure-webjobs-hosts/foo/{output_key}", //Specify the path of the file in the cloud storage bucket.
      "connection": "AzureWebJobsDashboard",    //Name of the blob storage bucket.
      "direction": "out"                     //This is an output binding/write
    },
```

At runtime, Azure will specify a file at path `os.environ[outputfile]`, and any bytes written to that path will be written to cloud storage at the end of the function.  

```
with open(os.environ[outputfile], 'wb') as f:
  f.write(output_Pickle)
```

**This means that random storage access isn't a typical access pattern w Azure.**

Technically, we _could_ support random storage IO if we update the conda runtime to have the Azure SDK. However, my understanding is that the Azure python SDK isn't very mature. For example, they have no mechanism to detect auth credentials from your environment the way Google and AWS do. Thus, users would have to upload their auth credentialswithin the data pickle in order to achieve random IO.

## Function.json
This is the config file. 

