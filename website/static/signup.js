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


function sameAsPermanent(){
	var citizenship = document.getElementById('same_as_permanent').value;
	if(citizenship == 'Yes'){
				document.getElementById('pres_house_block_lot').disabled = true;
				document.getElementById('pres_street').disabled = true;
				document.getElementById('pres_subdivision_village').disabled = true;
				document.getElementById('pres_barangay').disabled = true;
				document.getElementById('pres_city_municipality').disabled = true;
				document.getElementById('pres_province').disabled = true;
				document.getElementById('pres_zip_code').disabled = true;

				document.getElementById('pres_house_block_lot').value = document.getElementById('p_house_block_lot').value;
				document.getElementById('pres_street').value = document.getElementById('p_street').value;
				document.getElementById('pres_subdivision_village').value = document.getElementById('p_subdivision_village').value;
				document.getElementById('pres_barangay').value = document.getElementById('p_barangay').value;
				document.getElementById('pres_city_municipality').value = document.getElementById('p_city_municipality').value;
				document.getElementById('pres_province').value = document.getElementById('p_province').value;
				document.getElementById('pres_zip_code').value = document.getElementById('p_zip_code').value;
		}else{
				document.getElementById('pres_house_block_lot').removeAttribute('disabled');
				document.getElementById('pres_street').removeAttribute('disabled');
				document.getElementById('pres_subdivision_village').removeAttribute('disabled');
				document.getElementById('pres_barangay').removeAttribute('disabled');
				document.getElementById('pres_city_municipality').removeAttribute('disabled');
				document.getElementById('pres_province').removeAttribute('disabled');
				document.getElementById('pres_zip_code').removeAttribute('disabled');

				document.getElementById('pres_house_block_lot').value = ""
				document.getElementById('pres_street').value = ""
				document.getElementById('pres_subdivision_village').value = ""
				document.getElementById('pres_barangay').value = ""
				document.getElementById('pres_city_municipality').value = ""
				document.getElementById('pres_province').value = ""
				document.getElementById('pres_zip_code').value = ""
		}
}


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



//code for submit
document.getElementById("signUp").addEventListener("submit", function(e){
  e.preventDefault()
  var file_input = document.getElementById('psa');

  if(file_input.files.length == 0){
  	alert("No file selected")
  }

//console.log(file_input.files)

  var formElem = document.getElementById("signUp");
  let formData = new FormData(formElem);
  //formData.append('file',  input.files[0])

  const data = {}
  formData.forEach((value, key) => (data[key] = value))
 
  // for (var i = 0; i < file_input.files.length; i++) {
  // 	formData.append("files[]", document.getElementById('psa').files[i]);
  // }
  console.log(data)
  fetch('/signup', {
		method: 'POST',
		body: formData
	}).then((res)=>{
		setTimeout(function() { 
			triggerToast(); 
			setTimeout(()=>{
				document.getElementById('toastBody').innerHTML = ""
			},6000)
		}, 450);
		
	}).catch(console.error)
});


//code for submit eligibility in signup
// document.getElementById("add_eligibility_form_sign_up").addEventListener("submit", function(e){
// 	e.preventDefault()

// 	var formElem = document.getElementById("signUp");
// 	let formData = new FormData(formElem);
  
// 	const data = {}
// 	formData.forEach((value, key) => (data[key] = value))
   
// 	console.log(data)
// 	fetch('/signup', {
// 		  method: 'POST',
// 		  body: formData
// 	  }).then((res)=>{
// 		  setTimeout(function() { 
// 			  triggerToast(); 
// 			  setTimeout(()=>{
// 				  document.getElementById('toastBody').innerHTML = ""
// 			  },6000)
// 		  }, 450);
		  
