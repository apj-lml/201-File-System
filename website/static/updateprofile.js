
/* -------------------------------------------------------------------------- */
/*                               code for submit                              */
/* -------------------------------------------------------------------------- */
// document.getElementById("signUp").addEventListener("submit", function(e){
//     e.preventDefault()
//     var file_input = document.getElementById('psa');
  
//     if(file_input.files.length == 0){
//         alert("No file selected")
//     }
  
//     var formElem = document.getElementById("signUp");
//     let formData = new FormData(formElem);
  
//     const data = {}
//     formData.forEach((value, key) => (data[key] = value))
   
//     console.log(data)
//     fetch('/signup', {
//           method: 'POST',
//           body: formData
//       }).then((res)=>{
//           setTimeout(function() { 
//               triggerToast(); 
//               setTimeout(()=>{
//                   document.getElementById('toastBody').innerHTML = ""
//               },6000)
//           }, 450);
          
//       }).catch(console.error)
//   });
  
  /* -------------------------------------------------------------------------- */
  /*                           code for dynamic fields                          */
  /* -------------------------------------------------------------------------- */
  var cs_no_fields = document.getElementById('cs_no_fields');
  document.getElementById('add_cse_field').addEventListener('click',()=>{
      var cs_fields = document.getElementById('cs_fields');
      cs_fields.innerHTML = ``;
      var x = cs_no_fields.value;
      // for(var x = 1; x < cs_no_fields.value; x++){
          cs_fields.insertAdjacentHTML("beforebegin",`
          <div class="card shadow-sm mb-3" id=remove_cse${x}>
              <div class="card-body">
                  <div class="d-md-flex flex-row">
                  <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" name ="cs_eligibility[${x}]" placeholder="Eligibility" form="add_cse_form">
                  <label for="cs_eligibility" style="font-size: 11.5px;">Career Service / RA 1080 (BOARD/BAR) Under Special Laws / CES / CSEE / Barangay Eligibility / Driver's License</label>
                  </div>
                  <div class="form-floating flex-fill mb-3 p-1">
                      <input type="date" class="form-control" name ="date_of_examination[${x}]" placeholder="Date of Examination" form="add_cse_form">
                      <label for="date_of_examination">Date of Examination</label>
                  </div>
              </div>
              <div class="d-md-flex flex-row">
                  <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" name ="cs_rating[${x}]" placeholder="Rating" form="add_cse_form">
                  <label for="cs_rating">Rating (if applicable)</label>
                  </div>
                  <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" name ="place_of_examination_conferment[${x}]" placeholder="Place of Examination / Conferment" form="add_cse_form">
                  <label for="place_of_examination_conferment">Place of Examination / Conferment</label>
                  </div>
              </div>
              <div class="d-md-flex flex-row">
              <div class="form-floating flex-fill mb-3 p-1 col-md-6">
                  <input type="text" class="form-control" name ="license_no[${x}]" placeholder="License Number" form="add_cse_form">
                  <label for="license_no">License Number</label>
              </div>
              <div class="form-floating flex-fill mb-3 p-1">
                  <input type="date" class="form-control" name ="date_of_validity[${x}]" placeholder="Date of Validity" form="add_cse_form">
                  <label for="date_of_validity">Date of Validity</label>
              </div>
              </div>
          <a href="#" onclick="document.getElementById('cs_no_fields').value--;document.getElementById('remove_cse${x}').remove(); return false">Remove field</a>
          </div>
      </div>
          `);
      // }
  });
  
  document.getElementById('add_vocational_field').addEventListener('click',()=>{
      var vocational_fields = document.getElementById('vocational_fields');
      var vocational_no_fields = document.getElementById('vocational_no_fields');
      vocational_fields.innerHTML = ``;
      //  for(var x = 1; x < vocational_no_fields.value; x++){
          var x = vocational_no_fields.value;
          vocational_fields.insertAdjacentHTML("beforebegin",`
              <div class="card shadow-sm mb-3" id=remove_vocational${x}>
  
                  <div class="card-body">
                      <div class="d-md-flex flex-row">
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="v_school[${x}]" name ="v_school[${x}]" placeholder="School" form="add_vocational_form">
                      <label for="v_school">School</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="vocational_trade_course[${x}]" name ="vocational_trade_course[${x}]" placeholder="Vocational / Trade Course" form="add_vocational_form">
                      <label for="vocational_trade_course">Vocational / Trade Course</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="v_period_of_attendance_from[${x}]" name ="v_period_of_attendance_from[${x}]" placeholder="Period of Attendance (From)" form="add_vocational_form">
                      <label for="v_period_of_attendance_from">Period of Attendance (From)</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="v_period_of_attendance_to[${x}]" name ="v_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" form="add_vocational_form">
                      <label for="v_period_of_attendance_to">Period of Attendance (To)</label>
                      </div>
                  </div>
                  <div class="d-md-flex flex-row">
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="v_highest_level[${x}]" name ="v_highest_level[${x}]" placeholder="Highest Level" form="add_vocational_form">
                      <label for="v_highest_level">Highest Level Attained / Units Earned</label>
                      </div>   
                      <div class="form-floating flex-fill mb-3 p-1">
                      <input type="text" class="form-control" id="v_scholarship_academic_honor[${x}]" name ="v_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" form="add_vocational_form">
                      <label for="v_scholarship_academic_honor">Sholarship / Academic Honor</label>
                      </div>  
                  </div>
                  <a href="#" onclick="document.getElementById('vocational_no_fields').value--;document.getElementById('remove_vocational${x}').remove(); return false">Remove field</a>
                  </div>
              </div>
          `);
      //  }
  });
  
  document.getElementById('add_ld_field').addEventListener('click',()=>{
      var vocational_fields = document.getElementById('ld_fields');
      var vocational_no_fields = document.getElementById('ld_no_fields');
      vocational_fields.innerHTML = ``;
      //  for(var x = 1; x < vocational_no_fields.value; x++){
          var x = vocational_no_fields.value;
          vocational_fields.insertAdjacentHTML("beforebegin",`
          <div class="card shadow-sm mb-3" id=remove_ld${x}>
              <div class="card-body">
                  <div class="d-md-flex flex-row">
                      <div class="form-floating flex-fill mb-3 p-1">
                          <input type="text" class="form-control" name ="ld_program[${x}]" placeholder="Interventions/Training Program" form="add_ld_form">
                          <label for="ld_program">Interventions / Training Program</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                          <input type="date" class="form-control" name ="ld_date_from[${x}]" placeholder="Inclusive Date of Attendance From" form="add_ld_form">
                          <label for="ld_date_from">Inclusive Date of Attendance From</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                          <input type="date" class="form-control" name ="ld_date_to[${x}]" placeholder="Inclusive Date of Attendance To" form="add_ld_form">
                          <label for="ld_date_to">Inclusive Date of Attendance To</label>
                      </div>
                      </div>
                      <div class="d-md-flex flex-row">
                      <div class="form-floating flex-fill mb-3 p-1">
                          <input type="number" class="form-control" name ="ld_no_hours[${x}]" placeholder="Rating" form="add_ld_form">
                          <label for="ld_no_hours">Number of Hours</label>
                      </div>
                      <div class="form-floating flex-fill mb-3 p-1">
                          <input type="text" class="form-control" name ="ld_type[${x}]" placeholder="Type of Learning & Development (Ex. Manegerial, Supervisory, Technical)" form="add_ld_form">
                          <label for="ld_type">Type of Learning & Development (Ex. Manegerial, Supervisory, Technical)</label>
                      </div>
                      </div>
                      <div class="d-md-flex flex-row">
                      <div class="form-floating flex-fill mb-3 p-1 col-md-6">
                          <input type="text" class="form-control" name ="ld_sponsored_by[${x}]" placeholder="Conducted / Sponsored By" form="add_ld_form">
                          <label for="license_no">Conducted / Sponsored By</label>
                      </div>
                  </div>
                  <a href="#" onclick="document.getElementById('ld_no_fields').value--;document.getElementById('remove_ld${x}').remove(); return false">Remove field</a>
              </div>
          </div>
  
          `);
      //  }
  });