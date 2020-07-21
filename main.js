const electron = require('electron');
const debug = require('electron-debug');       //for dev tools 
const gitapi = require('./gitapi');

const path = require('path');
const url = require('url');


const {app, BrowserWindow, Menu, ipcMain,dialog} = electron;

let mainWindow;
let webWindow;

debug();                           


app.on('ready', function(){
  // Create new window
  mainWindow = new BrowserWindow({resizable: false,height: 750, width:900,
    webPreferences: {
      nodeIntegration: true
      // preload: path.join(__dirname, 'js/mainWindow.js')
  }
  });
  // Load html in window
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'html/mainWindow.html'),
    protocol: 'file:'
    //slashes:true
  }));

  mainWindow.webContents.openDevTools();                   //enabling dev tools

 	mainWindow.on('closed', function(){
    	app.quit();
		}
	);
  const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);
  // Insert menu
  Menu.setApplicationMenu(mainMenu);
});


// ipcMain.on('repo-url-entered',(event,arg)=>{

//   dialog.showMessageBox(type = 'info', message = 'Your input has been recorded');

//   gitapi(arg,(error,data)=>{
//       if(error){
//         dialog.showMessageBox(type = 'error', message = error);          
//       }
//       else{
//         dialog.showMessageBox(type = 'error', message = 'your results are ready for {}'.format(data));
//       }
//   });

// });

const mainMenuTemplate =  [
  // Each object is a dropdown
  {
    label: 'Menu',
    submenu:[
      {
        label:'View Logs',
        click(){
            mainWindow.loadURL(url.format({
				    pathname: path.join(__dirname, 'html/mainLogs.html'),
				    protocol: 'file:',
				    slashes:true
        	}));
      	}
    	},
      {
        label:'View Reports',
        click(){
            mainWindow.loadURL(url.format({
    				pathname: path.join(__dirname, 'html/mainReports.html'),
    				protocol: 'file:',
    				slashes:true
        	}));
        }
      },
      {
        label:'Home',
        click(){
            mainWindow.loadURL(url.format({
    				pathname: path.join(__dirname, 'html/mainWindow.html'),
    				protocol: 'file:',
    				slashes:true
        	}));
        }
      }      
    ]
  },
  {
  	label: 'Options',
  	submenu:[

  		{
  			label: 'Reload',
  			accelerator:process.platform == 'darwin' ? 'Command+R' : 'Ctrl+R',
        // click(){
        //     mainWindow.loadURL(url.format({
    				// pathname: app.Reload(),
    				// protocol: 'file:',
    				// slashes:true
        // 	}));
        //}
        role: 'reload' 		 //default functionality
  		},

  		{
  			label: 'Quit',
  			accelerator:process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
		    click(){
		      app.quit();
		    }
  		}
  	]
  },
  {
    label: 'GitHub',
    click(){
      webWindow = new BrowserWindow({resizable: true,height: 750, width:900});
      webWindow.loadURL('https://github.com');
    }
  }
];

if(process.platform == 'darwin'){
	mainMenuTemplate.unshift({});
}