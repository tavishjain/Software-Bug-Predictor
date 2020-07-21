var {PythonShell} = require('python-shell');

const path = require('path');

const scriptpath = path.join(__dirname, '../../python/');

let options = {
  mode: 'text',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: scriptpath,
  args: ['value1', 'value2', 'value3']
};
 
PythonShell.run('script2.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', path.join(scriptpath,results[0]));
});