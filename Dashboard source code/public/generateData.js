var db= firebase.firestore(app);
function getData(lot,year,month,day){
  var counter1=0
  var counter2=0
  var data_dic={}
  var path=String(lot+'/'+year+'/'+month+'.'+day);
    db.collection("parking_lots_v2").doc(String(lot)).collection("year")
    .doc(String(year)).collection("month").doc(String(month)).collection("day")
    .doc(String(day)).collection("data").get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
        data_dic[doc.id]=doc.data();
      });
    });
    // return {path:data_dic}
    collectData(lot,year,month,day,data_dic);
}

function collectData(lot,year,month,day,data){
  // console.log(lot,year,month,day,data);
  day_dic[day]=data;
  month_dic[month]=day_dic;
  year_dic[year]=month_dic;
  lot_dic[lot]=year_dic;
  // console.log(lot_dic);

}

var database_content={};
var lot;
var year=2018;
var month=0;
var day;
var lot_dic={};
var year_dic={};
var month_dic={};
var day_dic={};

function fetchData(){
  return new Promise((resolve, reject)=>{
    month++;
    if (month>12){
      month=1;
      if(year==2018){
        year=2019;
      }
    }
    for (lot=1;lot<19;lot++){
      for (day=1; day <31; day++) {
          getData(lot,year,month,day)
      }
    }
    resolve();
});
// console.log(lot_dic);
var lotarray=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
var lotarray2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
}
fetchData().then(()=>{
  setTimeout(()=>{
  var prevState=false;
  var hourIn;
  var minuteIn;
  var counter=0;
  var avrgHour=0;
  var avrgMinute=0;
  var datapath;
  console.log(lot_dic);

    for (var lot in lot_dic) {
      if (lot_dic.hasOwnProperty(lot)) {
        for (var year in lot_dic[lot]) {
          if (lot_dic[lot].hasOwnProperty(year)) {
            for (var month in lot_dic[lot][year]) {
              var monthG=lot_dic[lot][year][month];
              if (lot_dic[lot][year].hasOwnProperty(month)) {
                for (var day in monthG) {
                  if (monthG.hasOwnProperty(day)) {
                    // console.log(lot_dic[lot][year][month][day]);
                    var dataG=lot_dic[lot][year][month][day];
                    console.log(dataG);
                    for (var data in dataG) {
                      console.log(data);
                      if (dataG.hasOwnProperty(data)) {
                        var event=String(data)
                        datapath=String(lot+'/'+year+'/'+month+'.'+day);
                        var currentState=dataG[data]['state'];
                        var index=event.indexOf('_');
                        var eventLength=event.length;
                        console.log(currentState,index,eventLength);
                        var hour=Number(event.slice(0,index));
                        var minute=Number(event.slice(index+1));
                        // console.log(event);
                        // console.log('min',minute);
                        if(currentState==true ){
                          hourIn=hour;
                          minuteIn=minute;
                          prevState=currentState;
                          counter++;
                        }else if (currentState==false && prevState==true) {
                          if(hour>hourIn){
                            var hourDiff=hour - hourIn;
                            avrgHour+=hourDiff/2;
                          }
                          if(minute>minuteIn){
                            var minuteDiff= minute - minuteIn;
                          }else{
                            var minuteDiff= 60 - minute + minute;
                          }
                          console.log(hourDiff,minuteDiff);

                          avrgMinute+=minuteDiff/2;
                        }
                        console.log(datapath,avrgHour,counter);
                      }
                    }

                  }
                }
              }
            }

          }
        }
      }
      }
    },10000);
// if(counter!= 0){
//   var totalAverageTime = String(avrgHour+':'+avrgMinute);
//   db.collection("averageTime").doc(datapath).set(
//   { averageTime: totalAverageTime,
//     occupancyRate: counter},
//   {merge:true}).then(function() {
//     console.log("Document successfully written!");
//   }).catch(function(error) {
//       console.error("Error writing document: ", error);
//   });
// }
});
// function generateData(datapath,data){
//   var prevState=false;
//   var hourIn;
//   var minuteIn;
//   var counter=0;
//   var avrgHour=0;
//   var avrgMinute=0;
//
//   for (var event in data) {
//     if (data.hasOwnProperty(event)) {
//       var currentState=data[event]['state'];
//       var hour=Number(event.slice(0,event.indexOf('_')));
//       var minute=Number(event.slice(event.indexOf('_'),-1));
//       if(currentState==true && prevState==false){
//         hourIn=hour;
//         minuteIn=minute;
//         prevState=currentState;
//         counter++;
//       }else if (currentState==false && prevState==true) {
//         var hourDiff=hour - hourIn;
//         var minuteDiff= minute - minuteIn;
//         avrgHour+=hourDiff/counter;
//         avrgMinute+=minuteDiff/counter;
//       }
//     }
//   }
//     console.log(datapath,avrgHour,counter,data);
//   if(counter!= 0){
//     var totalAverageTime = String(avrgHour+':'+avrgMinute);
//     db.collection("averageTime").doc(datapath).set(
//     { averageTime: totalAverageTime,
//       occupancyRate: counter},
//     {merge:true}).then(function() {
//       console.log("Document successfully written!");
//     }).catch(function(error) {
//         console.error("Error writing document: ", error);
//     });
//   }
// }


function clear(){
  clearInterval(interval);
}
