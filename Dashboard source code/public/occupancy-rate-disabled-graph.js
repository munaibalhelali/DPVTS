setTimeout(function () {
  var lotarrayF=lotarray.map(function(value, index, array){
    return value/3;
  });
  var myChart = document.getElementById('my-occupancy-Chart').getContext('2d');

  // Global Options
  Chart.defaults.global.defaultFontFamily = 'Lato';
  Chart.defaults.global.defaultFontSize = 18;
  Chart.defaults.global.defaultFontColor = '#777';
  var array=[];
  var r;
  var g;
  var b;
  for (var i = 0; i < 3; i++) {
    r=Math.floor(Math.random()*255)+1;
    g= Math.floor(Math.random()*255)+1;
    b=Math.floor(Math.random()*255)+1;
    array[i]="rgba("+r+", "+g+", "+b+", 0.6)";
  }
  var data=[]
  for (var i = 0; i < 2; i++) {
    // data[i]=  Math.floor(Math.random()*1000)+1;
    data[i+1]=lotarrayF[i+13]

  }
  data[0]=0;
  console.log(data);
  var massPopChart = new Chart(myChart, {
    type:'horizontalBar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['','13','14'],
      datasets:[{
        label:'Occupancy Rate',
        data:data,
        //backgroundColor:'green',
        backgroundColor:array,
        borderWidth:1,
        borderColor:'#777',
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
      }]
    },
    options:{
      title:{
        display:true,
        text:'Parking Occupancy Rate per Parking Lot',
        fontSize:25
      },
      legend:{
        display:false,
        position:'right',
        labels:{
          fontColor:'#000'
        }
      },
      layout:{
        padding:{
          left:10,
          right:10,
          bottom:0,
          top:10
        }
      },
      tooltips:{
        enabled:true
      }
    }
  });

}, 8000);
