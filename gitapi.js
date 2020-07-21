const request = require('request');


const gitapi = (address,callback) =>{

 		const url = "sd" + address;

	  request({ url:url, json:true },(error,response)=>{
    if(error){
    	callback("your file could not be fetched due to some error",undefined);
    }
    else{

    	// ...... do processing  .........
    	// ...... save the files .........
    	var to_return = "repo_name";
    	callback(undefined,to_return);
    }
  }); 	
};  


module.export  = gitapi;