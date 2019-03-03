

var returnText1= document.getElementById('outputText1');
var returnText2= document.getElementById('outputText2');
var lotState=[];
var lotInTime=[];
buttonCounter();

var firebaseRef = firebase.database().ref().child("parking_lots");
firebaseRef.on('value', function(snapshot) {
  lotState=[];
  lotInTime=[];
  snapshot.forEach(function(childSnapshot) {
    var status = childSnapshot.val().status;
    var time = childSnapshot.val().time;
    updateButn(status,childSnapshot.key);
    lotState.push(status);
    lotInTime.push(time);

  });
});
function updateButn(state, lotId){
  var button = document.getElementById(lotId);
  if(state == true){
    button.className = 'occupied';

  }else if(state==false){
    button.className = 'available';
  }
}

function buttonCounter(mode=0){
  var i;
  var today = new Date();
  var epochTime=(new Date).getTime()/1000;
  var ch = today.getHours();
  var cm = today.getMinutes();
  for(i=0; i<lotState.length;i++){

    var time= lotInTime[i];
    time=epochTime-time;
    var h=Math.floor(time/3600);
    var m=Math.floor((time -(h*3600))/60);
    h=checkTime(h);
    m=checkTime(m);
    if(i+1==13 ){
      if(lotState[i]){
        document.getElementById("disp1").innerHTML='<br><br><br>13<br>Duration:\n'+h+':'+m;
      }else{
        document.getElementById("disp1").innerHTML='<br><br><br>13<br>Parking available';
      }
    }else if(i+1==14){
      if(lotState[i]){
        document.getElementById(14).innerHTML='<br><br><br>14<br>Duration:\n'+h+':'+m;
      }else{
        document.getElementById(14).innerHTML='<br><br><br>14<br>Parking available';
      }
    }else{
      if(!lotState[i]){
        document.getElementById(i+1).innerHTML=i+1+" \nparking\navailable";
      }else{
      document.getElementById(i+1).innerHTML=i+1+'\nDuration:\n'+h+':'+m;
      }
    }
  }

var t = setTimeout(buttonCounter, 500);
}
function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

function showCounter(id){

    var today = new Date();
    var epochTime=(new Date).getTime()/1000;
    var ch = today.getHours();
    var cm = today.getMinutes();
    var time= lotInTime[id-1];
    time=epochTime-time;
    var h=Math.floor(time/3600);
    var m=Math.floor((time -(h*3600))/60);
    h=checkTime(h);
    m=checkTime(m);
    if(lotState[id-1] == true){
    window.alert("Parking lot No. "+ id+  " have been occupied for: "+'\n'+h+':'+m);
  }else{
    window.alert("Parking lot No. "+ id+  " have been availabel for: "+'\n'+h+':'+m);
  }
}

function control_panel(){
  var parking_zone = document.forms["controlpanel"]["parking-area"].value;
  var view_mode = document.forms["controlpanel"]["view-type"].value;
  try {
    var input_date= document.forms["controlpanel"]["choose-date"].value;
    var index1=input_date.indexOf('-');
    var index2=input_date.lastIndexOf('-');
    var year=Number(input_date.slice(0,index1));
    var month=Number(input_date.slice(index1+1,index2));
    var day=Number(input_date.slice(index2+1));
  } catch (e) {
    console.log(e);
    return ;
  }

  console.log(year,':',month,':',day);
  setDataValues(year,month,day,view_mode,'non_disabled')
  var area=document.getElementById("parking_area_image");
  var body=document.getElementById("body");
  if(parking_zone == "FOE"){
    area.className='foe';
    body.className='foebody';
  }else if (parking_zone=="FOM") {
    area.className='fom';
    body.className='fombody';
  }else if (parking_zone=="FCI") {
    area.className='fci';
    body.className='fcibody';
  }

}
