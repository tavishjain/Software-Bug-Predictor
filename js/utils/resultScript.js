var {PythonShell} = require('python-shell');
const path = require('path');

const scriptpath = path.join(__dirname, '../../Python/');
const scriptName = 'training_ml_model.py';
const resultScript = async (path)=>{
    
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: scriptpath,
        args: [path]
      };
    return new Promise((resolve,reject)=>{
        PythonShell.run(scriptName, options, function (err, results) {
            if (err) {
                console.log('script2 failed');
                reject({error:'the data could not be downloaded or ',address:undefined})
            }
                // results is an array consisting of messages collected during execution
            else{
                // console.log(results[0]);
                resolve({error:undefined,address: path.join(scriptpath,results[0])});
            }
            });
    });
};

module.exports = resultScript;