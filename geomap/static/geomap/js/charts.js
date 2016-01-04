//// ************** RealTime	 *****************   

var xRealtime                         = ['xRealtime'];
var Machine1                          = ['Maschine 1'];
var Machine2                          = ['Maschine 2'];
var d_xRealtime                       = new Date();
d_xRealtime.setSeconds(d_xRealtime.getSeconds() - 22);

for (var i = 0; i < 10; i++) {
          xRealtime.push(d_xRealtime.setSeconds(d_xRealtime.getSeconds() + 2));
          Machine1.push(Math.round(Math.random() * 40) + 220);
          Machine2.push(Math.round(Math.random() * 40) + 50 + Math.max(i-4,0)*40);
}

var chartRealTime                     = c3.generate({
          bindto                      : '#chartRealTime',
          data                        : {
              x                       : 'xRealtime',
              columns                 : [
                  xRealtime, Machine1, Machine2
              ],
              type                    : 'line',
          },
          axis                        : {
              x                       : {
                  type                : 'timeseries',
                  tick                : {
                    format          : '%H:%M:%S', // format string is also available for timeseries data
                    culling         : {
                        max         :  4 // the number of tick texts will be adjusted to less than this value
                }
                  }
              },
              y                       : {
                  min                 : 0,
              }
          },
          color                       : {
              pattern                 : ['#193441', '#682321']
          },
          legend                      : {
              hide                    : 'Normal'
          }
      });

var roundChartRealtime                = 1;

function updateChartRealtime() { //  create a loop function
          setTimeout(function() { //  call a 2s setTimeout when the loop is called
              xRealtime.push(d_xRealtime.setSeconds(d_xRealtime.getSeconds() + 2));
              Machine1.push(Math.round(Math.random() * 40) + 220)
              Machine2.push(Math.round(Math.random() * 40) + 240 - Math.min(roundChartRealtime, 10)*20)
              chartRealTime.load({
                  columns             : [xRealtime, Machine1, Machine2]
              });
              roundChartRealtime++; //  increment the counter
              if (roundChartRealtime < 30) { //  if the counter < 20, call the loop function
                  updateChartRealtime(); //  ..  again which will trigger another 
              } //  ..  setTimeout()
              else{ // remove the first 29 values and start again
                  roundChartRealtime  = 1;
                   xRealtime.splice(1, 29);
                   Machine1.splice(1, 29);
                   Machine2.splice(1, 29);
                  updateChartRealtime();
              }
          }, 1000);
      }
        
updateChartRealtime(); //  start the loop

//// ************** Warning	 *****************   

Value                                 = [
    'Wert',
   201.7443529,
201.9569807,
202.154804,
201.5376642,
202.164203,
202.7688229,
204.7585769,
205.9506103,
205.1222096,
204.642248,
205.4733711,
205.5909015,
207.1733655,
208.5789608,
208.4316581,
207.9697884,
208.0578536,
208.9842139,
210.0496297,
211.009208, 
]

var xWarning                          = ['xWarning']
var Normal                            = ['Normal'];
var Critical                          = ['Critical'];
var Failure                           = ['Failure'];
var d_xWarning                        = new Date()

for (var i = 0, t = 20; i < t; i++) {
          xWarning.push(d_xWarning.setSeconds(d_xWarning.getSeconds() + 2))
          Normal.push(202)
          Critical.push(7)
          Failure.push(5)
}
        
var chartWarning                      = c3.generate({
          bindto                      : '#chartWarning',
          data                        : {
              x                       : 'xWarning',
              columns                 : [
                  xWarning, Normal, Critical, Failure, Value.slice(0,4)
              ],
              type                    : 'area-spline',
              types                   : {
            Value                     : 'line',
        },
              order                   : 'asc',
            groups                    : [['Failure','Critical', 'Normal']]
          },
          axis                        : {
              x                       : {
                  type                : 'timeseries',
                  tick                : {
                    format          : '%H:%M:%S', // format string is also available for timeseries data
                    culling         : {
                        max         :  4 // the number of tick texts will be adjusted to less than this value
                }
              }
              },
              y                       : {
                  min                 : 200,
              }
          },
          color                       : {
              pattern                 : ["none", "yellow","red", '#193441']
          },
          legend                      : {
              show                    : false
          },
    tooltip                           : {
        show                          : false
    }
      });
        
var roundChartWarning                 = 10;

function updateChartWarning() { //  create a loop function
          setTimeout(function() { //  call a 2s setTimeout when the loop is called
              chartWarning.load({
                  columns             : [Value.slice(0,roundChartWarning)],
              type                    : 'line',
              });
              roundChartWarning++; //  increment the counter
              if (roundChartWarning < 21) { //  if the counter < 20, call the loop function
                  updateChartWarning(); //  ..  again which will trigger another 
              } //  ..  setTimeout()
              else{
                  roundChartWarning   = 10; // reset counter
                  updateChartWarning();
              }
          }, 1500);
      }

updateChartWarning(); //  start the loop

