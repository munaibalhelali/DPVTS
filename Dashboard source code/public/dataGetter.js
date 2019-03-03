var db= firebase.firestore(app);
var viewOption='month'
var dayOption=1
var monthOption=1
var yearOption=2018
var chosenDate=String(yearOption)+'-'+String(monthOption)+'-'+String(dayOption)
var avrg_rate_data=[];
var revenue_rate_data=[];
var occupancy_rate_data=[];
var avrg_disablelot_1_data=[];
var avrg_disablelot_2_data=[];
var occu_disablelot_1_data=[];
var occu_disablelot_1_data=[];

function getData(lot,year,month){
  avrg_disablelot_1_data=[];
  avrg_disablelot_2_data=[];
  occu_disablelot_1_data=[];
  occu_disablelot_2_data=[];

  avrg_rate_data=[];
  revenue_rate_data=[];
  occupancy_rate_data=[];

  if(viewOption=='year'){
    for(var month1=1;month1<13;month1++){
      db.collection("parking_lot_avrg").doc(String(lot)).collection("year")
      .doc(String(year)).collection("month").doc(String(month1))
      .get().then(function(doc) {
        if (doc.exists) {
          if(lot==13){
            avrg_disablelot_1_data.push(doc.data()["monthlyAvrg"]);
            occu_disablelot_1_data.push(doc.data()["monthly_occupancy"]);
          }else if(lot==14){
            avrg_disablelot_2_data.push(doc.data()["monthlyAvrg"]);
            occu_disablelot_2_data.push(doc.data()["monthly_occupancy"]);
          }
        }
      }).catch(function(error) {
        console.log("Error getting document:", error);
        });
    }


    db.collection("parking_lot_avrg").doc(String(lot)).collection("year")
    .doc(String(year))
    .get().then(function(doc) {
      if (doc.exists) {

          // console.log("Document data:", doc.data());
          avrg_rate_data.push(doc.data()["annualAvrg"]);
          occupancy_rate_data.push(doc.data()["annual_occupancy"]);
          revenue_rate_data.push(doc.data()["annual_revenue"]);
        } else {
            // doc.data() will be undefined in this case
            console.log("No such document!");
          }
        }).catch(function(error) {
        console.log("Error getting document:", error);
        });
  }else{
    db.collection("parking_lot_avrg").doc(String(lot)).collection("year")
    .doc(String(year)).collection("month").doc(String(month))
    .get().then(function(doc) {
      if (doc.exists) {

        if(viewOption=='day'){
          if(lot==13){
            avrg_disablelot_1_data=[doc.data()["dailyAvrg"][dayOption-1]]
            occu_disablelot_1_data=[doc.data()["daily_occupancy"][dayOption-1]];
            console.log(doc.data()["dailyAvrg"],avrg_disablelot_1_data);
          }else if(lot==14){
            avrg_disablelot_2_data=[doc.data()["dailyAvrg"][dayOption-1]];
            occu_disablelot_2_data=[doc.data()["daily_occupancy"][dayOption-1]];
            console.log(doc.data()["dailyAvrg"],avrg_disablelot_2_data);
          }
          // console.log("Document data:", doc.data());
          avrg_rate_data.push(doc.data()["dailyAvrg"][dayOption-1]);
          console.log('dailyAvrg', avrg_rate_data);
          occupancy_rate_data.push(doc.data()["daily_occupancy"][dayOption-1]);
          revenue_rate_data.push(doc.data()["daily_revenue"][dayOption-1]);
        }else if(viewOption=='month'){
          if(lot==13){
            avrg_disablelot_1_data=doc.data()["dailyAvrg"];
            occu_disablelot_1_data=doc.data()["daily_occupancy"];
          }else if(lot==14){
            avrg_disablelot_2_data=doc.data()["dailyAvrg"];
            occu_disablelot_2_data=doc.data()["daily_occupancy"];
          }
          avrg_rate_data.push(doc.data()["monthlyAvrg"]);
          occupancy_rate_data.push(doc.data()["monthly_occupancy"]);
          revenue_rate_data.push(doc.data()["monthly_revenue"]);
          console.log(avrg_rate_data,'\n',occupancy_rate_data,'\n',revenue_rate_data);
        }
      } else {
          // doc.data() will be undefined in this case
          console.log("No such document!");
      }
      }).catch(function(error) {
      console.log("Error getting document:", error);
      });
    }
}

function getDataLoop(){
  for (var lot=1;lot<19;lot++){
      getData(lot,yearOption,monthOption);
  }

  try {
    updateGraphs()
  //   if(calledby=='disabled'){
  //   draw_disabled_graphs();
  // }else if (calledby=='non_disabled'){
  //   draw_non_disabled_graphs();
  //   console.log('updating graphs');
  // }
  } catch (e) {
  //   console.log(e);
  }

}
getDataLoop()
// console.log(lot_dic);

function setDataValues(year,month,day,mode,calledby){
  if (year==0) {
    return ;
  }
  calledby=calledby;
  console.log(year, month,day,mode);
  yearOption=year;
  monthOption=month;
  dayOption=day;
  viewOption=mode;
  chosenDate=String(year)+'-'+String(month)+'-'+String(day)
  getDataLoop();

}
