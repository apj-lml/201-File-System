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


          myrate();
          sameAsPermanent();

          // employment_status();


      })
      
    
          
      document.getElementById("same_as_permanent").addEventListener("change", function(e){
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
          //alert(citizenship)
          if(citizenship == 'Filipino'){
              document.getElementById('dual_citizenship').disabled = true;
              document.getElementById('indicate_country').disabled = true;
          }else{
              document.getElementById('dual_citizenship').removeAttribute('disabled');
              document.getElementById('indicate_country').removeAttribute('disabled');	
          }
      });



      function employment_status(){
        var emp_stauts = document.getElementById("employment_status").value;

        var d_rate = document.getElementById("daily_rate");
        var m_rate = document.getElementById("monthly_rate");
        var step = document.getElementById("step");
        var item_no = document.getElementById("item_no");
        //var date_of_last_step_increment = document.getElementById("date_of_last_step_increment");
      
        m_rate.readOnly = false;
        d_rate.readOnly = false;
        step.disabled = false;
        item_no.readOnly = false;
        //date_of_last_step_increment.disabled = false;

        m_rate.value = "N/A";
        d_rate.value = "N/A";
        step.value = "";
        item_no.value = "N/A";
        //date_of_last_step_increment.value = "";

        if(emp_stauts == "JOB ORDER" || emp_stauts == "CASUAL"){
          m_rate.readOnly = true;
          //parseFloat('100,000.00'.replace(/,/g, ''))
          step.disabled = true;
          item_no.readOnly = true;
          //date_of_last_step_increment.disabled = true;
        }
        else{
          m_rate.value = ""
          d_rate.readOnly = true;
        }

        // myrate()
      }
      function myrate(){
        // alert(123)
        var sg = document.getElementById('salary_grade').value
        var step = document.getElementById("step").value;
        var monthly_rate =  document.getElementById('monthly_rate');
        var daily_rate =  document.getElementById('daily_rate');

        if (document.getElementById('employment_status').value == "PERMANENT" || document.getElementById('employment_status').value == "COTERMINOUS" ){
          monthly_rate.value = monthly_salary[sg][step]
          var temp_m_rate = parseFloat(monthly_rate.value.replace(/,/g, ''));
          monthly_rate.value = temp_m_rate.toLocaleString('en-US')
          daily_rate.value = "N/A"
        }else if (document.getElementById('employment_status').value == "JOB ORDER" || document.getElementById('employment_status').value == "CASUAL" ){
          daily_rate.value = daily_salary[sg]
          var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
          daily_rate.value = temp_m_rate.toLocaleString('en-US')
          monthly_rate.value = "N/A"
        }
    
        // if(emp_stauts == "JOB ORDER" || emp_stauts == "CASUAL"){
        //   //parseFloat('100,000.00'.replace(/,/g, ''))
        //   var temp_m_rate = parseFloat(d_rate.value.replace(/,/g, '')) * 22;
        //   m_rate.value = temp_m_rate.toLocaleString('en-US')
        // }else if (emp_stauts == "PERMANENT" || "COTERMINOUS"){
        //   var temp_d_rate = parseFloat(m_rate.value.replace(/,/g, '')) / 22;
        //   d_rate.value = temp_d_rate.toLocaleString('en-US')
        // }
      }

    document.getElementById("employment_status").addEventListener("change", employment_status);


    document.getElementById("salary_grade").addEventListener("change", myrate);
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




    // document.getElementById('e_highest_level').addEventListener('change',(e)=>{
    //   //console.log(e.target.value)
    //   if(e.target.value == 'GRADUATED'){
    //     document.getElementById('e_highest_grade_year_units').disabled = true;
    //     document.getElementById('e_scholarship_academic_honor').readOnly = false;
    //     document.getElementById('e_period_of_attendance_from').value = ""

    //     document.getElementById('e_period_of_attendance_to').value = ""
    //     document.getElementById('e_period_of_attendance_to').readOnly = false

    //   }else if(e.target.value == "CURRENTLY ENROLLED"){
    //     document.getElementById('e_highest_grade_year_units').disabled = true;
    //     document.getElementById('e_scholarship_academic_honor').readOnly = true;
    //     document.getElementById('e_period_of_attendance_to').readOnly = true;
    //     document.getElementById('e_period_of_attendance_to').value = "PRESENT"
    //     document.getElementById('e_period_of_attendance_from').value = ""

    //   }else{
    //     document.getElementById('e_period_of_attendance_to').readOnly = false;
    //     document.getElementById('e_period_of_attendance_to').value = ""
    //     document.getElementById('e_period_of_attendance_from').value = ""

    //     document.getElementById('e_highest_grade_year_units').disabled = false;
    //     document.getElementById('e_scholarship_academic_honor').readOnly = true;
    //   }
    // });

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

    // document.getElementById('c_highest_level_units_earned').addEventListener('change',(e)=>{
    //   // console.log(e.target.value)
    //   if(e.target.value == 'GRADUATED'){
    //     document.getElementById('c_highest_grade_year_units').disabled = true;
    //     document.getElementById('c_scholarship_academic_honor').readOnly = false;
    //     document.getElementById('c_period_of_attendance_from').value = ""

    //     document.getElementById('c_period_of_attendance_to').value = ""
    //     document.getElementById('c_period_of_attendance_to').readOnly = false

    //   }else if(e.target.value == "CURRENTLY ENROLLED"){
    //     document.getElementById('c_highest_grade_year_units').disabled = true;
    //     document.getElementById('c_scholarship_academic_honor').readOnly = true;
    //     document.getElementById('c_period_of_attendance_to').readOnly = true;
    //     document.getElementById('c_period_of_attendance_to').value = "PRESENT"
    //     document.getElementById('c_period_of_attendance_from').value = ""

    //   }else{
    //     document.getElementById('c_period_of_attendance_to').readOnly = false;
    //     document.getElementById('c_period_of_attendance_to').value = ""
    //     document.getElementById('c_period_of_attendance_from').value = ""

    //     document.getElementById('c_highest_grade_year_units').disabled = false;
    //     document.getElementById('c_scholarship_academic_honor').readOnly = true;
    //   }
    // });

    // document.getElementById('gs_highest_level_units_earned').addEventListener('change',(e)=>{
    //   // console.log(e.target.value)
    //   if(e.target.value == 'GRADUATED'){
    //     document.getElementById('gs_highest_grade_year_units').disabled = true;
    //     document.getElementById('gs_scholarship_academic_honor').readOnly = false;
    //     document.getElementById('gs_period_of_attendance_from').value = ""

    //     document.getElementById('gs_period_of_attendance_to').value = ""
    //     document.getElementById('gs_period_of_attendance_to').readOnly = false

    //   }else if(e.target.value == "CURRENTLY ENROLLED"){
    //     document.getElementById('gs_highest_grade_year_units').disabled = true;
    //     document.getElementById('gs_scholarship_academic_honor').readOnly = true;
    //     document.getElementById('gs_period_of_attendance_to').readOnly = true;
    //     document.getElementById('gs_period_of_attendance_to').value = "PRESENT"
    //     document.getElementById('gs_period_of_attendance_from').value = ""

    //   }else{
    //     document.getElementById('gs_period_of_attendance_to').readOnly = false;
    //     document.getElementById('gs_period_of_attendance_to').value = ""
    //     document.getElementById('gs_period_of_attendance_from').value = ""

    //     document.getElementById('gs_highest_grade_year_units').disabled = false;
    //     document.getElementById('gs_scholarship_academic_honor').readOnly = true;
    //   }
    // });

    // document.getElementById('doc_highest_level_units_earned').addEventListener('change',(e)=>{
    //   // console.log(e.target.value)
    //   if(e.target.value == 'GRADUATED'){
    //     document.getElementById('doc_highest_grade_year_units').disabled = true;
    //     document.getElementById('doc_scholarship_academic_honor').readOnly = false;
    //     document.getElementById('doc_period_of_attendance_from').value = ""

    //     document.getElementById('doc_period_of_attendance_to').value = ""
    //     document.getElementById('doc_period_of_attendance_to').readOnly = false

    //   }else if(e.target.value == "CURRENTLY ENROLLED"){
    //     document.getElementById('doc_highest_grade_year_units').disabled = true;
    //     document.getElementById('doc_scholarship_academic_honor').readOnly = true;
    //     document.getElementById('doc_period_of_attendance_to').readOnly = true;
    //     document.getElementById('doc_period_of_attendance_to').value = "PRESENT"
    //     document.getElementById('doc_period_of_attendance_from').value = ""

    //   }else{
    //     document.getElementById('doc_period_of_attendance_to').readOnly = false;
    //     document.getElementById('doc_period_of_attendance_to').value = ""
    //     document.getElementById('doc_period_of_attendance_from').value = ""

    //     document.getElementById('doc_highest_grade_year_units').disabled = false;
    //     document.getElementById('doc_scholarship_academic_honor').readOnly = true;
    //   }
    // });


  })()