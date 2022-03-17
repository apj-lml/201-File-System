
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
          <div class="card shadow-sm mb-3" id="remove_cse${x}">
              <div class="card-body">
                  <div class="d-md-flex flex-row">
                  <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" name ="cs_eligibility[${x}]" placeholder="Eligibility" form="add_cse_form">
                  <label for="cs_eligibility" style="font-size: 11.5px;">Career Service / RA 1080 (BOARD/BAR) Under Special Laws / CES / CSEE / Barangay Eligibility / Driver's License</label>
                  </div>
                  <div class="form-floating flex-fill mb-3 p-1">
                      <input type="date" class="form-control" name ="date_of_examination[${x}]" placeholder="Date of Examination From" form="add_cse_form">
                      <label for="date_of_examination">Date of Examination</label>
                  </div>
                  <div class="form-floating flex-fill mb-3 p-1">
                    <input type="date" class="form-control" name ="date_of_examination_to[${x}]" placeholder="Date of Examination To" value="N/A" form="add_cse_form">
                    <label for="date_of_examination_to">Date of Examination To</label>
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
          <a href="#" onclick="document.getElementById('cs_no_fields').value--;document.getElementById('remove_cse${x}').remove(); return false">Remove</a>
          </div>
      </div>
          `);
      // }
  });
  

  var college_no_fields = document.getElementById('college_no_fields');
  document.getElementById('add_college_field').addEventListener('click',()=>{
      var cs_fields = document.getElementById('college_fields');
      cs_fields.innerHTML = ``;
      var x = college_no_fields.value;
      // for(var x = 1; x < cs_no_fields.value; x++){
          cs_fields.insertAdjacentHTML("beforebegin",`
          <div class="card shadow-sm mb-3" id="remove_college${x}">
            <div class="card-body">
                <div class="d-md-flex flex-row">
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="text" class="form-control" id="add_c_school[${x}]" name ="c_school[${x}]" placeholder="c_school[${x}]" value="" form="add_college_form">
                    <label for="c_school[1]">School</label>
                    </div>
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="text" class="form-control" id="add_c_degree_course[${x}]" name ="c_degree_course[${x}]" placeholder="c_degree_course[${x}]" value="" form="add_college_form">
                    <label for="c_degree_course[1]">Degree</label>
                    </div>
                    <div class="form-floating flex-fill mb-3 p-1">
                    <select class="form-select" id="add_c_highest_level_units_earned[${x}]" name="c_highest_level_units_earned[${x}]" aria-label="Floating label select example" value="" form="add_college_form" onchange="graduated(this, document.getElementById('add_c_highest_grade_year_units[${x}]'), document.getElementById('add_c_scholarship_academic_honor[${x}]'), document.getElementById('add_c_period_of_attendance_from[${x}]'), document.getElementById('add_c_period_of_attendance_to[${x}]'))" required>
                        <option class="" value="" selected>-</option>
                        <option value="GRADUATED">GRADUATED</option>
                        <option value="UNDERGRADUATE">UNDERGRADUATE</option>
                        <option value="CURRENTLY ENROLLED">CURRENTLY ENROLLED</option>
                    </select>
                    <label for="c_highest_level_units_earned[1]">Highest Level Attained</label>
                    </div>

                </div>
                <div class="d-md-flex flex-row">
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="number" class="form-control" id="add_c_period_of_attendance_from[${x}]" name ="c_period_of_attendance_from[${x}]" placeholder="Period of Attendance (From)" value="" form="add_college_form" oninput="year_only(this)">
                    <label for="c_period_of_attendance_from[1]">Period of Attendance (From)</label>
                    </div>
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="number" class="form-control" id="add_c_period_of_attendance_to[${x}]" name ="c_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" value="" form="add_college_form" oninput="year_only(this)">
                    <label for="c_period_of_attendance_to[1]">Period of Attendance (To)</label>
                    </div>
                </div>
                <div class="d-md-flex flex-row">
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="text" class="form-control" id="add_c_highest_grade_year_units[${x}]" name ="c_highest_grade_year_units[${x}]" placeholder="Highest Level" value="" form="add_college_form">
                    <label for="c_highest_grade_year_units[1]">Units Earned</label>
                    </div>   
                    <div class="form-floating flex-fill mb-3 p-1">
                    <input type="text" class="form-control" id="add_c_scholarship_academic_honor[${x}]" name ="c_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" value="" form="add_college_form">
                    <label for="c_scholarship_academic_honor[1]">Scholarship / Academic Honor</label>
                    </div>  
                </div>
                <a href="#" onclick="document.getElementById('college_no_fields').value--;document.getElementById('remove_college${x}').remove(); return false">Remove</a>
            </div>
            </div>
          `);
      // }
  });

  var masteral_no_fields = document.getElementById('masteral_no_fields');
  document.getElementById('add_masteral_field').addEventListener('click',()=>{
      var masteral_fields = document.getElementById('masteral_fields');
      masteral_fields.innerHTML = ``;
      var x = masteral_no_fields.value;
      // for(var x = 1; x < cs_no_fields.value; x++){
        masteral_fields.insertAdjacentHTML("beforebegin",`
          <div class="card shadow-sm mb-3" id="remove_masteral${x}">
          <div class="card-body">

         <div class="d-md-flex flex-row">
           <div class="form-floating flex-fill mb-3 p-1">
             <input type="text" class="form-control" id="add_gs_school[${x}]" name ="gs_school[${x}]" placeholder="School" value="" form="add_masteral_form">
             <label for="gs_school">School</label>
           </div>
           <div class="form-floating flex-fill mb-3 p-1">
             <input type="text" class="form-control" id="add_gs_degree_course[${x}]" name ="gs_degree_course[${x}]" placeholder="Degree / Course" value="" form="add_masteral_form">
             <label for="gs_degree_course">Degree / Course</label>
           </div>
           <div class="form-floating flex-fill mb-3 p-1">
             <select class="form-select" id="add_gs_highest_level_units_earned[${x}]" name="gs_highest_level_units_earned[${x}]" aria-label="Floating label select example" value="" form="add_masteral_form" onchange="graduated(this, document.getElementById('add_gs_highest_grade_year_units[${x}]'), document.getElementById('add_gs_scholarship_academic_honor[${x}]'), document.getElementById('add_gs_period_of_attendance_from[${x}]'), document.getElementById('add_gs_period_of_attendance_to[${x}]'))" required>
               <option class="" value="" selected>-</option>
               <option value="GRADUATED">GRADUATED</option>
               <option value="UNDERGRADUATE">UNDERGRADUATE</option>
               <option value="CURRENTLY ENROLLED">CURRENTLY ENROLLED</option>
             </select>
             <label for="gs_highest_level">Highest Level Attained</label>
           </div>
       </div>
       <div class="d-md-flex flex-row">
         <div class="form-floating flex-fill mb-3 p-1">
           <input type="number" class="form-control" id="add_gs_period_of_attendance_from[${x}]" name ="gs_period_of_attendance_from[${x}]" placeholder="Period of Attendance (From)" value="" form="add_masteral_form">
           <label for="gs_period_of_attendance_from">Period of Attendance (From)</label>
         </div>
         <div class="form-floating flex-fill mb-3 p-1">
           <input type="number" class="form-control" id="add_gs_period_of_attendance_to[${x}]" name ="gs_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" value="" form="add_masteral_form">
           <label for="gs_period_of_attendance_to">Period of Attendance (To)</label>
         </div>
       </div>
       <div class="d-md-flex flex-row">
         <div class="form-floating flex-fill mb-3 p-1">
           <input type="text" class="form-control" id="add_gs_highest_grade_year_units[${x}]" name ="gs_highest_grade_year_units[${x}]" placeholder="Highest Level" value="" form="add_masteral_form">
           <label for="gs_highest_grade_year_units">Units Earned</label>
         </div>   
         <div class="form-floating flex-fill mb-3 p-1">
           <input type="text" class="form-control" id="add_gs_scholarship_academic_honor[${x}]" name ="gs_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" value="" form="add_masteral_form">
           <label for="gs_scholarship_academic_honor">Scholarship / Academic Honor</label>
         </div> 
       </div>
       <a href="#" onclick="document.getElementById('masteral_no_fields').value--;document.getElementById('remove_masteral${x}').remove(); return false">Remove</a>
       </div>
       </div>
          `);
      // }
  });


  var doctoral_no_fields = document.getElementById('doctoral_no_fields');
  document.getElementById('add_doctoral_field').addEventListener('click',()=>{
      var doctoral_fields = document.getElementById('doctoral_fields');
      doctoral_fields.innerHTML = ``;
      var x = doctoral_no_fields.value;
      // for(var x = 1; x < cs_no_fields.value; x++){
        doctoral_fields.insertAdjacentHTML("beforebegin",`
          <div class="card shadow-sm mb-3" id="remove_doctoral${x}">
            <div class="card-body">
              <div class="d-md-flex flex-row">
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_doc_school[${x}]" name ="doc_school[${x}]" placeholder="School" value="" form="add_doctoral_form">
                  <label for="doc_school">School</label>
                </div>
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_doc_degree_course[${x}]" name ="doc_degree_course[${x}]" placeholder="Degree / Course" value="" form="add_doctoral_form">
                  <label for="doc_degree_course">Degree / Course</label>
                </div>
                <div class="form-floating flex-fill mb-3 p-1">
                  <select class="form-select" id="add_doc_highest_level_units_earned[${x}]" name="doc_highest_level_units_earned[${x}]" aria-label="Floating label select example" value="" form="add_doctoral_form" onchange="graduated(this, document.getElementById('add_doc_highest_grade_year_units[${x}]'), document.getElementById('add_doc_scholarship_academic_honor[${x}]'), document.getElementById('add_doc_period_of_attendance_from[${x}]'), document.getElementById('add_doc_period_of_attendance_to[${x}]'))" required>
                    <option class="" value="" selected>-</option>
                    <option value="GRADUATED">GRADUATED</option>
                    <option value="UNDERGRADUATE">UNDERGRADUATE</option>
                    <option value="CURRENTLY ENROLLED">CURRENTLY ENROLLED</option>
                  </select>
                  <label for="doc_highest_level">Highest Level Attained</label>
                </div>
            </div>
            <div class="d-md-flex flex-row">
              <div class="form-floating flex-fill mb-3 p-1">
                <input type="number" class="form-control" id="add_doc_period_of_attendance_from[${x}]" name ="doc_period_of_attendance_from[${x}]" placeholder="Period of Attendance (To)" value="" form="add_doctoral_form">
                <label for="doc_period_of_attendance_from">Period of Attendance (From)</label>
              </div>
              <div class="form-floating flex-fill mb-3 p-1">
                <input type="number" class="form-control" id="add_doc_period_of_attendance_to[${x}]" name ="doc_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" value="" form="add_doctoral_form">
                <label for="doc_period_of_attendance_to">Period of Attendance (To)</label>
              </div>
            </div>
            <div class="d-md-flex flex-row">
              <div class="form-floating flex-fill mb-3 p-1">
                <input type="text" class="form-control" id="add_doc_highest_grade_year_units[${x}]" name ="doc_highest_grade_year_units[${x}]" placeholder="Highest Level" value="" form="add_doctoral_form">
                <label for="doc_highest_grade_year_units">Units Earned</label>
              </div>
              <div class="form-floating flex-fill mb-3 p-1">
                <input type="text" class="form-control" id="add_doc_scholarship_academic_honor[${x}]" name ="doc_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" value="" form="add_doctoral_form">
                <label for="doc_scholarship_academic_honor">Scholarship / Academic Honor</label>
              </div>   
            </div>
          <a href="#" onclick="document.getElementById('doctoral_no_fields').value--;document.getElementById('remove_doctoral${x}').remove(); return false">Remove</a>

          </div>
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
          <div class="card shadow-sm mb-3" id="remove_vocational${x}" >
          <div class="card-body">
              <div class="d-md-flex flex-row">
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_v_school[${x}]" name ="v_school[${x}]" placeholder="School" value="" form="add_vocational_form" required>
                  <label for="v_school">School</label>
                </div>
                
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_vocational_trade_course[${x}]" name ="vocational_trade_course[${x}]" placeholder="Vocational / Trade Course" value="" form="add_vocational_form">
                  <label for="vocational_trade_course">Vocational / Trade Course</label>
                </div>

                <div class="form-floating flex-fill mb-3 p-1">
                  <select class="form-select" id="add_v_highest_level[${x}]" name="v_highest_level[${x}]" aria-label="Floating label select example" value="" form="add_vocational_form" onchange="graduated(this, document.getElementById('add_v_highest_grade_year_units[${x}]'), document.getElementById('add_v_scholarship_academic_honor[${x}]'), document.getElementById('add_v_period_of_attendance_from[${x}]'), document.getElementById('add_v_period_of_attendance_to[${x}]'))" required>
                    <option class="" value="" selected>-</option>
                    <option value="GRADUATED">GRADUATED</option>
                    <option value="UNDERGRADUATE">UNDERGRADUATE</option>
                    <option value="CURRENTLY ENROLLED">CURRENTLY ENROLLED</option>
                  </select>
                  <label for="hs_highest_level">Highest Level Attained</label>
                </div>
              </div>
              <div class="d-md-flex flex-row">
                <div class="form-floating col-sm-4 mb-3 p-1">
                  <input type="date" class="form-control" id="v_date_of_validity[${x}]" name="v_date_of_validity[${x}]" placeholder="Date of Validity of NC II" form="add_vocational_form" value="">
                  <label for="v_period_of_attendance_from">Date of Validity of NC II</label>
                </div>
              </div>
              <div class="d-md-flex flex-row">
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="number" class="form-control" id="add_v_period_of_attendance_from[${x}]" name ="v_period_of_attendance_from[${x}]" placeholder="Period of Attendance (From)" value="" form="add_vocational_form" oninput="year_only(this)">
                  <label for="v_period_of_attendance_from">Period of Attendance (From)</label>
                </div>
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="number" class="form-control" id="add_v_period_of_attendance_to[${x}]" name ="v_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" value="" form="add_vocational_form" oninput="year_only(this)">
                  <label for="v_period_of_attendance_to">Period of Attendance (To)</label>
                </div>
              </div>
              <div class="d-md-flex flex-row">
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_v_highest_grade_year_units[${x}]" name ="v_highest_grade_year_units[${x}]" placeholder="Highest Level" value="" form="add_vocational_form">
                  <label for="v_highest_grade_year_units">Units Earned</label>
                </div>   
                <div class="form-floating flex-fill mb-3 p-1">
                  <input type="text" class="form-control" id="add_v_scholarship_academic_honor[${x}]" name ="v_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" value="" form="add_vocational_form">
                  <label for="v_scholarship_academic_honor">Scholarship / Academic Honor</label>
                </div>  
              </div>
              <a href="#" onclick="document.getElementById('vocational_no_fields').value--;document.getElementById('remove_vocational${x}').remove(); return false">Remove</a>
        </div>
      </div>
          `);
      //  }
  });
  
//   document.getElementById('add_ld_field').addEventListener('click',()=>{
//       var vocational_fields = document.getElementById('ld_fields');
//       var vocational_no_fields = document.getElementById('ld_no_fields');
//       vocational_fields.innerHTML = ``;
//           var x = vocational_no_fields.value;
//           vocational_fields.insertAdjacentHTML("beforebegin",`
//           <div class="card shadow-sm mb-3" id=remove_ld${x}>
//               <div class="card-body">
//                   <div class="d-md-flex flex-row">
//                       <div class="form-floating flex-fill mb-3 p-1">
//                           <input type="text" class="form-control" name ="ld_program[${x}]" placeholder="Interventions/Training Program" form="add_ld_form">
//                           <label for="ld_program">Interventions / Training Program</label>
//                       </div>
//                       <div class="form-floating flex-fill mb-3 p-1">
//                           <input type="date" class="form-control" name ="ld_date_from[${x}]" placeholder="Inclusive Date of Attendance From" form="add_ld_form">
//                           <label for="ld_date_from">Inclusive Date of Attendance From</label>
//                       </div>
//                       <div class="form-floating flex-fill mb-3 p-1">
//                           <input type="date" class="form-control" name ="ld_date_to[${x}]" placeholder="Inclusive Date of Attendance To" form="add_ld_form">
//                           <label for="ld_date_to">Inclusive Date of Attendance To</label>
//                       </div>
//                       </div>
//                       <div class="d-md-flex flex-row">
//                       <div class="form-floating flex-fill mb-3 p-1">
//                           <input type="number" class="form-control" name ="ld_no_hours[${x}]" placeholder="Rating" form="add_ld_form">
//                           <label for="ld_no_hours">Number of Hours</label>
//                       </div>
//                       <div class="form-floating flex-fill mb-3 p-1">
//                           <input type="text" class="form-control" name ="ld_type[${x}]" placeholder="Type of Learning & Development (Ex. Manegerial, Supervisory, Technical)" form="add_ld_form">
//                           <label for="ld_type">Type of Learning & Development (Ex. Manegerial, Supervisory, Technical)</label>
//                       </div>
//                       </div>
//                       <div class="d-md-flex flex-row">
//                       <div class="form-floating flex-fill mb-3 p-1 col-md-6">
//                           <input type="text" class="form-control" name ="ld_sponsored_by[${x}]" placeholder="Conducted / Sponsored By" form="add_ld_form">
//                           <label for="license_no">Conducted / Sponsored By</label>
//                       </div>
//                   </div>
//                   <a href="#" onclick="document.getElementById('ld_no_fields').value--;document.getElementById('remove_ld${x}').remove(); return false">Remove field</a>
//               </div>
//           </div>
  
//           `);

//   });