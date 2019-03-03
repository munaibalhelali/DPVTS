var occupancyChart;
var averageChart;
var revenueChart;
var compareChart;
const month_label=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30'];
const year_label =['1','2','3','4','5','6','7','8','9','10','11','12']
var view_label;
var my_avrg_Chart = document.getElementById('average-parking-time-chart').getContext('2d');
var my_occupancy_Chart = document.getElementById('my-occupancy-Chart').getContext('2d');
var my_revenue_Chart = document.getElementById('my-revenue-Chart').getContext('2d');
var my_avrg_compare_Chart = document.getElementById('my-avrg-compare-Chart').getContext('2d');
var my_occupancy_compare_Chart = document.getElementById('my-occupancy-compare-Chart').getContext('2d');

if(viewOption=='month'){
  view_label=month_label;
  var view_per = chosenDate.slice(0,chosenDate.lastIndexOf('-'));
}else if(viewOption=='year'){
  view_label=year_label;
  var view_per=chosenDate.slice(0,chosenDate.indexOf('-'));
}else{
  var view_per=chosenDate
}
var averageChartTitle='Average Parking Time per Parking Lot as of: '+ view_per;
var occupancyChartTitle='Parking Occupancy Rate per Parking Lot as of: '+ view_per;
var revenueChartTitle='Parking Revenue Rate per Parking Lot as of: '+ view_per;
var avrg_compareChartTitle='Average parikng timeline graph as of:'+ view_per;
var occupancy_compareChartTitle='Occupancy timeline graph as of:'+ view_per;

var avrg_data=[]
var occupancy_data=[]
var revenue_data=[]
setTimeout(function () {

  // Global Options
  Chart.defaults.global.defaultFontFamily = 'Lato';
  Chart.defaults.global.defaultFontSize = 18;
  Chart.defaults.global.defaultFontColor = '#777';

  var array=[];
  var r;
  var g;
  var b;
  for (var i = 0; i < 2; i++) {
    r=Math.floor(Math.random()*255)+1;
    g= Math.floor(Math.random()*255)+1;
    b=Math.floor(Math.random()*255)+1;
    array[i]="rgba("+r+", "+g+", "+b+", 0.6)";
  }

  avrg_data=[]
  occupancy_data=[]
  revenue_data=[]
  for (var i = 0; i < 2; i++) {
    // data[i]=  Math.floor(Math.random()*1000)+1;
    avrg_data.push(avrg_rate_data[i+13])
    occupancy_data.push(occupancy_rate_data[i+13])
    revenue_data.push(revenue_rate_data[i+13])
    // console.log('avrg_data',avrg_data);

  }

  occupancyChart = new Chart(my_occupancy_Chart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1','2'],
      datasets:[{
        label:'Occupancy Rate',
        data:occupancy_data,
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
      labels:['1','2'],
      datasets:[{
        label:'Revenue rate (RM)',
        data:revenue_data,
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


  averageChart = new Chart(my_avrg_Chart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:['1','2'],
      datasets:[{
        label:'Average duration (Minutes)',
        data:avrg_data,
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
  compare_avrg_Chart = new Chart(my_avrg_compare_Chart, {
    type:'line', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:view_label,
      datasets:[{
        label:'Disabled lot 1',
        data:avrg_disablelot_1_data,
        //backgroundColor:'green',
        backgroundColor:'transparent',
        borderWidth:3,
        borderColor:array[0],
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
      },{
        label:'Disabled lot 2',
        data:avrg_disablelot_2_data,
        //backgroundColor:'green',
        backgroundColor:'transparent',
        borderWidth:3,
        borderColor:array[1],
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
      }]
    },
    options:{
      title:{
        display:true,
        text:avrg_compareChartTitle,
        fontSize:18
      },
      legend:{
        display:true,
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
                 labelString:'Days',
                 fontSize:14

               }
           }]
    }
    }
  });
  compare_occupancy_Chart = new Chart(my_occupancy_compare_Chart, {
    type:'line', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
      labels:view_label,
      datasets:[{
        label:'Disabled lot 1',
        data:occu_disablelot_1_data,
        //backgroundColor:'green',
        backgroundColor:'transparent',
        borderWidth:3,
        borderColor:array[0],
        hoverBorderWidth:3,
        hoverBorderColor:'#000',


      },{
        label:'Disabled lot 2',
        data:occu_disablelot_2_data,
        //backgroundColor:'green',
        backgroundColor:'transparent',
        borderWidth:3,
        borderColor:array[1],
        hoverBorderWidth:3,
        hoverBorderColor:'#000',


      }]
    },
    options:{
      title:{
        display:true,
        text:occupancy_compareChartTitle,
        fontSize:18
      },
      legend:{
        display:true,
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

               id: 'y-axis',
               type: 'linear',
               position: 'left',
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
                 labelString:'Days',
                 fontSize:14

               }
           }]
    }
  }
  });

}, 5000);

