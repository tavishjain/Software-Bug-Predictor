const process = require('process');
const {shell,remote} = require('electron');

const gitRequest= require('./utils/gitRequest.js');
const dataScript = require('./utils/dataScript.js');
const resultScript = require('./utils/resultScript.js');

const grLifeCycle = async (url) => {
	const validrequest = await gitRequest(url);
	if(validrequest.data!==undefined){
		console.log('link valid');
		document.getElementsByName('cspan11')[0].classList.toggle('visible');
		document.getElementsByName('cspan12')[0].classList.toggle('visible');

	}
	//loading the repository python script
	const datafile = await dataScript({username:'ram',password:'1234'},url); 
	if(datafile.address!==undefined){
		console.log('data '+ datafile.address);
		document.getElementsByName('cspan21')[0].classList.toggle('visible');
		document.getElementsByName('cspan22')[0].classList.toggle('visible');
	}
	//generating the report python script
	const resultfile = await resultScript(datafile.address);
	if(resultfile.address!==undefined){
		console.log('report '+resultfile.address);
		document.getElementsByName('cspan31')[0].classList.toggle('visible');
		document.getElementsByName('cspan32')[0].classList.toggle('visible');
		
		document.getElementsByName('toreport')[0].href = resultfile.address;
		document.getElementsByName('toreport')[0].classList.remove('btn-secondary');
		document.getElementsByName('toreport')[0].classList.add('btn-primary');

		
	}
	return resultfile;
};

const resetProptron = ()=>{
	document.getElementsByName('proptron')[0].classList.toggle('visible');
		
	if(!document.getElementsByName('cspan11')[0].classList.contains('visible'))
		document.getElementsByName('cspan11')[0].classList.add('visible');
	if(!document.getElementsByName('cspan21')[0].classList.contains('visible'))
		document.getElementsByName('cspan21')[0].classList.add('visible');
	if(!document.getElementsByName('cspan31')[0].classList.contains('visible'))	
		document.getElementsByName('cspan31')[0].classList.add('visible');
	
	document.getElementsByName('cspan12')[0].classList.remove('visible');
	document.getElementsByName('cspan22')[0].classList.remove('visible');
	document.getElementsByName('cspan32')[0].classList.remove('visible');

	document.getElementsByName('toreport')[0].href = '###';
	document.getElementsByName('toreport')[0].classList.add('btn-secondary');
	document.getElementsByName('toreport')[0].classList.remove('btn-primary');
}

window.onload = (event)=>{
	console.log('loading done');
	let form = document.getElementsByName('myForm')[0];
	let proptron = document.getElementsByName('proptron')[0];
	let reportButton = document.getElementsByName('toreport')[0];
	
	form.onsubmit = (event)=>{
		event.preventDefault();
		let url = form.elements['searchQuery'].value;
		// ***** DANGER ***** 
		url = 'https://github.com/tavishjain/Popbuzz';
		if(!/^$|\s+/.test(url)){
			console.log('initiating getRepo');
			//launch loader css
			if(!proptron.classList.contains('visible'))
			proptron.classList.toggle('visible');
			
			//initiate async
			grLifeCycle(url).then((value)=>{
				//set the button url
				//change the button color
				console.log("runer boi");
			}).catch((value)=>{
				//make the 
				console.log('error');
				// console.log(value);
				resetProptron();
				// console.log(value.error);
						
			});
		}
	};

	reportButton.onclick = (event)=>{
		event.preventDefault();
		//redirect
		var filename = reportButton.href;
		if(process.platform === "win32")filename = filename.split("\\").join("\\\\");
		console.log(filename);
		shell.openItem(reportButton.href);
		//C:\Users\Admin\Desktop\Moglix\error_predictor\Python\dataLogs\reports\report1.csv
		//C:\Users\Admin\Desktop\Moglix\error_predictor\python\reports\report1.csv
		//visible elements reset
		resetProptron();
	}

};


	

// btn.addEventListener('click',function() {
// 	alert('Clicked!');
//  });


// function sendRequest(){

// console.log('here1');
// 	var x = document.forms["myForm"]["searchQuery"].value;


// 	ipc.send('repo-url-entered',x);

// 	document.forms["myForm"].reset();

// }
	// $("body").append('<div id="overlay" style="background-color:grey;position:absolute;top:0;left:0;height:100%;width:100%;z-index:999"></div>');

	//window.alert("The request has been sent to backend");

	// //...
	// //...
	// //modification of x to appropriate xml form
	// //...
	// //...

	//var xhttp = new XMLHttpRequest();

	// xhttp.onreadystatechange = function() {

	// 	if(this.readyState == 2 && this.status==100){
	// 		document.alert("the request is recieved")
	// 	}
	// 	else if(this.readyState == 2){
	// 		document.alert('the request is not recieved');
	// 	}

 //    if (this.readyState == 4 && this.status == 200) {
 //      document.getElementById("demo").innerHTML =
 //      this.responseText;
 //    }
 //  };

	// $("#overlay").remove();

	// function urlParser(address){
	// 	let url,repo;
	// 	if(/^(http|https):/.test(address)){
	// 		// console.log('http matching');
	// 		url = address;
	// 	}else if(/^github\.com/.test(url)){
	// 		// console.log('matching git');
	// 		url = 'https://' + address;
	// 	}else{
	// 		// console.log('matching nothing');
	// 		url = 'https://github.com/' + address;
	// 	}
	// 	repo = str.replace("https://github.com/", "");
	// 	console.log(`repor: ${repo}`);
	// 	return url;
	// } 




     

