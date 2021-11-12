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

