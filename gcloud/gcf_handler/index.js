/*Bacckground Cloud Function to be triggered by Cloud Storage.
 *
 * @param {object} event The Cloud Functions event.
 * @param {function} The callback function.
 */
const spawn = require('child-process-promise').spawn;
const Storage = require('@google-cloud/storage');
const fs = require("fs");


function download_runtime_if_necessary(req) {
  /**
   * Check if file exists.
   */
  const dest = "/tmp/";
  const runtime_loc = req.body.runtime.google_bucket;
  const runtimeName = req.body.runtime.google_key;
  const storage = Storage();
  const runtime_bucket = storage.bucket(runtime_loc);
  const runtime = runtime_bucket.file(runtimeName);

  download_runtime = true;
  try {
    // Node.js doesn't come with a good way to check if a given file exists
    // so only thing we can do is run .stat, and see if it crashes.
    existence = fs.statSync(dest+runtimeName);
    console.log("Container being reused");
    download_runtime = false;
  } catch(err) {
    console.log("fresh container");
    download_runtime = true;
  }

  options = {
    destination: dest + runtimeName 
  };
  if (!download_runtime) {
    console.log("not downloading");
    try {
        //If this exists, this means that there is another thread running in the container.
        existence = fs.statSync("/tmp/status");
    } catch(err) {
        console.log("CONCURRENT THREADS WTF");
    }
    return Promise.resolve(true);
  } else {
    return runtime.download(options);
  }
}

exports.handler = function wrenhandler (req, res) {

  response = {"exception": null};
  const callset_id = req.body.callset_id;
  const call_id = req.body.call_id;
  console.log("STARTING " + callset_id + "-" + call_id); 

  const conda_path = "/tmp/condaruntime/bin";

  const func_filename = "/tmp/func.pickle";
  const data_filename = "/tmp/data.pickle";
  const output_filename = "/tmp/output.pickle";

  const dest = "/tmp/";
  console.log(req.body.callset_id);
  response['func_key'] = req.body.func_key;
  response['data_key'] = req.body.data_key;
  response['output_key'] = req.body.output_key;
  response['status_key'] = req.body.status_key;

  const storage_bucket = storage.bucket(req.body.storage_info.location);
  response["start_time"] = new Date().getTime()/1000;
  download_runtime_if_necessary(req)
    .then((err) => {
       console.log("downloading");
      // tar without attempting to chown, because we can't chown.
      var TAR = spawn("tar",  ["--no-same-owner", "-xzf", "/tmp/" + runtimeName, "-C", "/tmp"]);
      var childProcess = TAR.childProcess;

      TAR.then((err) => {
        const func = storage_bucket.file(req.body.func_key);
        options = {
          destination : func_filename
        }
        return func.download(options)
      })
      .catch(function(error) {
        console.error('ERROR w func download ', error);
        res.send("fail");
      })
      .then((err) => {
        console.log("we downloaded the function");
        const data = storage_bucket.file(req.body.data_key);
        if (req.body.data_byte_range == null) {
            options = {};
        } else {
            options = {
                'start' : req.body.data_byte_range[0],
                'end' : req.body.data_byte_range[1]
            };
        }
        data.createReadStream(
          options
        ).on('error', function(err) {console.log(err);})
          .pipe(fs.createWriteStream(data_filename));
        
        var attempt_python = spawn(conda_path + "/python", ["jobrunner.py", func_filename, data_filename, output_filename]);
        var pythonProc = attempt_python.childProcess;

        attempt_python.then((err) =>{
          storage_bucket.upload(output_filename, {destination: req.body.output_key})
          .then((err) => {
            const status_file = storage_bucket.file(req.body.status_key);
            stream = status_file.createWriteStream();
            stream.write(JSON.stringify(response), function() {
              stream.end();
              console.log("write completed " + req.body.status_key);
            });
            fs.writeFile("/tmp/status", JSON.stringify(response), function(err) {
                if (err) {
                    return console.log(err);
                } 
                console.log("flush to fs");
            });
            res.send("ok");
          })
          .catch(function(err){
             console.error('Err w uploading output pickle or status file', err);
             res.send("line 80");
          });
        });
      }).catch(function(err){
        console.error('Error somewhere after launching python', err);
        res.send("line 85");
      });
    }).catch(function(err) {
      console.error('Error ', err);
      response["exception"] = err.toString();
     
      const status_file = storage_bucket.file(req.body.status_key);
      console.log(req.body.status_key);
      stream = status_file.createWriteStream();
      stream.write(JSON.stringify(response));
      stream.end();
      res.send("fail");
    });
}


/*
 * Utility functions to figure out what's going on under the hood, 
 */
exports.neitzsche = function HELLO (event, callback) {
  var promise = spawn("whoami");
  var childProcess = promise.childProcess;

  childProcess.stdout.on('data', function (data) {
    console.log('[spawn] stdout: ', data.toString());
  });
  childProcess.stderr.on('data', function (data) {
    console.log('[spawn] stderr: ', data.toString());
  });

  promise.then(function(result) {
    console.log(result.stdout.toString());
  }).catch(function(err) {
    console.error(err.stderr);
  }); 
  callback();
}

exports.list = function list(event, callback) {
  var LS_COMMAND = spawn("ls", ["-lha", "/tmp"]);
  var childProc = LS_COMMAND.childProcess;

  childProc.stdout.on('data', function (data) {
    console.log("[LS] stdout: ", data.toString());
  });
  childProc.stderr.on('data', function (data) {
    console.log("[LS] stderr: ", data.toString());
  });

  LS_COMMAND.then(function(result) {
    console.log(result.toString());
  });
}

/* Debian
exports.OS = function list(req, res) {
  var LS_COMMAND = spawn("cat", ["/etc/issue"]);
  var childProc = LS_COMMAND.childProcess;

  childProc.stdout.on('data', function (data) {
    console.log("[OS] stdout: ", data.toString());
  });
  childProc.stderr.on('data', function (data) {
    console.log("[OS] stderr: ", data.toString());
  });

  LS_COMMAND.then(function(result) {
    console.log(result.toString());
  });
  res.send("ok");
}
*/
