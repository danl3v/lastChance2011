/*
 * countdown.js
 * Last Chance Dance 2011
 * Modified from ricocheting.com
 * NOTE: the month entered must be one less than current month. ie; 0=January, 11=December
 * NOTE: the hour is in 24 hour format. 0=12am, 15=3pm etc
 * format: dateFuture1 = new Date(year,month-1,day,hour,min,sec)
 * example: dateFuture1 = new Date(2003,03,26,14,15,00) = April 26, 2003 - 2:15:00 pm
 */

/*global document, setTimeout */

var dateNow, days, hours, mins, secs, out, amount;

function GetCount(cdate,ddate,iid){
    dateNow = cdate; // grab current date
    amount = ddate.getTime() - dateNow.getTime(); // calc milliseconds between dates

    if (amount < 0) { document.getElementById(iid).innerHTML = "Now!"; } // if time already passed
    else {
        days=0; hours=0; mins=0; secs=0; out="";
    
        amount = Math.floor(amount/1000); // kill the "milliseconds" so just secs
    
        days = Math.floor(amount/86400); // days
        amount = amount % 86400;
    
        hours = Math.floor(amount/3600); // hours
        amount = amount % 3600;
    
        mins = Math.floor(amount/60); // minutes
        amount = amount % 60;
    
        secs = Math.floor(amount); // seconds
    
        out += (days<=9?'0':'')+days +" "+((days===1)?"day":"days")+", ";
        out += (hours<=9?'0':'')+hours +" "+((hours===1)?"hour":"hours")+", ";
        out += (mins<=9?'0':'')+mins +" "+((mins===1)?"min":"mins")+", ";
        out += (secs<=9?'0':'')+secs +" "+((secs===1)?"sec":"secs")+", ";
        out = out.substr(0,out.length-2);
        document.getElementById(iid).innerHTML=out;
    
        setTimeout(function(){ GetCount(new Date(cdate-(-1000)),ddate,iid); }, 1000);
    }
}