function updateGraphs(){
  var timeLineScaleLabel;
  avrg_data=[]
  occupancy_data=[]
  revenue_data=[]
  setTimeout(()=>{
    console.log('updating the graphs');
    // console.log();
    console.log(avrg_disablelot_1_data);
    console.log(avrg_disablelot_2_data);
    console.log(occu_disablelot_1_data);
    console.log(occu_disablelot_2_data);
    if(viewOption=='month'){
      view_label=month_label;
      timeLineScaleLabel='Days'
      var view_per = chosenDate.slice(0,chosenDate.lastIndexOf('-'));
    }else if(viewOption=='year'){
      view_label=year_label;
      timeLineScaleLabel='Months'
      var view_per=chosenDate.slice(0,chosenDate.indexOf('-'));
    }else{
      view_label=[''];
      var view_per=chosenDate
      timeLineScaleLabel='Day'
    }

    for (var i = 0; i < 2; i++) {
      // data[i]=  Math.floor(Math.random()*1000)+1;
      avrg_data.push(avrg_rate_data[i+12])
      occupancy_data.push(occupancy_rate_data[i+12])
      revenue_data.push(revenue_rate_data[i+12])
      // console.log('avrg_data',avrg_data);

    }

    averageChartTitle='Average Parking Time per Parking Lot as of: '+ view_per;
    occupancyChartTitle='Parking Occupancy Rate per Parking Lot as of: '+ view_per;
    revenueChartTitle='Parking Revenue Rate per Parking Lot as of: '+ view_per;
    compareChartTitle='Average parikng timeline graph as of:'+ view_per;
    occupancy_compareChartTitle='Occupancy timeline graph as of:'+ view_per;

    revenueChart.data.datasets[0].data=revenue_data;
    revenueChart.options.title.text=revenueChartTitle;
    revenueChart.update();

    occupancyChart.data.datasets[0].data=occupancy_data;
    occupancyChart.options.title.text=occupancyChartTitle;
    occupancyChart.update();

    averageChart.data.datasets[0].data=avrg_data;
    averageChart.options.title.text=averageChartTitle;
    averageChart.update();

    compare_avrg_Chart.data.datasets[0].data=avrg_disablelot_1_data;
    compare_avrg_Chart.data.datasets[1].data=avrg_disablelot_2_data;
    compare_avrg_Chart.options.title.text=compareChartTitle;
    compare_avrg_Chart.data.labels=view_label;
    compare_avrg_Chart.options.scales.xAxes[0].scaleLabel.labelString=timeLineScaleLabel;
    compare_avrg_Chart.update();

    compare_occupancy_Chart.data.datasets[0].data=occu_disablelot_1_data;
    compare_occupancy_Chart.data.datasets[1].data=occu_disablelot_2_data;
    compare_occupancy_Chart.options.title.text=occupancy_compareChartTitle;
    compare_occupancy_Chart.data.labels=view_label;
    compare_occupancy_Chart.options.scales.xAxes[0].scaleLabel.labelString=timeLineScaleLabel;
    compare_occupancy_Chart.update();

  },5000);


}
