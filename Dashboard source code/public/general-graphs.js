var averageChart;
var occupancyChart;
var revenueChart;
var my_avrg_Chart = document.getElementById('average-parking-time-chart').getContext('2d');
var my_occupancy_Chart = document.getElementById('my-occupancy-Chart').getContext('2d');
var my_revenue_Chart = document.getElementById('my-revenue-Chart').getContext('2d');

if(viewOption=='month'){
  var view_per = chosenDate.slice(0,chosenDate.lastIndexOf('-'));
}else if(viewOption=='year'){
  var view_per=chosenDate.slice(0,chosenDate.indexOf('-'));
}else{
  var view_per=chosenDate
}
var averageChartTitle='Average Parking Time per Parking Lot as of: '+ view_per;
var occupancyChartTitle='Parking Occupancy Rate per Parking Lot as of: '+ view_per;
var revenueChartTitle='Parking Revenue Rate per Parking Lot as of: '+ view_per;
setTimeout(function () {

  // console.log(lotarray);
  // console.log(lotarrayF);
  // console.log(lotarray2);

  my_avrg_Chart.clearRect(0, 0, my_avrg_Chart.width, my_avrg_Chart.height);
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
  averageChart = new Chart(my_avrg_Chart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18'],
      datasets:[{
        label:'Average duration (Minutes)',
        data:avrg_rate_data,
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
        text:averageChartTitle,
        fontSize:18
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
      },
      scales: {
           yAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Average Occupancy Time (Minutes)',
                 fontSize:14
               },
               ticks:{
                 beginAtZero:true
               }
           }],
           xAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Parking Lots',
                 fontSize:14

               }
           }]
    }
    }
  });


  occupancyChart = new Chart(my_occupancy_Chart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18'],
      datasets:[{
        label:'Occupancy rate',
        data:occupancy_rate_data,
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
        text:occupancyChartTitle,
        fontSize:18
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
      },
      scales: {
           yAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Occupancy Rate',
                 fontSize:14
               },
               ticks:{
                 beginAtZero:true
               }
           }],
           xAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Parking Lots',
                 fontSize:14

               }
           }]
    }
    }
  });


  revenueChart = new Chart(my_revenue_Chart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1', '2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16','17','18'],
      datasets:[{
        label:'Revenue rate (RM)',
        data:revenue_rate_data,
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
        text:revenueChartTitle,
        fontSize:18
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
      },
      scales: {
           yAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Revenue Rate (RM)',
                 fontSize:14
               },
               ticks:{
                 beginAtZero:true
               }
           }],
           xAxes: [{
               scaleLabel:{
                 display:true,
                 labelString:'Parking Lots',
                 fontSize:14

               }
           }]
    }
    }
  });


}, 5000);

function updateGraphs(){
  setTimeout(()=>{
    console.log('updating the graphs');
    if(viewOption=='month'){
      view_per = chosenDate.slice(0,chosenDate.lastIndexOf('-'));
    }else if(viewOption=='year'){
      view_per=chosenDate.slice(0,chosenDate.indexOf('-'));
    }else{
      view_per=chosenDate
    }
    averageChartTitle='Average Parking Time per Parking Lot as of: '+ view_per;
    occupancyChartTitle='Parking Occupancy Rate per Parking Lot as of: '+ view_per;
    revenueChartTitle='Parking Revenue Rate per Parking Lot as of: '+ view_per;

    revenueChart.data.datasets[0].data=revenue_rate_data;
    revenueChart.options.title.text=revenueChartTitle;
    revenueChart.update();

    occupancyChart.data.datasets[0].data=occupancy_rate_data;
    occupancyChart.options.title.text=occupancyChartTitle;
    occupancyChart.update();

    averageChart.data.datasets[0].data=avrg_rate_data;
    averageChart.options.title.text=averageChartTitle;
    averageChart.update();

  },5000);


}
