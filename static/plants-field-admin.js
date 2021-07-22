(function($) {
    $(function() {
        var productType = $('#id_product_type'),
            nutritionalValue = $('.field-nutritional_value');
            howToGrowSoilNeed = $('.field-how_to_grow_soil_need');
            howToGrowFertilizersType = $('.field-how_to_grow_fertilizer_type');
            howToGrowProcess = $('.field-how_to_grow_process');
            howToGrowGrowthPattern = $('.field-how_to_grow_growth_pattern');
            howToGrowPruning = $('.field-how_to_grow_pruning');
            howToGrowRePotting = $('.field-how_to_grow_re_potting');
            maintenanceTipDo = $('.field-maintenance_tip_do');
            maintenanceTipDont = $('.field-maintenance_tip_dont');
            toxicity = $('.field-toxicity');
            maintenanceLevel = $('.field-maintenance_level');
            waterFrequencySummer = $('.field-water_frequency_summer');
            waterFrequencyWinter = $('.field-water_frequency_winter');
            fertilizerFrequencySummer = $('.field-fertilizer_frequency_summer');
            fertilizerFrequencyWinter = $('.field-fertilizer_frequency_winter');
            season = $('.field-season');
            familyName = $('.field-family_name');
            fragrance = $('.field-fragrance');
            plantType = $('.field-plant_type');
            flower = $('.field-flower');
            flowerColor = $('.field-flower_color');
            oxygenSunlight = $('.field-oxygen_sunlight');
            oxygenNight = $('.field-oxygen_night');
            // pot size
            // potSizeMin = $('.field-pot_size_min');
            // potSizeMax = $('.field-pot_size_max');

            minHeight = $('.field-min_height');
            maxHeight = $('.field-max_height');

            width = $('.field-width');
            height = $('.field-height');
            diameter = $('.field-diameter');





        function toggleNutrional(value) {
          if(value != 'Plants'){
            if(value != 'Pots'){
              width.hide();
              height.hide();
              diameter.hide();
            } else {
              width.show();
              height.show();
              diameter.show();
            }

            nutritionalValue.hide();
            howToGrowSoilNeed.hide();
            howToGrowFertilizersType.hide();
            howToGrowProcess.hide();
            howToGrowGrowthPattern.hide();
            howToGrowPruning.hide();
            howToGrowRePotting.hide();
            maintenanceTipDo.hide();
            maintenanceTipDont.hide();
            toxicity.hide();
            maintenanceLevel.hide();
            waterFrequencySummer.hide();
            waterFrequencyWinter.hide();
            fertilizerFrequencySummer.hide();
            fertilizerFrequencyWinter.hide();
            season.hide();
            familyName.hide();
            fragrance.hide();
            plantType.hide();
            flower.hide();
            flowerColor.hide();
            oxygenSunlight.hide();
            oxygenNight.hide();
            minHeight.hide();
            maxHeight.hide();
          } else {
            nutritionalValue.show();
            howToGrowSoilNeed.show();
            howToGrowFertilizersType.show();
            howToGrowProcess.show();
            howToGrowGrowthPattern.show();
            howToGrowPruning.show();
            howToGrowRePotting.show();
            maintenanceTipDo.show();
            maintenanceTipDont.show();
            toxicity.show();
            maintenanceLevel.show();
            waterFrequencySummer.show();
            waterFrequencyWinter.show();
            fertilizerFrequencySummer.show();
            fertilizerFrequencyWinter.show();
            season.show();
            familyName.show();
            fragrance.show();
            plantType.show();
            flower.show();
            flowerColor.show();
            oxygenSunlight.show();
            oxygenNight.show();
            minHeight.show();
            maxHeight.show();
            // potSizeMin.show();
            // potSizeMax.show();
            width.hide();
            diameter.hide();
            height.hide();
          }
        }
        // show/hide on load based on pervious value of productType
        toggleNutrional(productType.val());


        // show/hide on change
        productType.change(function() {
            toggleNutrional($(this).val());
        });
    });
})(django.jQuery);
