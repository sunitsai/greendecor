	var _search = instantsearch({
        appId: 'AGHBVMU77S',
        apiKey: 'b5fb475940558ecf9d3ea95a20603b6e',
        indexName: 'my_index',
		urlSync: true
      });
      _search.addWidget(
        instantsearch.widgets.searchBox({
          container: '#search-box',
          placeholder: 'Search for products...'
        })
      );

      _search.addWidget(
        instantsearch.widgets.pagination({
          container: '#pagination-container',
			labels: {
				  previous: '<i class="fa fa-angle-left fa-2x"></i>',
				  next: '<i class="fa fa-angle-right fa-2x"></i>'
				},
				showFirstLast: false
        	})
      );
      _search.on('render', function(options) {
		  $(window).scroll(function(){
			  $(window).scrollTop==0;
		  });
      });

      var hitTemplate =
      '<div class="col-sm-4 search-card"> <div class="card">'+
                       ' <a href="/plant/{{slug}}">'+
                                        '<div class="slider-image">'+
                                            ' <img src="/media/{{my_image.image}}" alt="{{my_image.alt}}" title="{{my_image.title}}">'+
                                            '</div></a>'+
                                        ' <div class="content"><a href="/plant/{{slug}}">'+
                                        '<h6 class="title">{{{_highlightResult.name.value}}}</h6>'+
                                ' <h6 class="price active-price"><i class="fa fa-inr"></i>{{selling_price}}</h6>'+
                                        '</a><div class="hollow-button"><a onclick="add_to_cart({{objectID}},1)" class="button"><i class="fa fa-shopping-cart"></i>'+
                                    'Add To Cart</a></div>'+
                                '</div>'+
                            '</div>'+
                    '</div>';

        var noTemplate='<div class="col-sm-8 text-center col-centered" style="padding:40px 0px;"><p>You searched for <strong>{{query}}</strong></p><h3 class="title">We couldnt find any matches!</h3><p>Please check the spelling or try searching something else</p></div>';

        var filterTemplate='<div class="col-sm-12 no-gutter category">'+
                                    '<label><input type="checkbox" class="{{cssClasses.checkbox}}" value="{{name}}" {{#isRefined}}checked{{/isRefined}} / name="optcheckbox"><span>{{name}}<span></label>'+
                                '</div>';
      _search.addWidget(
        instantsearch.widgets.hits({
          container: '#result',
		  hitsPerPage: 9,
          templates: {
            empty:noTemplate,
            item: hitTemplate,
          }
        })
      );
		_search.addWidget(
		  instantsearch.widgets.rangeSlider({
			container: '#prices',
			attributeName: 'selling_price',
			cssClasses: {
			  count: 'count',
			  active: 'active'
			}
		  })
		);
		_search.addWidget(
		  instantsearch.widgets.stats({
			container: '#stats-container'
		  })
		);
		_search.addWidget(
		  instantsearch.widgets.sortBySelector({
			container: '#sort-by-selector',
			indices: [
			  {name: 'my_index', label: 'All Result'},
			  {name: 'selling_price_asc', label: 'Low to High'},
			  {name: 'selling_price_desc', label: 'High to Low'}
			]
		  })
		);
      _search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#tags',
            attributeName: '_tags',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
		_search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#season',
            attributeName: '_season',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
		_search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#fragrance',
            attributeName: 'fragrance',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
	_search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#placemen',
            attributeName: 'placement',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
	_search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#category',
            attributeName: '_category',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
	_search.addWidget(
          instantsearch.widgets.refinementList({
            container: '#maintenance_level',
            attributeName: 'maintenance_level',
            operator: 'or',
            sortBy: ['name:asc'],
            limit: 10,
            templates: {
              item: filterTemplate
            }
          })
        );
		_search.addWidget(
			  instantsearch.widgets.clearAll({
				container: '#clear-all',
				templates: {
				  link: '<i class="fa fa-times"></i> Clear all'
				},
				cssClasses: {
				 root: 'clear-all'
				},
				autoHideContainer: true
			  })
			);
//            var client = algoliasearch("145V1NEFNV", "2841c5d513038a1c527b12a78ae04106")
//            var players = client.initIndex('Company');
//            var searchInput = document.getElementById('search-box');
//            var inputContainer = document.getElementById('search-box-container');
//
//            autocomplete('#search-box', {}, [
//                {
//                  source: autocomplete.sources.hits(players, { hitsPerPage: 5 }),
//                  displayKey: 'name',
//                  templates: {
//                    suggestion: function(suggestion) {
//                      return '<span>' +
//                        suggestion._highlightResult.name.value + '</span>';
//                    }
//                  }
//                }
////                {
////                  source: autocomplete.sources.hits(teams, { hitsPerPage: 3 }),
////                  displayKey: 'name',
////                  templates: {
////                    header: '<div class="aa-suggestions-category">Teams</div>',
////                    suggestion: function(suggestion) {
////                      return '<span>' +
////                        suggestion._highlightResult.name.value + '</span><span>'
////                          + suggestion._highlightResult.location.value + '</span>';
////                    }
////                  }
////                }
//            ]).on('autocomplete:updated', function() {
//                        if (searchInput.value.length > 0) {
//                            inputContainer.classList.add("input-has-value");
//                        }
//                        else {
//                            inputContainer.classList.remove("input-has-value");
//                        }
//                    });
      _search.start();
$('#clear-all').click(function(){
	var q=$(this).find('a.ais-clear-all--link').attr('href')
	window.location.href=q;
});