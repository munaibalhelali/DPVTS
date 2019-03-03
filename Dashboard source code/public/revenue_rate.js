setTimeout(function () {
  var myChart = document.getElementById('my-revenue-Chart').getContext('2d');

  // Global Options
  Chart.defaults.global.defaultFontFamily = 'Lato';
  Chart.defaults.global.defaultFontSize = 18;
  Chart.defaults.global.defaultFontColor = '#777';
  var array=[];
  var r;
  var g;
  var b;
  for (var i = 0; i < 18; i++) {
    r=Math.floor(Math.random()*255)+1;
    g= Math.floor(Math.random()*255)+1;
    b=Math.floor(Math.random()*255)+1;
    array[i]="rgba("+r+", "+g+", "+b+", 0.6)";
  }
  var data=[]
  for (var i = 0; i < 18; i++) {
    data[i]=  Math.floor(Math.random()*1000)+1;
  }
  var massPopChart = new Chart(myChart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18'],
      datasets:[{
        label:'Revenue rate',
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
        text:'Parking Revenue Rate per Parking Lot',
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
          top:20
        }
      },
      tooltips:{
        enabled:true
      }
    }
  });

}, 8000);
