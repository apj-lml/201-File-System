// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
    var monthly_salary = {
      1:{1:11068, 2:11160, 3:11254, 4:11348, 5:11443, 6:11538, 7:11635, 8:11732},
      2:{1:11761, 2:11851, 3:11942, 4:12034, 5:12126, 6:12219, 7:12313, 8:12407},
      3:{1:12466, 2:12562, 3:12656, 4:12756, 5:12854, 6:12952, 7:13052, 8:13152},
      4:{1:13214, 2:13316, 3:13418, 4:13521, 5:13625, 6:13729, 7:13835, 8:13491},
      5:{1:14007, 2:14115, 3:14223, 4:14332, 5:14442, 6:14553, 7:14665, 8:14777},
      6:{1:14847, 2:14961, 3:15076, 4:15192, 5:15309, 6:15426, 7:15545, 8:15664},
      7:{1:15738, 2:15859, 3:15981, 4:16104, 5:16227, 6:16352, 7:16447, 8:16604},
      8:{1:16758, 2:16910, 3:17063, 4:17217, 5:17372, 6:17529, 7:17688, 8:17848},
      9:{1:17975, 2:18125, 3:18277, 4:18430, 5:18584, 6:18739, 7:18896, 8:19054},
      10:{1:19233, 2:19394, 3:19556, 4:19720, 5:19884, 6:20051, 7:20218, 8:20387},
      11:{1:20754, 2:21038, 3:21327, 4:21610, 5:21915, 6:22216, 7:22520, 8:22829},
      12:{1:22938, 2:23222, 3:23510, 4:23801, 5:24096, 6:24395, 7:24697, 8:25003},
      13:{1:25232, 2:25545, 3:25861, 4:26181, 5:26506, 6:26834, 7:27166, 8:27503},
      14:{1:27755, 2:28099, 3:28447, 4:28800, 5:29156, 6:29517, 7:29883, 8:30253},
      15:{1:30531, 2:30909, 3:31292, 4:31680, 5:32072, 6:32469, 7:32871, 8:33279},
      16:{1:33584, 2:34000, 3:34421, 4:34847, 5:35279, 6:35716, 7:36159, 8:36606},
      17:{1:36942, 2:37400, 3:37863, 4:38332, 5:38807, 6:39228, 7:39774, 8:40267},
      18:{1:40637, 2:41140, 3:41650, 4:42165, 5:42688, 6:43217, 7:43752, 8:44294},
      19:{1:45269, 2:46008, 3:46759, 4:47522, 5:48298, 6:49086, 7:49888, 8:50702},
      20:{1:51155, 2:51989, 3:52838, 4:53700, 5:54577, 6:55468, 7:56373, 8:57293},
      21:{1:57805, 2:58748, 3:59707, 4:60681, 5:61672, 6:62678, 7:63701, 8:64741},
      22:{1:65319, 2:66385, 3:67469, 4:68570, 5:69689, 6:70827, 7:71983, 8:73157},
      23:{1:73811, 2:75015, 3:76240, 4:77484, 5:78749, 6:80034, 7:81340, 8:82668},
      24:{1:83406, 2:84767, 3:86151, 4:87557, 5:88986, 6:90439, 7:91915, 8:93415},
      25:{1:95083, 2:96635, 3:98212, 4:99815, 5:101444, 6:103100, 7:1047783, 8:106493}
  }
      var daily_salary = {
        1:503.09,
        2:534.59,
        3:566.63,
        4:600.63,
        5:636.68,
        6:674.86,
        7:715.36,
        8:761.72,
        9:817.04,
        10:874.22,
        11:943.36,
        12:1042.63,
        13:1146.90,
        14:1261.59,
        15:1387.77,
        16:1526.54
      }

      var job_grade_monthly_salary = {
        2:{1:"13000.00",	2:13111,	3:13223,	4:13334,	5:13446,	6:13557,	7:13669,	8:13780},
        3:{1:13819.00,	2:13927,	3:14036,	4:14144,	5:14253,	6:14361,	7:14470,	8:14578},
        4:{1:14678.00,	2:14793,	3:14909,	4:15024,	5:15140,	6:15255,	7:15371,	8:15486},
        5:{1:15586.00,	2:16166,	3:16745,	4:17325,	5:17905,	6:18485,	7:19064,	8:19644},
        6:{1:19744.00,	2:19928,	3:20111,	4:20295,	5:20478,	6:20662,	7:20845,	8:21029},
        7:{1:21129.00,	2:21620,	3:22111,	4:22602,	5:23094,	6:23585,	7:24076,	8:24567},
        8:{1:27000.00,	2:27604,	3:28209,	4:28813,	5:29417,	6:30021,	7:30626,	8:31230},
        9:{1:31320.00,	2:32037,	3:32755,	4:33472,	5:34189,	6:34906,	7:35624,	8:36341},
        10:{1:36619.00,	2:38010,	3:39401,	4:40792,	5:42182,	6:43573,	7:44964,	8:46355},
        11:{1:46725.00,	2:51386,	3:56046,	4:60707,	5:65367,	6:70028,	7:74688,	8:79349},
        12:{1:80003.00,	2:82987,	3:85970,	4:88954,	5:91937,	6:94921,	7:97904,	8:100888},
        13:{1:102690.00,	2:106586,	3:110486,	4:114379,	5:118275,	6:122171,	7:126068,	8:129964},
        14:{1:131124.00,	2:133372,	3:135620,	4:137868,	5:140115,	6:142363,	7:144611,	8:146859},
        15:{1:148171.00,	2:150711,	3:153251,	4:155791,	5:158331,	6:160871,	7:163411,	8:165951},
        16:{1:167432.00,	2:170302,	3:173173,	4:176043,	5:178914,	6:181784,	7:184655,	8:187525},
        17:{1:189199.00,	2:192442,	3:195686,	4:198929,	5:202172,	6:205415,	7:208659,	8:211902},
        18:{1:278434.00,	2:284201,	3:289969,	4:295736,	5:301504,	6:307271,	7:313039,	8:318806},
        19:{1:331954.00,	2:339067,	3:346181,	4:353294,	5:360408,	6:367521,	7:374635,	8:381748},
        20:{1:419144.00,	2:422737,	3:426329,	4:429922,	5:433514,	6:437107,	7:440699,	8:444292}
      }

      var casual_job_grade_daily_salary = {
        2:{1:"590.90",	2:595.95},
        3:{1:628.13,	2:633.04},
        4:{1:667.18,	2:"672.40"},
        5:{1:708.45,	2:734.81},
        6:{1:897.45,	2:905.81},
        7:{1:"960.40",	2:982.72},
        8:{1:1227.27,	2:1254.72},
        9:{1:1423.63,	2:1456.22},
        10:{1:"1664.50",	2:1727.72},
        11:{1:2123.86,	2:2335.72},
        12:{1:"3636.50",	2:3772.13},
        13:{1:4667.72,	2:4844.81}
      }

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })

      window.addEventListener('load', function() {

        
        //code to restrict max date of birthdate
          var dtToday = new Date();
      
          var month = dtToday.getMonth() + 1;
          var day = dtToday.getDate();
          var year = dtToday.getFullYear();
      
          if(month < 10)
              month = '0' + month.toString();
          if(day < 10)
              day = '0' + day.toString();
      
          var maxDate = year + '-' + month + '-' + day;
          document.getElementById('birthdate').max = maxDate;


          // myrate();
          sameAsPermanent();

          employment_status();
          date_of_last_promotion();

        var emp_status = document.getElementById("employment_status").value;
          
          if(emp_status == "CASUAL"){
            // var sg = document.getElementById('salary_grade');
            // var job_grade = document.getElementById('job_grade');
            disableStepCasual(true)
          }

      })
      
    
          
      document.getElementById("same_as_permanent_address").addEventListener("change", function(e){
          sameAsPermanent();
      });
      
      
      document.getElementById("birthdate").addEventListener('change',()=>{
        var dob = new Date(document.getElementById("birthdate").value);
        var diff_ms = Date.now() - dob.getTime();
          var age_dt = new Date(diff_ms); 
        
          var age = Math.abs(age_dt.getUTCFullYear() - 1970);
          document.getElementById("age").value = age;
      });
      
      
      document.getElementById("citizenship").addEventListener("change", function(e){
          var citizenship = document.getElementById('citizenship').value;
          if(citizenship == 'Filipino'){
              document.getElementById('dual_citizenship').disabled = true;
              document.getElementById('indicate_country').disabled = true;
          }else{
              document.getElementById('dual_citizenship').removeAttribute('disabled');
              document.getElementById('indicate_country').removeAttribute('disabled');	
          }
      });



      function employment_status(){

        var emp_status = document.getElementById("employment_status").value;

        var d_rate = document.getElementById("daily_rate");
        var m_rate = document.getElementById("monthly_rate");
        var step = document.getElementById("step");
        var sg = document.getElementById('salary_grade');
        var job_grade = document.getElementById('job_grade');

      
        step.disabled = false;

        m_rate.value = "N/A";
        d_rate.value = "N/A";

        if(emp_status == "JOB ORDER"){

          step.value = "";
          d_rate.readOnly = true;

          m_rate.disabled = true;
          step.disabled = true;
          sg.disabled = false;
          //sg.value = "1";
          job_grade.disabled = true;
          //job_grade.value = "";
          // disableSgJobOrder(true);


        }else if(emp_status == "CASUAL"){

          m_rate.disabled = true;
          // step.value = "1";
          sg.disabled = true;
          sg.value = null;
          job_grade.disabled = false;
          //job_grade.value = "";
          disableStepCasual(true);

        }
        
        else{

          m_rate.value = "";
          d_rate.readOnly = true;
          sg.value = "N/A";
          sg.disabled = true;
          job_grade.disabled = false;
          // job_grade.value = "2";
          // step.value = "1";
        }
        date_of_last_promotion();
        myrate()
      }

      
      function date_of_last_promotion(){
        var dolp = document.getElementById('date_of_last_promotion');
        var emp_status = document.getElementById("employment_status");
        // dolp.readOnly = isReadOnly;

        if(emp_status.value == "PERMANENT"){
          dolp.readOnly = false;

        }else{
          dolp.readOnly = true;

        }

      }

      function myrate(){
        var sg = document.getElementById('salary_grade').value;
        var step = document.getElementById("step").value;
        var monthly_rate =  document.getElementById('monthly_rate');
        var daily_rate =  document.getElementById('daily_rate');
        var emp_status = document.getElementById('employment_status').value;
        var job_grade = document.getElementById('job_grade').value;

        if (emp_status == "PERMANENT" || emp_status == "COTERMINOUS"){

          monthly_rate.value = job_grade_monthly_salary[job_grade][step];
          var temp_m_rate = parseFloat(monthly_rate.value.replace(/,/g, ''));
          monthly_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          daily_rate.value = "N/A";
          document.getElementById('salary_grade').value = "";;
          disableStepCasual(false);

        }else if (emp_status == "JOB ORDER"){
          daily_rate.value = daily_salary[sg];
          var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
          daily_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          monthly_rate.value = "N/A";
          disableStepCasual(false);

        }else if (emp_status == "CASUAL"){
          daily_rate.value = casual_job_grade_daily_salary[job_grade][step];
          var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
          daily_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          monthly_rate.value = "N/A";
        }

        document.getElementsByName('daily_rate')[0].value = document.getElementById('daily_rate').value;
        document.getElementsByName('monthly_rate')[0].value = document.getElementById('monthly_rate').value;

        document.getElementsByName('job_grade')[0].value = document.getElementById('job_grade').value;
        document.getElementsByName('salary_grade')[0].value = document.getElementById('salary_grade').value;
        document.getElementsByName('step')[0].value = document.getElementById('step').value;


        /* -------------------------------------------------------------------------- */
        /*                                  OLD CODE                                  */
        /* -------------------------------------------------------------------------- */

        // if (emp_status == "PERMANENT" || emp_status == "COTERMINOUS" ){
        //   monthly_rate.value = monthly_salary[sg][step]
        //   var temp_m_rate = parseFloat(monthly_rate.value.replace(/,/g, ''));
        //   monthly_rate.value = temp_m_rate.toLocaleString('en-US')
        //   daily_rate.value = "N/A"
        // }else if (emp_status == "JOB ORDER" || emp_status == "CASUAL" ){
        //   daily_rate.value = daily_salary[sg]
        //   var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
        //   daily_rate.value = temp_m_rate.toLocaleString('en-US')
        //   monthly_rate.value = "N/A"
        // }
      }
      function disableSgJobOrder(isDisabled){
          var sg = document.getElementById("salary_grade").getElementsByTagName("option");
          for (var i = 17; i < sg.length; i++) { 
          //   if ( i==5 || i==17 || i==4) {
              sg[i].disabled = isDisabled;
            }
      }

      function disableStepCasual(isDisabled){
        var op = document.getElementById("step").getElementsByTagName("option");
        for (var i = 3; i < op.length; i++) { 
            op[i].disabled = isDisabled;
          }

        var jg = document.getElementById("job_grade").getElementsByTagName("option");
          for (var j = 13; j < jg.length; j++) { 
              jg[j].disabled = isDisabled;
            }
      }
    document.getElementById("employment_status").addEventListener("change", employment_status);


    document.getElementById("salary_grade").addEventListener("change", myrate);
    document.getElementById("job_grade").addEventListener("change", myrate);
    document.getElementById("step").addEventListener("change", myrate);

    // window.addEventListener("load", ()=>{

    // });

    document.getElementById("section").addEventListener("change", (e)=>{
      console.log(e.target.value)
      var units = `<option class='' value='' selected disabled hidden>-</option>`;
      document.getElementById("unit").innerHTML = units;
      if(e.target.value == "Administrative & Finance"){
        units = `
          <option value="Administrative Unit">Administrative Unit</option>
          <option value="Finance Unit">Finance Unit</option>
          <option value="Cashiering Unit">Cashiering Unit</option>
          <option value="Property Unit">Property Unit</option>
          <option value="N/A">N/A</option>
        `;
      }
      else if(e.target.value == "Engineering"){
        units = `
          <option value="Planning Unit">Planning Unit</option>
          <option value="Design Unit">Design Unit</option>
          <option value="Construction Unit">Construction Unit</option>
          <option value="Institutional Development Unit">Institutional Development Unit</option>
          <option value="Equipment Unit">Equipment Unit</option>
          <option value="N/A">N/A</option>
        `;
      }
      else if(e.target.value == "Operation & Maintenance"){
        units = `
          <option value="Agno-Sinocalan RIS">Agno-Sinocalan RIS</option>
          <option value="San Fabian-Dumoloc RIS">San Fabian-Dumoloc RIS</option>
          <option value="Lower Agno RIS">Lower Agno RIS</option>
          <option value="Ambayoan-Dipalo RIS">Ambayoan-Dipalo RIS</option>
          <option value="N/A">N/A</option>
        `;
      }
      else{
        units = `
          <option value="N/A">N/A</option>
          `;
      }
      document.getElementById("unit").insertAdjacentHTML("afterbegin", units);
    });



    document.getElementById('hs_highest_level').addEventListener('change',(e)=>{
      // console.log(e.target.value)
      if(e.target.value == 'GRADUATED'){
        document.getElementById('hs_highest_grade_year_units').disabled = true;
        document.getElementById('hs_scholarship_academic_honor').readOnly = false;
        document.getElementById('hs_period_of_attendance_from').value = ""

        document.getElementById('hs_period_of_attendance_to').value = ""
        document.getElementById('hs_period_of_attendance_to').readOnly = false

      }else if(e.target.value == "CURRENTLY ENROLLED"){
        document.getElementById('hs_highest_grade_year_units').disabled = true;
        document.getElementById('hs_scholarship_academic_honor').readOnly = true;
        document.getElementById('hs_period_of_attendance_to').readOnly = true;
        document.getElementById('hs_period_of_attendance_to').value = "PRESENT"
        document.getElementById('hs_period_of_attendance_from').value = ""

      }else{
        document.getElementById('hs_period_of_attendance_to').readOnly = false;
        document.getElementById('hs_period_of_attendance_to').value = ""
        document.getElementById('hs_period_of_attendance_from').value = ""

        document.getElementById('hs_highest_grade_year_units').disabled = false;
        document.getElementById('hs_scholarship_academic_honor').readOnly = true;
      }
    });

    
  })()