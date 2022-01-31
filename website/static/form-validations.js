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


          activate_booster_shot();
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
      function activate_booster_shot(){
        var booster_id_no = document.getElementById('booster_id_no');
        var booster_brand = document.getElementById('booster_brand');
        var booster_place = document.getElementById('booster_place');
        var booster_date = document.getElementById('booster_date');
        var booster_shot = document.getElementById('do_you_have_booster');

        if (booster_shot.value == "YES"){
          booster_id_no.disabled = false;
          booster_brand.disabled = false;
          booster_place.disabled = false;
          booster_date.disabled = false;
        }else{
          booster_id_no.disabled = true;
          booster_brand.disabled = true;
          booster_place.disabled = true;
          booster_date.disabled = true;

          booster_id_no.value = "";
          booster_brand.value = "";
          booster_place.value = "";
          booster_date.value = "";
        
          }
        }
      document.getElementById('do_you_have_booster').addEventListener('change', activate_booster_shot);

      function employment_status(){
        var emp_stauts = document.getElementById("employment_status").value;

        var d_rate = document.getElementById("daily_rate");
        var m_rate = document.getElementById("monthly_rate");
        var step = document.getElementById("step");
        var item_no = document.getElementById("item_no");
        //var date_of_last_step_increment = document.getElementById("date_of_last_step_increment");
      
        m_rate.disabled = false;
        d_rate.disabled = false;
        step.disabled = false;
        item_no.disabled = false;
        //date_of_last_step_increment.disabled = false;

        m_rate.value = "";
        d_rate.value = "";
        step.value = "";
        item_no.value = "";
        //date_of_last_step_increment.value = "";

        if(emp_stauts == "Job Order" || emp_stauts == "Casual"){
          m_rate.disabled = true;
          //parseFloat('100,000.00'.replace(/,/g, ''))
          step.disabled = true;
          item_no.disabled = true;
          //date_of_last_step_increment.disabled = true;
        }
        else{
          m_rate.value = ""
          d_rate.disabled = true;
        }

        // myrate()
      }
      function myrate(){

        var d_rate = document.getElementById("daily_rate");
        var m_rate = document.getElementById("monthly_rate");
        var emp_stauts = document.getElementById("employment_status").value;

        if(emp_stauts == "Job Order" || emp_stauts == "Casual"){
          //parseFloat('100,000.00'.replace(/,/g, ''))
          var temp_m_rate = parseFloat(d_rate.value.replace(/,/g, '')) * 22;
          m_rate.value = temp_m_rate.toLocaleString('en-US')
        }else if (emp_stauts == "Permanent" || "Cotermenous"){
          var temp_d_rate = parseFloat(m_rate.value.replace(/,/g, '')) / 22;
          d_rate.value = temp_d_rate.toLocaleString('en-US')
        }
      }

    document.getElementById("employment_status").addEventListener("change", employment_status);


    document.getElementById("daily_rate").addEventListener("keyup", myrate);


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

  })()