//// ************** Prediction	 *****************  

 Value                                = [
    'Wert',
201.7443529,
201.9569807,
202.154804,
201.5376642,
202.164203,
202.7688229,
204.7585769,
205.9506103,
205.1222096,
204.642248,
205.4733711,
205.5909015,
207.1733655,
208.5789608,
208.4316581,
207.9697884,
208.0578536,
208.9842139,
210.0496297,
211.009208,
213.0276765,
213.6651535,
213.245145,
213.154868,
213.1285216,
214.3102865,
215.9180191,
216.8667214,
216.9157167,
215.4677116,
215.5375433,
216.5786228,
218.8010701,
219.8828234,
220.158414,
219.3445913,
219.5206826,
220.1585876,
221.4431665,
222.141309,
224.1597776,
223.9525112,
224.7972545,
224.3772461,
224.286969,
224.2606226,
225.4423875,
227.0501202,
227.9988225,
228.0478177,
226.5998126,
null,
null,
null,
null,
null,
null,
null,
null,
null,
null,
]
 
Prediction                            = [
    'Vorhersage',
201.8506668,
201.9520459,
201.911601,
202.116495,
202.6768142,
203.4359755,
204.1528845,
204.6484935,
205.1894032,
205.3558681,
205.6004191,
206.2917694,
207.0496514,
207.5489349,
208.0423253,
208.404495,
208.6986287,
209.2141387,
210.2257163,
211.3471763,
212.1993625,
212.8204102,
213.2442729,
213.5007949,
213.951368,
214.6756833,
215.4278531,
215.8956911,
216.1411424,
216.2732631,
216.6601329,
217.2535542,
218.1916947,
218.9531043,
219.5415163,
219.8130198,
220.1250884,
220.5216674,
221.4847047,
222.540019,
223.3837507,
223.9525112,
224.3763739,
224.6328959,
225.0834691,
225.8077844,
226.5599541,
227.0277921,
227.2732435,
227.4053642,
227.7922339,
228.3856553,
229.3237957,
230.0852053,
230.6736173,
230.9451208,
231.2571894,
231.6537685,
231.9480375,
232.3797888,
]

var xPrediction1                       = ['xPrediction1'];
var dummy                              = ['dummy'];
var d_xPrediction1                     = new Date();
var xLine                              = ['xLine'];

d_xPrediction1.setSeconds(d_xPrediction1.getSeconds() - 60 * 42);

for (var i = 0; i < 60; i++) {
     xPrediction1.push(d_xPrediction1.setSeconds(d_xPrediction1.getSeconds() + 60));
     dummy.push(0);
 }

var xPrediction2                       = ['xPrediction2', xPrediction1.slice(10,11), xPrediction1.slice(10,11)];
xLine.push(0,235);

var chartPrediction                   = c3.generate({
        bindto                        : '#chartPrediction',
          data                        : {
              xs                      : {
            'Wert'                   : 'xPrediction1',
            'Vorhersage'              : 'xPrediction1',
            'dummy'                   : 'xPrediction1',
            'xLine'                   : 'xPrediction2',
        },
              columns                 : [
                  xPrediction1, 
                  xPrediction2, 
                  dummy,
                  Value.slice(0,10), 
                  Prediction.slice(0,20), 
                  xLine
              ],      
        type                          : 'line',
        regions                       : { 'Vorhersage': [{'start':xPrediction1.slice(10,11), 'style':'dashed'}]},
        line                          : {
        connect_null                  : false
    },
    },
        point                         : {
  show                                : false
},
    legend                            : {
        position                      : 'right',
        hide                          : ['xLine', 'dummy']
    },
          color                       : {
              pattern                 : ['#682321', '#193441', "red"]
          },
          axis                        : {
              x                       : {
                  type                : 'timeseries',
                                    tick                : {
                    format          : '%H:%M', // format string is also available for timeseries data
                    culling         : {
                        max         :  4 // the number of tick texts will be adjusted to less than this value
                }
              }
              },
              y                       : {
                  min                 : 200,
              }
          },
    tooltip                           : {
        show                          : false
    }
});

var roundChartPrediction = 10;

function updateChartPrediction() { //  create a loop function
          setTimeout(function() { //  call a 2s setTimeout when the loop is called
              xPrediction2                       = ['xPrediction2', 
                                                    xPrediction1.slice(roundChartPrediction,roundChartPrediction+1),
                                                    xPrediction1.slice(roundChartPrediction,roundChartPrediction+1)];
              chartPrediction.internal.config.data_regions.Vorhersage[0].start = xPrediction1.slice(roundChartPrediction,roundChartPrediction+1);
              chartPrediction.load({
                  columns             : [
                        xPrediction1, 
                        xPrediction2, 
                        dummy,
                        Value.slice(0,roundChartPrediction+1), 
                        Prediction.slice(0,roundChartPrediction + 10), 
                        xLine],
              type                    : 'line',
              });
              roundChartPrediction++; //  increment the counter
              if (roundChartPrediction < 50) { //  if the counter < 20, call the loop function
                  updateChartPrediction(); //  ..  again which will trigger another 
              } //  ..  setTimeout()
              else{
                  roundChartPrediction   = 10; // reset counter
                  updateChartPrediction();
              }
          }, 1000);
      }

updateChartPrediction(); //  start the loop

