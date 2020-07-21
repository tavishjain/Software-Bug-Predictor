var {PythonShell} = require('python-shell');
const path = require('path');

const scriptpath = path.join(__dirname, '../../Python/');
const scriptname = 'data_collection_and_generation.py';
const dataScript = async ({username,password},url)=>{
    //console.log(username,password,url);
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: scriptpath,
        args: [url]
      };
    return new Promise((resolve,reject)=>{
        PythonShell.run(scriptname, options, function (err, results) {
            if (err) {
                console.log('script1 failed');
                reject({error:'the data could not be downloaded or ',address:undefined})
            }
                // results is an array consisting of messages collected during execution
            else{
                // console.log(results[0]);
                resolve({error:undefined,address: results[0]});
            }
            });
    });
};

module.exports = dataScript;