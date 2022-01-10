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
/* -------------------------------------------------------------------------- */
/*                               currency input                               */
/* -------------------------------------------------------------------------- */
      // var currencyInput = document.querySelector('input[type="currency"]')
      // var currency = 'PHP' 

      // onBlur({target:currencyInput})

      // currencyInput.addEventListener('focus', onFocus)
      // currencyInput.addEventListener('blur', onBlur)

      // function localStringToNumber( s ){
      //   return Number(String(s).replace(/[^0-9.-]+/g,""))
      // }

      // function onFocus(e){
      //   console.log(currencyInput);
      //   var value = e.target.value;
      //   e.target.value = value ? localStringToNumber(value) : ''
      // }

      // function onBlur(e){
      //   var value = e.target.value

      //   var options = {
      //       maximumFractionDigits : 2,
      //       currency              : currency,
      //       style                 : "currency",
      //       currencyDisplay       : "symbol"
      //   }
        
      //   e.target.value = (value || value === 0) 
      //     ? localStringToNumber(value).toLocaleString(undefined, options)
      //     : ''
      // }
/* -------------------------------------------------------------------------- */
/*                            end of currency input                           */
/* -------------------------------------------------------------------------- */
      function myrate(){
        var emp_stauts = document.getElementById("employment_status").value;

        var d_rate = document.getElementById("daily_rate");
        var m_rate = document.getElementById("monthly_rate");
        var step = document.getElementById("step");
        var item_no = document.getElementById("item_no");
        var date_of_last_step_increment = document.getElementById("date_of_last_step_increment");
      
        m_rate.disabled = false;
        d_rate.disabled = false;
        step.disabled = false;
        item_no.disabled = false;
        date_of_last_step_increment.disabled = false;
      
        if(emp_stauts == "Job Order" || emp_stauts == "Casual"){
          m_rate.disabled = true;
          //parseFloat('100,000.00'.replace(/,/g, ''))
          var temp_m_rate = parseFloat(d_rate.value.replace(/,/g, '')) * 22;
          m_rate.value = temp_m_rate.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
          step.disabled = true;
          item_no.disabled = true;
          date_of_last_step_increment.disabled = true;
        }
        else{
          m_rate.value = ""
          d_rate.disabled = true;
        }
      }

    document.getElementById("employment_status").addEventListener("change", myrate);


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