// 	  }).catch(console.error)
//   });


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
				<input type="text" class="form-control" name ="cs_eligibility[${x}]" placeholder="Eligibility" form="signUp">
				<label for="cs_eligibility">Career Service / RA 1080 (BOARD/BAR) Under Special Laws / CES / CSEE / Barangay Eligibility / Driver's License</label>
				</div>
				<div class="form-floating flex-fill mb-3 p-1">
					<input type="date" class="form-control" name ="date_of_examination[${x}]" placeholder="Date of Examination" form="signUp">
					<label for="date_of_examination">Date of Examination</label>
				</div>
			</div>
			<div class="d-md-flex flex-row">
				<div class="form-floating flex-fill mb-3 p-1">
				<input type="text" class="form-control" name ="cs_rating[${x}]" placeholder="Rating" form="signUp">
				<label for="cs_rating">Rating (if applicable)</label>
				</div>
				<div class="form-floating flex-fill mb-3 p-1">
				<input type="text" class="form-control" name ="place_of_examination_conferment[${x}]" placeholder="Place of Examination / Conferment" form="signUp">
				<label for="place_of_examination_conferment">Place of Examination / Conferment</label>
				</div>
			</div>
			<div class="d-md-flex flex-row">
			<div class="form-floating flex-fill mb-3 p-1 col-md-6">
				<input type="text" class="form-control" name ="license_no[${x}]" placeholder="License Number" form="signUp">
				<label for="license_no">License Number</label>
			</div>
			<div class="form-floating flex-fill mb-3 p-1">
				<input type="date" class="form-control" name ="date_of_validity[${x}]" placeholder="Date of Validity" form="signUp">
				<label for="date_of_validity">Date of Validity</label>
			</div> 
			
			</div>
			<div class="d-md-flex flex-row">
            <div class="flex-fill mb-3 p-1">
              <label for="psa" class="form-label">Upload Supporting Document</label>
              <input class="form-control" type="file" id="cse[${x}]" name="cse[${x}]" form="signUp">
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
					<input type="text" class="form-control" id="v_school[${x}]" name ="v_school[${x}]" placeholder="School" form="signUp">
					<label for="v_school">School</label>
					</div>
					<div class="form-floating flex-fill mb-3 p-1">
					<input type="text" class="form-control" id="vocational_trade_course[${x}]" name ="vocational_trade_course[${x}]" placeholder="Vocational / Trade Course" form="signUp">
					<label for="vocational_trade_course">Vocational / Trade Course</label>
					</div>
					<div class="form-floating flex-fill mb-3 p-1">
					<input type="text" class="form-control" id="v_period_of_attendance_from[${x}]" name ="v_period_of_attendance_from[${x}]" placeholder="Period of Attendance (From)" form="signUp">
					<label for="v_period_of_attendance_from">Period of Attendance (From)</label>
					</div>
					<div class="form-floating flex-fill mb-3 p-1">
					<input type="text" class="form-control" id="v_period_of_attendance_to[${x}]" name ="v_period_of_attendance_to[${x}]" placeholder="Period of Attendance (To)" form="signUp">
					<label for="v_period_of_attendance_to">Period of Attendance (To)</label>
					</div>
				</div>
				<div class="d-md-flex flex-row">
					<div class="form-floating flex-fill mb-3 p-1">
					<input type="text" class="form-control" id="v_highest_level[${x}]" name ="v_highest_level[${x}]" placeholder="Highest Level" form="signUp">
					<label for="v_highest_level">Highest Level Attained / Units Earned</label>
					</div>   
					<div class="form-floating flex-fill mb-3 p-1">
					<input type="text" class="form-control" id="v_scholarship_academic_honor[${x}]" name ="v_scholarship_academic_honor[${x}]" placeholder="Scholarship / Academic Honor" form="signUp">
					<label for="v_scholarship_academic_honor">Sholarship / Academic Honor</label>
					</div>  
				</div>
				<a href="#" onclick="document.getElementById('vocational_no_fields').value--;document.getElementById('remove_vocational${x}').remove(); return false">Remove field</a>
				</div>
			</div>
		`);
	//  }
});