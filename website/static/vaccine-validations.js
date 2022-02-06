(function () {
    'use strict'
  window.addEventListener('load',(e)=>{
      activate_booster_shot();
      activate_covid_vac();
  })
      document.getElementById('do_you_have_booster').addEventListener('change', activate_booster_shot);
      document.getElementById('are_you_covid_vac').addEventListener('change', activate_covid_vac);
        
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
  
        function activate_covid_vac(){
          var vac_id_no = document.getElementById('vac_id_no');
          var vac_brand = document.getElementById('vac_brand');
          var vac_place = document.getElementById('vac_place');
          var vac_first_dose = document.getElementById('vac_first_dose');
          var vac_second_dose = document.getElementById('vac_second_dose');
          var are_you_covid_vac = document.getElementById('are_you_covid_vac');
          var vaccine_card = document.getElementById('vaccine_card');

  
          if (are_you_covid_vac.value == "YES"){
            vac_id_no.disabled = false;
            vac_brand.disabled = false;
            vac_place.disabled = false;
            vac_first_dose.disabled = false;
            vac_second_dose.disabled = false;
            vaccine_card.disabled = false;

          }else{
            vac_id_no.disabled = true;
            vac_brand.disabled = true;
            vac_place.disabled = true;
            vac_first_dose.disabled = true;
            vac_second_dose.disabled = true;
            vaccine_card.disabled = true;

  
            vac_id_no.value = "";
            vac_brand.value = "";
            vac_place.value = "";
            vac_first_dose.value = "";
            vac_second_dose.value = "";
            vaccine_card.value = "";

          
            }
          }
  
  
  })()