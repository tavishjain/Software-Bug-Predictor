const {shell,remote} = require('electron');
const process = require('process');
const filesize = require('filesize');
const moment = require('moment');

window.onload = (event)=>{
    var path = require('path');
    var fs = require('fs');
    
    var dirPath = path.join(__dirname+'./../Python/dataLogs/reports/');
    console.log(dirPath);
    fs.readdir(dirPath, function (err, files) {
        if (err) {
            return console.log('Unable to scan dir ' + err);
        }
        //else  
        
        let parentElement = document.getElementById('elementron');
        // console.log(parentElement);

        files.forEach(function (file) {
            fs.stat(dirPath+file, function(err, stats) {
            // Do something with the file.
                let childElement = document.createElement('div');
                childElement.classList.add("element");
                
                let title = document.createElement('div');
                title.classList.add("elementtitle");
                title.innerText = file;
                
                let size = document.createElement('div');
                size.classList.add("elementsize");
                size.innerText = "size: " + filesize(stats.size);
                
                let date = document.createElement('div');
                date.classList.add("elementdate");
                let bdate = moment(stats.birthtimeMs).format("DD/MM/YYYY h:mm:ss a");
                date.innerText = "Created: " + bdate;
                
                let update = document.createElement('div');
                update.classList.add("elementupdate");
                let adate = moment(stats.atimeMs).format("DD/MM/YYYY h:mm:ss a");
                update.innerText = "Modified: " + adate;
                
                let button = document.createElement('button');
                button.classList.add('gotoelement', 'btn', 'btn-sm', 'btn-outline-info');
                button.innerText = 'open';
                button.href = dirPath + file;
                button.onclick = (event)=>{
                    event.preventDefault();
                    //redirect
                    var filename = button.href;
                    if(process.platform === "win32")filename = filename.split("\\").join("\\\\");
                    console.log(filename);
                    shell.openItem(filename);
                    
                };

                childElement.appendChild(title);
                childElement.appendChild(size);
                childElement.appendChild(date);
                childElement.appendChild(update);
                childElement.appendChild(button);

                parentElement.appendChild(childElement);
                // console.log(button.href);
              });
        });
    });
    
}
