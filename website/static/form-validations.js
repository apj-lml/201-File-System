// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

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

        if(emp_status == "JOB ORDER" || emp_status == "CONTRACT OF SERVICE"){

          step.value = "";
          d_rate.readOnly = true;

          m_rate.disabled = true;
          step.disabled = true;
          sg.disabled = false;
          //sg.value = "1";
          job_grade.disabled = true;
          job_grade.value = "";
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
          // sg.value = "N/A";
          sg.disabled = false;
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

        var first_day_in_service = document.getElementById('first_day_in_service');
        var date_of_assumption = document.getElementById('date_of_assumption');

        if(emp_status.value == "PERMANENT" || emp_status.value == "TEMPORARY" || emp_status.value == "COTERMINOUS"){
          dolp.readOnly = false;
          first_day_in_service.readOnly = false;
          date_of_assumption.readOnly = false;
        }else{
          dolp.readOnly = true;
          first_day_in_service.readOnly = true;
          date_of_assumption.readOnly = true;
        }

      }

      function myrate(){
        var sg = document.getElementById('salary_grade').value;
        var step = document.getElementById("step").value;
        var monthly_rate =  document.getElementById('monthly_rate');
        var daily_rate =  document.getElementById('daily_rate');
        var emp_status = document.getElementById('employment_status').value;
        var job_grade = document.getElementById('job_grade').value;
        var salary_grade = document.getElementById('salary_grade').value;

        if(sg == ''){
          sg = 1;
        }
        if(step == ''){
          step = 1;
        }
        if(job_grade == ''){
          job_grade = 2;
        }

        if (emp_status == "PERMANENT" || emp_status == "COTERMINOUS" || emp_status == "TEMPORARY"){
          monthly_rate.value = job_grade_monthly_salary[salary_grade][step];
          var temp_m_rate = parseFloat(monthly_rate.value.replace(/,/g, ''));
          monthly_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          daily_rate.value = "N/A";
          // salary_grade.value = "";
          disableStepCasual(false);

        }else if (emp_status == "JOB ORDER" || emp_status == "CONTRACT OF SERVICE"){

          daily_rate.value = daily_salary[sg];
          var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
          daily_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          monthly_rate.value = "N/A";
          disableStepCasual(false);

        }else if (emp_status == "CASUAL"){

          daily_rate.value = casual_job_grade_daily_salary[job_grade][step];
          var temp_m_rate = parseFloat(daily_rate.value.replace(/,/g, ''));
          daily_rate.value = temp_m_rate.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
          daily_rate.value = casual_job_grade_daily_salary[job_grade][step];
          monthly_rate.value = "N/A";


          disableStepCasual(true);

        }


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

    // document.getElementById("section").addEventListener("change", (e)=>{
    //   console.log(e.target.value)
    //   var units = `<option class='' value='' selected disabled hidden>-</option>`;
    //   document.getElementById("unit").innerHTML = units;
    //   if(e.target.value == "Administrative & Finance"){
    //     units = `
    //       <option value="Administrative Unit">Administrative Unit</option>
    //       <option value="Finance Unit">Finance Unit</option>
    //       <option value="Cashiering Unit">Cashiering Unit</option>
    //       <option value="Property Unit">Property Unit</option>
    //       <option value="N/A">N/A</option>
    //     `;
    //   }
    //   else if(e.target.value == "Engineering"){
    //     units = `
    //       <option value="Planning Unit">Planning Unit</option>
    //       <option value="Design Unit">Design Unit</option>
    //       <option value="Construction Unit">Construction Unit</option>
    //       <option value="Institutional Development Unit">Institutional Development Unit</option>
    //       <option value="Equipment Unit">Equipment Unit</option>
    //       <option value="N/A">N/A</option>
    //     `;
    //   }
    //   else if(e.target.value == "Operation & Maintenance"){
    //     units = `
    //       <option value="Agno-Sinocalan RIS">Agno-Sinocalan RIS</option>
    //       <option value="San Fabian-Dumoloc RIS">San Fabian-Dumoloc RIS</option>
    //       <option value="Lower Agno RIS">Lower Agno RIS</option>
    //       <option value="Ambayoan-Dipalo RIS">Ambayoan-Dipalo RIS</option>
    //       <option value="N/A">N/A</option>
    //     `;
    //   }
    //   else{
    //     units = `
    //       <option value="N/A">N/A</option>
    //       `;
    //   }
    //   document.getElementById("unit").insertAdjacentHTML("afterbegin", units);
    // });

    //HIGH SCHOOL

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