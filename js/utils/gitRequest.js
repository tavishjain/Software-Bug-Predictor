const request = require('request');
const cheerio = require('cheerio');

function urlParser(address){
    let url,repo;
    if(/^(http|https):/.test(address)){
        // console.log('http matching');
        url = address;
    }else if(/^github\.com/.test(address)){
        // console.log('matching git');
        url = 'https://' + address;
    }else{
        // console.log('matching nothing');
        url = 'https://github.com/' + address;
    }
    repo = url.replace("https://github.com/", "");
    //console.log(`repor: ${repo}`);
    return{url,repo};
} 


const gitrequest = async (address) =>{
    let {url,repo} = urlParser(address);
    let repoReg = new RegExp(repo);

    return new Promise((resolve, reject) => {
        request(url, (error,response,html) => {
            if(error){ 
            reject( {error:'Unable to connect to git services!',data:undefined});
            }else{ 
                var $ = cheerio.load(html);
                var titleStr =  $("head > title").text();
                // console.log(repo);
                // console.log(titleStr);
                if(repoReg.test(titleStr)&&repo!=""){
                    resolve({error:undefined,data:url});
                } else{
                    reject({error:'can not find the requested repo',data:undefined});
                }
            }    
        });
    });
}


module.exports = gitrequest